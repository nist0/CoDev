---
name: whatsapp-bot
description: Build WhatsApp bots using the WhatsApp Business Cloud API (Meta). Covers webhook verification, HMAC-SHA256 signature validation, message types (text, template, interactive), Python and C# outbound patterns, and deployment checklist.
argument-hint: "[language: python|csharp] [feature: webhook|templates|interactive|media]"

user-invocable: true
---

# WhatsApp Bot Development (Cloud API)

## When to use

- Sending and receiving WhatsApp messages via the Meta Cloud API.

- Implementing inbound webhook verification and payload routing.

- Sending template messages, interactive button/list messages, or media.

- Integrating WhatsApp into a multi-channel bot strategy.

## Prerequisites

- Meta for Developers account at `developers.facebook.com`.

- WhatsApp Business App created and connected.

- Verified phone number (sandbox available during development).

- `WHATSAPP_ACCESS_TOKEN` and `WHATSAPP_PHONE_NUMBER_ID` stored in secrets/env.

- `WHATSAPP_VERIFY_TOKEN` and `WHATSAPP_APP_SECRET` for webhook security.

## Cloud API overview

```text
User --> WhatsApp --> Meta Cloud --> HTTPS POST --> Your webhook
Your bot --> POST /messages --> Meta Cloud --> WhatsApp --> User
```

Base URL: `https://graph.facebook.com/v18.0/{phone_number_id}/messages`

## Step 1 -- Webhook setup (GET verification)

Meta sends a GET to verify your webhook. Respond with `hub.challenge`:

```python
# Python / FastAPI
from fastapi import FastAPI, Request, HTTPException, Query

VERIFY_TOKEN: str = os.environ["WHATSAPP_VERIFY_TOKEN"]

@app.get("/whatsapp/webhook")
async def verify_webhook(
    mode:      str = Query(alias="hub.mode"),
    token:     str = Query(alias="hub.verify_token"),
    challenge: str = Query(alias="hub.challenge"),
):
    if mode == "subscribe" and hmac.compare_digest(token, VERIFY_TOKEN):
        return int(challenge)  # must return challenge as integer
    raise HTTPException(status_code=403, detail="Verification failed")
```

```csharp
// C# / ASP.NET Core
[HttpGet("webhook")]
public IActionResult VerifyWebhook(
    [FromQuery(Name = "hub.mode")]         string mode,
    [FromQuery(Name = "hub.verify_token")] string token,
    [FromQuery(Name = "hub.challenge")]    string challenge)
{
    var expected = _config["WhatsApp:VerifyToken"]
        ?? throw new InvalidOperationException("VerifyToken not configured");

    if (mode == "subscribe" && CryptographicOperations.FixedTimeEquals(
            System.Text.Encoding.UTF8.GetBytes(token),
            System.Text.Encoding.UTF8.GetBytes(expected)))
    {
        return Ok(int.Parse(challenge));
    }
    return StatusCode(403);
}
```

## Step 2 -- Webhook signature validation (POST)

Every inbound POST includes `X-Hub-Signature-256: sha256=<HMAC>` computed with the App Secret:

```python
import hmac
import hashlib

APP_SECRET: str = os.environ["WHATSAPP_APP_SECRET"]


def validate_signature(body: bytes, signature_header: str) -> bool:
    """Constant-time HMAC-SHA256 comparison."""
    if not signature_header.startswith("sha256="):
        return False
    expected = "sha256=" + hmac.new(
        APP_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature_header)


@app.post("/whatsapp/webhook")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks):
    body_bytes = await request.body()
    sig = request.headers.get("X-Hub-Signature-256", "")

    if not validate_signature(body_bytes, sig):
        raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()
    background_tasks.add_task(process_whatsapp_update, payload)
    return {"status": "ok"}  # always 200 OK to Meta
```

```csharp
[HttpPost("webhook")]
public async Task<IActionResult> ReceiveWebhook()
{
    using var reader = new StreamReader(Request.Body);
    var bodyText = await reader.ReadToEndAsync();
    var bodyBytes = System.Text.Encoding.UTF8.GetBytes(bodyText);

    var sigHeader  = Request.Headers["X-Hub-Signature-256"].ToString();
    var appSecret  = _config["WhatsApp:AppSecret"]
        ?? throw new InvalidOperationException("AppSecret not configured");

    using var hmac = new HMACSHA256(System.Text.Encoding.UTF8.GetBytes(appSecret));
    var computed = "sha256=" + Convert.ToHexString(hmac.ComputeHash(bodyBytes)).ToLower();

    if (!CryptographicOperations.FixedTimeEquals(
            System.Text.Encoding.UTF8.GetBytes(computed),
            System.Text.Encoding.UTF8.GetBytes(sigHeader)))
        return StatusCode(403);

    // process asynchronously -- return 200 immediately
    _ = Task.Run(() => ProcessUpdateAsync(bodyText));
    return Ok();
}
```

## Step 3 -- Parse incoming message

```python
def process_whatsapp_update(payload: dict) -> None:
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            messages = value.get("messages", [])
            for message in messages:
                msg_type = message.get("type")
                sender   = message["from"]  # phone number in E.164 format

                if msg_type == "text":
                    text = message["text"]["body"]
                    handle_text(sender, text)
                elif msg_type == "interactive":
                    interactive_type = message["interactive"]["type"]
                    if interactive_type == "button_reply":
                        button_id = message["interactive"]["button_reply"]["id"]
                        handle_button(sender, button_id)
                    elif interactive_type == "list_reply":
                        item_id = message["interactive"]["list_reply"]["id"]
                        handle_list_item(sender, item_id)
                elif msg_type == "image":
                    media_id = message["image"]["id"]
                    handle_image(sender, media_id)
```

## Step 4 -- Send messages (outbound)

```python
import httpx
import os

ACCESS_TOKEN:     str = os.environ["WHATSAPP_ACCESS_TOKEN"]
PHONE_NUMBER_ID:  str = os.environ["WHATSAPP_PHONE_NUMBER_ID"]
API_VERSION:      str = "v18.0"
BASE_URL:         str = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type":  "application/json",
}


async def send_text(to: str, body: str) -> dict:
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type":    "individual",
        "to":                to,
        "type":              "text",
        "text":              {"body": body, "preview_url": False},
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(BASE_URL, headers=HEADERS, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()


async def send_interactive_buttons(to: str, body_text: str, buttons: list[dict]) -> dict:
    """
    buttons: [{"id": "btn_1", "title": "Yes"}, {"id": "btn_2", "title": "No"}]
    Max 3 buttons.
    """
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type":    "individual",
        "to":                to,
        "type":              "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": body_text},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": b["id"], "title": b["title"]}}
                    for b in buttons
                ]
            },
        },
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(BASE_URL, headers=HEADERS, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()
```

```csharp
// C# outbound helper
public async Task SendTextAsync(string to, string body, CancellationToken ct = default)
{
    var payload = new
    {
        messaging_product = "whatsapp",
        recipient_type    = "individual",
        to,
        type = "text",
        text = new { body, preview_url = false }
    };

    var response = await _httpClient.PostAsJsonAsync(
        $"https://graph.facebook.com/v18.0/{_phoneNumberId}/messages",
        payload, ct);

    response.EnsureSuccessStatusCode();
}
```

## Step 5 -- Template messages (HSM)

Templates must be pre-approved by Meta in the WhatsApp Manager:

```python
async def send_template(to: str, template_name: str, lang_code: str = "en_US") -> dict:
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name":     template_name,
            "language": {"code": lang_code},
        },
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(BASE_URL, headers=HEADERS, json=payload, timeout=10)
        r.raise_for_status()
        return r.json()
```

## Step 6 -- Testing

```python
import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_send_text_success():
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.return_value = AsyncMock(
            status_code=200,
            json=lambda: {"messages": [{"id": "wamid.xxx"}]}
        )
        result = await send_text("+1234567890", "Hello")
        assert "messages" in result
```

## Self-check

- [ ] `WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_APP_SECRET`, `WHATSAPP_VERIFY_TOKEN` all loaded from env/secrets.

- [ ] GET verification endpoint returns `hub.challenge` using constant-time comparison.

- [ ] POST webhook validates `X-Hub-Signature-256` before any payload parsing.

- [ ] Webhook always returns 200 OK; processing dispatched asynchronously.

- [ ] `hmac.compare_digest` / `CryptographicOperations.FixedTimeEquals` used (no timing attack).

- [ ] Template names and components match Meta-approved template exactly.

- [ ] Interactive button replies limited to max 3 buttons.

- [ ] Access token refreshed via Meta token refresh flow (not hardcoded long-lived token).

## Outputs

- Webhook endpoint with GET verification and POST signature validation.

- Outbound helpers for text, templates, and interactive messages.

- Integration test stubs for outbound calls.
