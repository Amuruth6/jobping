import yaml
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

from database import init_db, is_new_posting, save_posting
from scraper import fetch_jobs_for_company
from notifier import send_telegram_message, format_digest

# add to top of main.py


logging.basicConfig(
    filename="jobping.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def matches_keywords(title: str, keywords: list) -> bool:
    title_lower = title.lower()
    return any(keyword.lower() in title_lower for keyword in keywords)


def run_check():
    print("Running job check...")
    config = load_config()
    companies = config["companies"]
    keywords = config["keywords"]
    telegram_cfg = config["telegram"]

    new_postings = []

    for company in companies:
        jobs = fetch_jobs_for_company(company)
        for job in jobs:
            if not matches_keywords(job["title"], keywords):
                continue
            if is_new_posting(job["id"]):
                save_posting(job["id"], company["name"], job["title"], job["url"])
                new_postings.append({
                    "company": company["name"],
                    "title": job["title"],
                    "url": job["url"],
                })

    if new_postings:
        message = format_digest(new_postings)
        send_telegram_message(telegram_cfg["bot_token"], telegram_cfg["chat_id"], message)
        print(f"Sent digest with {len(new_postings)} new postings.")
    else:
        print("No new postings found.")


if __name__ == "__main__":
    init_db()
    run_check()  # run once immediately on start

    config = load_config()
    interval = config.get("check_interval_hours", 24)

    scheduler = BlockingScheduler()
    scheduler.add_job(run_check, "interval", hours=interval)
    print(f"Scheduler started. Checking every {interval} hour(s). Press Ctrl+C to stop.")
    scheduler.start()