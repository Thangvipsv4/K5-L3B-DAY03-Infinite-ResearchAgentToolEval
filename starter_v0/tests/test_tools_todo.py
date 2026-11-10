
"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a real test for the existing tools.
Patterns are based on test_tools_examples.py.
Fixtures are in conftest.py.
"""

from __future__ import annotations

import pytest

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    result = TOOL_FUNCTIONS["clarify"](
        question="Bạn muốn chọn phương án nào?",
        response_type="choice",
        options=["ADAS", "Fintech"],
    )

    assert result["options"] == ["ADAS", "Fintech"]
    assert result["awaiting_user"] is True


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    result = TOOL_FUNCTIONS["format"](
        items=[
            {"title": "Tin A1", "section": "A"},
            {"title": "Tin B1", "section": "B"},
            {"title": "Tin A2", "section": "A"},
        ],
        template="sections",
    )

    assert result["markdown"].count("## A") == 1
    assert result["markdown"].count("## B") == 1


def test_format_thread_numbers_items() -> None:
    result = TOOL_FUNCTIONS["format"](
        items=[
            {"title": "Tin thứ nhất"},
            {"title": "Tin thứ hai"},
        ],
        template="thread",
    )

    lines = result["markdown"].splitlines()

    assert lines[0].startswith("1/")
    assert lines[2].startswith("2/")


def test_format_empty_items_does_not_crash() -> None:
    result_none = TOOL_FUNCTIONS["format"](items=None)
    result_empty = TOOL_FUNCTIONS["format"](items=[])

    assert result_none["item_count"] == 0
    assert result_empty["item_count"] == 0


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "123456")

    calls = fake_http(FakeResponse({"ok": True}))

    result = TOOL_FUNCTIONS["send"](
        text="Hello from AI20K",
        confirmed=True,
    )

    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert "test-token" in calls[0]["url"]
    assert calls[0]["json"]["chat_id"] == "123456"
    assert calls[0]["json"]["text"] == "Hello from AI20K"
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))

    result = TOOL_FUNCTIONS["send"](
        text="Hello",
        confirmed=True,
    )

    assert "error" in result
    assert calls == []


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")

    calls = fake_http(FakeResponse({"results": []}))

    TOOL_FUNCTIONS["lookup"](
        query="AI research",
        timeframe=None,
    )

    assert len(calls) == 1
    assert "time_range" not in calls[0]["json"]


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")

    calls = fake_http(FakeResponse({
        "data": {
            "markdown": "This is a research article about AI.",
            "metadata": {
                "title": "AI Research",
                "sourceURL": "https://example.com/ai",
            },
        }
    }))

    result = TOOL_FUNCTIONS["fetch"](
        url="https://example.com/ai"
    )

    assert len(calls) == 1

    item = result["items"][0]

    assert item["title"] == "AI Research"
    assert item["url"] == "https://example.com/ai"
    assert item["source"] == "example.com"
    assert "research article" in item["summary"]


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")

    fake_http(FakeResponse({
        "data": {
            "markdown": "A" * 5000,
            "metadata": {
                "title": "Long article",
                "sourceURL": "https://example.com/long",
            },
        }
    }))

    result = TOOL_FUNCTIONS["fetch"](
        url="https://example.com/long"
    )

    assert len(result["items"][0]["summary"]) == 4000


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    monkeypatch.setenv(
        "RAPIDAPI_TWITTER_HOST",
        "twitter-api45.p.rapidapi.com",
    )

    timeline_data = [
        {"text": "Missing ID"},
        *[
            {
                "tweet_id": str(i),
                "text": f"Tweet {i}",
                "screen_name": "testuser",
            }
            for i in range(1, 7)
        ],
    ]

    fake_http(FakeResponse({"timeline": timeline_data}))

    result = TOOL_FUNCTIONS["timeline"](
        screenname="testuser",
        limit=3,
    )

    assert len(result["items"]) == 3

    assert all(
        item["url"].startswith(
            "https://x.com/testuser/status/"
        )
        for item in result["items"]
    )


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    monkeypatch.setenv(
        "RAPIDAPI_TWITTER_HOST",
        "twitter-api45.p.rapidapi.com",
    )

    calls = fake_http(FakeResponse({"tweets": []}))

    TOOL_FUNCTIONS["social_search"](
        query="AI research",
        search_type="Top",
    )

    assert len(calls) == 1
    assert calls[0]["params"]["query"] == "AI research"
    assert calls[0]["params"]["search_type"] == "Top"


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    result = TOOL_FUNCTIONS["policy"](query="")

    assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    result = TOOL_FUNCTIONS["policy"](
        query="data privacy",
        policy_area="data_privacy",
    )

    assert len(result["results"]) > 0

    assert all(
        item["policy_area"] == "data_privacy"
        for item in result["results"]
    )



def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    result = TOOL_FUNCTIONS["policy"](
        query="injection",
        policy_area="source_citation",
    )

    assert len(result["results"]) > 0

    injection_found = False

    for item in result["results"]:
        untrusted = " ".join(item["untrusted_text"]).lower()
        facts = item["facts"].lower()

        if "ignore the citation policy" in untrusted:
            injection_found = True
            assert "ignore the citation policy" not in facts

    assert injection_found


    assert len(result["results"]) > 0

    injection_found = False

    for item in result["results"]:
        untrusted = " ".join(item["untrusted_text"]).lower()
        facts = item["facts"].lower()

        if "ignore the citation policy" in untrusted:
            injection_found = True
            assert "ignore the citation policy" not in facts

    assert injection_found


# ---------------- YOUR NEW TOOL(S) ----------------

def test_research_notes_happy_path(tmp_path, monkeypatch) -> None:
    from tools.research_notes import tool

    monkeypatch.setattr(
        tool,
        "NOTES_FILE",
        tmp_path / "notes.json",
    )

    result = tool.save_research_note(
        title="AI Research",
        content="Study about RAG",
        source="https://example.com",
        confirmed=True,
    )

    assert result["status"] == "saved"
    assert result["total_notes"] == 1
    assert result["note"]["title"] == "AI Research"


def test_research_notes_bad_input_from_model(tmp_path, monkeypatch) -> None:
    from tools.research_notes import tool

    monkeypatch.setattr(
        tool,
        "NOTES_FILE",
        tmp_path / "notes.json",
    )

    result = tool.save_research_note(
        title="",
        content="Some research",
        confirmed=True,
    )

    assert result["error"] == "ValueError"
    assert not (tmp_path / "notes.json").exists()


def test_research_notes_failure_returns_error_dict(tmp_path, monkeypatch) -> None:
    from tools.research_notes import tool

    notes_file = tmp_path / "notes.json"

    notes_file.write_text(
        "{invalid json",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        tool,
        "NOTES_FILE",
        notes_file,
    )

    result = tool.save_research_note(
        title="AI Research",
        content="Study about RAG",
        confirmed=True,
    )

    assert result["error"] == "JSONDecodeError"
    assert "message" in result
