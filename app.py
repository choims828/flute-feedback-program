from __future__ import annotations

from datetime import datetime
from pathlib import Path
import tempfile

import streamlit as st

from src.analyze import analyze_audio
from src.sheets import append_feedback_row, get_worksheet


st.set_page_config(page_title="🎵 플룻 레슨 피드백 정리", layout="centered")
st.title("🎵 플룻 레슨 피드백 정리")


def main() -> None:
    today = datetime.today().date()
    lesson_date = st.date_input("레슨 날짜", value=today)
    uploaded_file = st.file_uploader(
        "레슨 음원 업로드",
        type=["mp3", "m4a", "wav", "webm", "mp4", "aac", "ogg"],
    )

    if st.button("피드백 정리하기"):
        if uploaded_file is None:
            st.error("음원 파일을 먼저 업로드해 주세요.")
            return

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
                tmp.write(uploaded_file.getvalue())
                temp_path = tmp.name

            gemini_key = st.secrets["GEMINI_API_KEY"]
            sheet_id = st.secrets["SHEET_ID"]
            sa_dict = dict(st.secrets["gcp_service_account"])

            with st.spinner("음성 분석 및 정리 중..."):
                result = analyze_audio(temp_path, gemini_key)

            with st.spinner("구글 시트에 저장 중..."):
                worksheet = get_worksheet(sa_dict, sheet_id)
                append_feedback_row(worksheet, lesson_date.strftime("%Y-%m-%d"), result)

            st.success("저장 완료! 곡 이름은 시트에서 직접 채워주세요.")
            st.subheader("핵심 피드백")
            st.write(result.get("key_feedback", ""))
            st.subheader("연습 과제")
            st.write(result.get("practice_tasks", ""))
            st.subheader("잘한 점")
            st.write(result.get("did_well", ""))

            with st.expander("원본 전사 보기"):
                st.write(result.get("transcript", ""))

            st.markdown(f"[구글 시트 열기](https://docs.google.com/spreadsheets/d/{sheet_id}/edit)")
        except KeyError as exc:
            st.error(f"시크릿 설정이 누락되었습니다: {exc}")
        except Exception as exc:
            st.error(f"처리 중 오류가 발생했습니다: {exc}")


if __name__ == "__main__":
    main()
