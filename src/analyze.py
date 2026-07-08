from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

PROMPT = """이 오디오는 플룻 레슨에서 선생님이 준 음성 피드백입니다.
다음 작업을 수행하세요:
1) 오디오 전체 내용을 한국어로 정확히 받아쓰기합니다.
2) 받아쓴 내용을 바탕으로 아래를 정리합니다.
- key_feedback: 핵심 지적 사항 (2~4문장)
- practice_tasks: 다음 레슨까지 연습할 과제 (목록형 텍스트, 없으면 빈 문자열)
- did_well: 잘한 점/칭찬받은 점 (없으면 빈 문자열)
곡 이름은 추측하지 마세요. 오디오에 명확히 없으면 어디에도 넣지 마세요.
반드시 지정된 JSON 형식으로만 답하세요."""


def analyze_audio(file_path: str, api_key: str) -> dict[str, str]:
    """Analyze an audio file and return structured feedback."""
    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        uploaded = client.files.upload(file=file_path)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[uploaded, PROMPT],
            config={
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "object",
                    "properties": {
                        "transcript": {"type": "string"},
                        "key_feedback": {"type": "string"},
                        "practice_tasks": {"type": "string"},
                        "did_well": {"type": "string"},
                    },
                    "required": ["transcript", "key_feedback", "practice_tasks", "did_well"],
                },
            },
        )

        if hasattr(response, "text"):
            payload = response.text
        else:
            payload = response

        if isinstance(payload, str):
            import json

            parsed = json.loads(payload)
            return {
                "transcript": parsed.get("transcript", ""),
                "key_feedback": parsed.get("key_feedback", ""),
                "practice_tasks": parsed.get("practice_tasks", ""),
                "did_well": parsed.get("did_well", ""),
            }
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("Gemini analysis failed: %s", exc)

    return {
        "transcript": "",
        "key_feedback": "",
        "practice_tasks": "",
        "did_well": "",
    }
