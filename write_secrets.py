from pathlib import Path
import json

json_path = Path('delta-transit-468206-u4-f7b058b13346.json')
secrets_path = Path('.streamlit/secrets.toml')
data = json.loads(json_path.read_text(encoding='utf-8'))
content = f'''# 로컬 테스트용 예시입니다. 실제 값으로 교체하세요.
GEMINI_API_KEY = "AQ.Ab8RN6Jp22FjwpyIjCSlqkqzmwW34OMzF8IiZXMKF19BB7yH_Q"
SHEET_ID = "1A2PBdv23dc29liE7kVcH7uTaRstybCstJIGdtLvvLbs"

[gcp_service_account]
type = "{data['type']}"
project_id = "{data['project_id']}"
private_key_id = "{data['private_key_id']}"
private_key = """{data['private_key']}"""
client_email = "{data['client_email']}"
client_id = "{data['client_id']}"
auth_uri = "{data['auth_uri']}"
token_uri = "{data['token_uri']}"
auth_provider_x509_cert_url = "{data['auth_provider_x509_cert_url']}"
client_x509_cert_url = "{data['client_x509_cert_url']}"
universe_domain = "{data['universe_domain']}"
'''
secrets_path.write_text(content, encoding='utf-8')
print(secrets_path)
