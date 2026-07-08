import unittest
from unittest.mock import patch

from src.sheets import HEADERS, append_feedback_row, get_worksheet


class FakeWorksheet:
    def __init__(self):
        self.rows = []
        self.updated = []

    def get(self, range_name):
        if range_name == "A1":
            return []
        return []

    def update(self, values, range_name=None):
        self.updated.append((values, range_name))

    def append_row(self, values, value_input_option=None):
        self.rows.append((values, value_input_option))


class FakeClient:
    def __init__(self, worksheet):
        self.worksheet = worksheet

    def open_by_key(self, sheet_id):
        return type("Book", (), {"sheet1": self.worksheet})()


class SheetsTests(unittest.TestCase):
    def test_get_worksheet_initializes_headers(self):
        worksheet = FakeWorksheet()
        client = FakeClient(worksheet)

        with patch("src.sheets.gspread.service_account_from_dict", return_value=client):
            result = get_worksheet({"dummy": "value"}, "sheet-id")

        self.assertIs(result, worksheet)
        self.assertEqual(worksheet.updated[0][0], [HEADERS])

    def test_append_feedback_row_uses_expected_columns(self):
        worksheet = FakeWorksheet()
        result = {
            "key_feedback": "키 피드백",
            "practice_tasks": "연습 과제",
            "did_well": "잘한 점",
            "transcript": "전사 텍스트",
        }

        append_feedback_row(worksheet, "2026-07-08", result)

        self.assertEqual(
            worksheet.rows[0][0],
            ["2026-07-08", "", "키 피드백", "연습 과제", "잘한 점", "전사 텍스트"],
        )
        self.assertEqual(worksheet.rows[0][1], "USER_ENTERED")


if __name__ == "__main__":
    unittest.main()
