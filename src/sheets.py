from __future__ import annotations

from typing import Any

import gspread


HEADERS = ["날짜", "곡 이름", "핵심 피드백", "연습 과제", "잘한 점", "원본 전사"]


def get_worksheet(service_account_dict: dict[str, Any], sheet_id: str):
    """Open the first worksheet and ensure headers exist."""
    client = gspread.service_account_from_dict(service_account_dict)
    worksheet = client.open_by_key(sheet_id).sheet1

    if not worksheet.get("A1") or worksheet.get("A1") == [""]:
        worksheet.update([HEADERS], range_name="A1")

    return worksheet


def append_feedback_row(worksheet, date_str: str, result_dict: dict[str, str]) -> None:
    """Append a structured feedback row to the worksheet."""
    worksheet.append_row(
        [
            date_str,
            "",
            result_dict.get("key_feedback", ""),
            result_dict.get("practice_tasks", ""),
            result_dict.get("did_well", ""),
            result_dict.get("transcript", ""),
        ],
        value_input_option="USER_ENTERED",
    )
