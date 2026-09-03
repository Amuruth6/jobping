import requests


def send_telegram_message(bot_token: str, chat_id: str, message: str):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        resp = requests.post(url, data=payload, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Telegram send failed: {e}")


def format_digest(new_postings: list) -> str:
    if not new_postings:
        return None

    lines = ["<b>🔔 New job postings found:</b>\n"]
    for post in new_postings:
        lines.append(f"<b>{post['company']}</b>: {post['title']}\n{post['url']}\n")
    return "\n".join(lines)