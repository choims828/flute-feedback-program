# 플룻 레슨 피드백 정리 앱

이 앱은 음성 피드백 파일을 업로드하면 Gemini로 전사와 피드백 정리를 수행한 뒤, Google Sheets에 한 줄씩 저장하는 Streamlit 웹앱입니다.

## 준비 사항

1. Gemini API 키 발급
   - https://aistudio.google.com/
   - "Get API key"로 API 키를 발급합니다.
2. Google Cloud에서 서비스 계정 생성
   - Google Sheets API, Google Drive API를 활성화합니다.
   - 서비스 계정 생성 후 JSON 키를 다운로드합니다.
   - 저장할 Google Sheet를 만들고, 서비스 계정 이메일에 편집자 권한을 부여합니다.
3. Sheet ID 확인
   - Google Sheet URL에서 `SHEET_ID`를 추출합니다.

## 로컬 실행

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

`.streamlit/secrets.toml` 파일을 만들고 아래 형식으로 입력합니다.

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
SHEET_ID = "YOUR_SHEET_ID"

[gcp_service_account]
type = "service_account"
project_id = "YOUR_PROJECT_ID"
private_key_id = "YOUR_PRIVATE_KEY_ID"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
client_email = "YOUR_SERVICE_ACCOUNT_EMAIL"
client_id = "YOUR_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "YOUR_CLIENT_X509_CERT_URL"
```

실행:

```bash
streamlit run app.py
```

## 배포

- GitHub 저장소에 업로드합니다.
- Streamlit Community Cloud에서 저장소를 연결합니다.
- Settings > Secrets에 동일한 `.streamlit/secrets.toml` 내용을 붙여 넣습니다.
