# whatsapp-bot examples

## Example 1 -- Verify webhook (GET)

Meta sends this GET to confirm your endpoint. Return `hub.challenge` as integer:

```python
@app.get("/whatsapp/webhook")
async def verify(mode: str = Query(alias="hub.mode"),
                 token: str = Query(alias="hub.verify_token"),
                 challenge: str = Query(alias="hub.challenge")):
    if mode == "subscribe" and hmac.compare_digest(token, os.environ["WHATSAPP_VERIFY_TOKEN"]):
        return int(challenge)
    raise HTTPException(status_code=403)
```

## Example 2 -- Send a text message

```bash
curl -X POST "https://graph.facebook.com/v18.0/${WHATSAPP_PHONE_NUMBER_ID}/messages" \
  -H "Authorization: Bearer ${WHATSAPP_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "+33600000000",
    "type": "text",
    "text": { "body": "Hello from the Cloud API!" }
  }'
```

## Example 3 -- Send interactive buttons (max 3)

```python
payload = {
    "messaging_product": "whatsapp",
    "to": "+33600000000",
    "type": "interactive",
    "interactive": {
        "type": "button",
        "body": {"text": "Do you want to continue?"},
        "action": {
            "buttons": [
                {"type": "reply", "reply": {"id": "yes", "title": "Yes"}},
                {"type": "reply", "reply": {"id": "no",  "title": "No"}},
            ]
        }
    }
}
```

## Example 4 -- Validate HMAC-SHA256 signature

```python
import hmac, hashlib

def validate(body: bytes, sig_header: str, app_secret: str) -> bool:
    expected = "sha256=" + hmac.new(app_secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig_header)
```
