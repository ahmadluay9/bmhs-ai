# 1. Contoh Agent Card
```json
{
  "capabilities": {

  },
  "defaultInputModes": [
    "text/plain"
  ],
  "defaultOutputModes": [
    "text/plain"
  ],
  "description": "Agen ini berfungsi sebagai .",
  "name": "root_agent",
  "preferredTransport": "JSONRPC",
  "protocolVersion": "0.3.0",
  "skills": [
    {
      "description": "Agen ini berfungsi sebagai  ",
      "examples": [],
      "id": "root_agent",
      "name": "model",
      "tags": [
        "llm"
      ]
    }
  ],
  "supportsAuthenticatedExtendedCard": false,
  "url": "http://localhost:8001",
  "version": "0.0.1"
}

```

# 2. Tambahkan fitur autentikasi oauth2.0
```json
{
  "capabilities": {

  },
  "defaultInputModes": [
    "text/plain"
  ],
  "defaultOutputModes": [
    "text/plain"
  ],
  "description": "Agen ini berfungsi sebagai ...",
  "name": "agent_name",
  "preferredTransport": "JSONRPC",
  "protocolVersion": "0.3.0",
  "security": [
    {
      "bmhs_ai_oauth": [
        "openid",
        "email",
        "profile"
      ]
    }
  ],
  "securitySchemes": {
    "bmhs_ai_oauth": {
      "description": "Google Authentication",
      "flows": {
        "authorizationCode": {
          "authorizationUrl": "https://accounts.google.com/o/oauth2/auth?access_type=offline&prompt=consent",
          "scopes": {
            "openid": "Authenticate using your Google account",
            "email": "View your email address",
            "profile": "View basic profile information"
          },
          "tokenUrl": "https://oauth2.googleapis.com/token"
        }
      },
      "type": "oauth2"
    }
  },
  "skills": [
    {
      "description": "Agen ini berfungsi sebagai ...    ",
      "examples": [],
      "id": "agent_name",
      "name": "model",
      "tags": [
        "llm"
      ]
    }
  ],
  "supportsAuthenticatedExtendedCard": false,
  "url": "CLOUD_RUN_A2A_URL",
  "version": "0.0.1"
}
```