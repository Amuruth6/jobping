import yaml
from scraper import fetch_greenhouse_jobs, fetch_remoteok_jobs
from database import init_db, is_new_posting, save_posting
from notifier import send_telegram_message

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

print("--- Greenhouse ---")
jobs = fetch_greenhouse_jobs("razorpaysoftwareprivatelimited")
print(f"Found {len(jobs)} jobs")
print(jobs[:2])

print("--- RemoteOK ---")
jobs = fetch_remoteok_jobs()
print(f"Found {len(jobs)} jobs")
print(jobs[:2])

print("--- Database ---")
init_db()
print(is_new_posting("test123"))
save_posting("test123", "TestCo", "Test Job", "http://example.com")
print(is_new_posting("test123"))

print("--- Telegram ---")
telegram_cfg = config["telegram"]
send_telegram_message(telegram_cfg["bot_token"], telegram_cfg["chat_id"], "Test message from JobPing 🚀")