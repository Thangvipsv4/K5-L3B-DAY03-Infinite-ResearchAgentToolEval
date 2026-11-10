from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import (
    ARTIFACTS_DIR,
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).parent
TRANSCRIPTS_DIR = ROOT / "transcripts"
SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"
PROVIDER_KEYS = {
    "openrouter": "OPENROUTER_API_KEY",
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
}


def new_transcript(config: dict[str, Any]) -> dict[str, Any]:
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join(
        [safe_slug(config["version"]), safe_slug(config["provider"]), timestamp]
    )
    artifact_version = build_artifact_version(
        config["version"], SYSTEM_PROMPT_PATH, TOOLS_PATH
    )
    return {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": config["provider"],
        "model": config["model"] or None,
        "system_prompt": str(SYSTEM_PROMPT_PATH),
        "tools": str(TOOLS_PATH),
        "history_window": config["history_window"],
        "max_tool_rounds": config["max_tool_rounds"],
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }


def start_conversation(config: dict[str, Any]) -> None:
    st.session_state["active_config"] = config.copy()
    st.session_state["messages"] = []
    st.session_state["history"] = []
    st.session_state["transcript"] = new_transcript(config)


def save_current_transcript() -> Path:
    transcript_path = (
        TRANSCRIPTS_DIR
        / f"{st.session_state['transcript']['transcript_id']}.transcript.json"
    )
    write_transcript(transcript_path, st.session_state["transcript"])
    return transcript_path


st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="centered")
st.title("🔎 Research Agent")
st.caption("Chat local với research agent; mỗi lượt và tool call được lưu thành transcript.")

with st.sidebar:
    st.header("Cấu hình")
    provider_name = st.selectbox(
        "Provider",
        ["openrouter", "openai", "anthropic", "gemini", "ollama"],
        format_func=str.title,
    )
    model_name = st.text_input(
        "Model (để trống dùng mặc định)", placeholder="Ví dụ: openai/gpt-4o-mini"
    ).strip()
    version = st.text_input("Phiên bản artifact", value="v3").strip() or "v3"
    history_window = st.number_input(
        "Số lượt chat giữ trong ngữ cảnh", min_value=0, max_value=20, value=5
    )
    max_tool_rounds = st.number_input(
        "Số vòng gọi tool tối đa", min_value=1, max_value=10, value=4
    )
    st.divider()
    key_name = PROVIDER_KEYS.get(provider_name)
    if key_name:
        if os.getenv(key_name):
            st.success(f"Đã tìm thấy {key_name}.")
        else:
            st.warning(f"Chưa cấu hình {key_name} trong `.env`.")
    else:
        st.info("Ollama dùng server local; kiểm tra OLLAMA_BASE_URL nếu cần.")
    if st.button("Cuộc trò chuyện mới", use_container_width=True):
        start_conversation(
            {
                "provider": provider_name,
                "model": model_name,
                "version": version,
                "history_window": int(history_window),
                "max_tool_rounds": int(max_tool_rounds),
            }
        )

config = {
    "provider": provider_name,
    "model": model_name,
    "version": version,
    "history_window": int(history_window),
    "max_tool_rounds": int(max_tool_rounds),
}
if "transcript" not in st.session_state:
    start_conversation(config)

active_config = st.session_state["active_config"]
settings_changed = config != active_config
if settings_changed and not st.session_state["transcript"]["turns"]:
    start_conversation(config)
    settings_changed = False
elif settings_changed:
    st.warning(
        "Cấu hình đã thay đổi. Hãy bấm **Cuộc trò chuyện mới** để áp dụng cấu hình "
        "mới và tạo transcript riêng."
    )

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("tool_events"):
            with st.expander("Chi tiết tool call"):
                st.json(message["tool_events"])

if not st.session_state["messages"]:
    st.info("Nhập câu hỏi nghiên cứu để bắt đầu.")

prompt = None
if not settings_changed:
    prompt = st.chat_input("Bạn muốn nghiên cứu điều gì?")

if prompt:
    user_message = {"role": "user", "content": prompt}
    st.session_state["messages"].append(user_message)
    with st.chat_message("user"):
        st.markdown(prompt)

    turn_record: dict[str, Any] = {
        "turn_index": len(st.session_state["transcript"]["turns"]) + 1,
        "started_at": now_iso(),
        "user": prompt,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }
    try:
        provider = make_provider(provider_name)
        provider_model = model_name or getattr(provider, "default_model", None)
        declarations = load_tool_declarations(TOOLS_PATH)
        result = run_model_tool_loop(
            provider=provider,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")},
                *trim_history(st.session_state["history"], int(history_window)),
                {"role": "user", "content": prompt},
            ],
            tools=to_openai_tools(declarations),
            model=provider_model,
            max_tool_rounds=int(max_tool_rounds),
        )
        turn_record.update(result)
        assistant_text = result["assistant_text"]
        st.session_state["history"].extend(
            [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": assistant_text},
            ]
        )
        assistant_message = {
            "role": "assistant",
            "content": assistant_text or "Agent không trả về nội dung.",
            "tool_events": result["tool_events"],
        }
        st.session_state["messages"].append(assistant_message)
        with st.chat_message("assistant"):
            st.markdown(assistant_message["content"])
            if result["tool_events"]:
                with st.expander("Chi tiết tool call"):
                    st.json(result["tool_events"])
    except Exception as exc:
        error_message = f"{type(exc).__name__}: {exc}"
        turn_record.update({"status": "provider_error", "error": error_message})
        st.session_state["messages"].append(
            {"role": "assistant", "content": f"Lỗi: {error_message}"}
        )
        with st.chat_message("assistant"):
            st.error(error_message)
    finally:
        turn_record["ended_at"] = now_iso()
        st.session_state["transcript"]["turns"].append(turn_record)
        try:
            saved_path = save_current_transcript()
            st.caption(f"Transcript: `{saved_path.relative_to(ROOT)}`")
        except OSError as exc:
            st.error(f"Không thể lưu transcript: {exc}")

with st.sidebar:
    if st.session_state.get("transcript"):
        transcript = st.session_state["transcript"]
        st.caption(f"Artifact: `{transcript['artifact_version']}`")
        if transcript["turns"]:
            st.caption(f"Transcript: `{transcript['transcript_id']}`")
