
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


NOTES_FILE = Path(__file__).with_name("notes.json")


def save_research_note(
    title: str = "",
    content: str = "",
    source: str = "",
    confirmed: bool = False,
) -> dict[str, Any]:
    # 1. Kiểm tra dữ liệu đầu vào
    if not isinstance(title, str) or not title.strip():
        return {"error": "ValueError", "message": "Title must not be empty."}

    if not isinstance(content, str) or not content.strip():
        return {"error": "ValueError", "message": "Content must not be empty."}

    if not isinstance(source, str):
        return {"error": "ValueError", "message": "Source must be a string."}

    # 2. Yêu cầu xác nhận trước khi ghi file
    if not confirmed:
        return {
            "status": "needs_confirmation",
            "message": "Please confirm before saving this note.",
        }

    # 3. Tạo dữ liệu ghi chú
    note = {
        "title": title.strip(),
        "content": content.strip(),
        "source": source.strip(),
    }

    try:
        # 4. Đọc ghi chú cũ nếu file đã tồn tại
        if NOTES_FILE.exists():
            with NOTES_FILE.open("r", encoding="utf-8") as file:
                notes = json.load(file)
        else:
            notes = []

        if not isinstance(notes, list):
            return {"error": "ValueError", "message": "Notes file must contain a JSON list."}

        # 5. Thêm ghi chú mới và lưu lại
        notes.append(note)

        with NOTES_FILE.open("w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False, indent=2)

        return {
            "tool": "save_research_note",
            "status": "saved",
            "note": note,
            "total_notes": len(notes),
        }

    except (OSError, json.JSONDecodeError) as error:
        return {
            "error": type(error).__name__,
            "message": str(error),
        }
