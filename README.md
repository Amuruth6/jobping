# JobPing 🔔

An automated job-tracking bot I built for my own job search. Instead of manually
checking career pages on Razorpay, Postman, Zenoti, CRED, Meesho, Groww, Slice, and
RemoteOK every day, this script checks all of them on a schedule and sends me a
Telegram digest of new postings matching my target keywords.

## The problem
I was spending 65-120 minutes every morning opening 7+ career pages one by one,
scanning for anything new that matched roles I was targeting (Python, SDE, backend,
fresher). This automates that entire routine.

## How it works
1. Each company is checked via its ATS platform's public JSON API — Greenhouse or
   Lever — rather than scraping raw HTML.
2. Every posting title is matched against a configurable keyword list.
3. New matches are checked against a SQLite database to avoid repeat alerts.
4. Matched, new postings are sent as a single Telegram message.
5. The whole cycle repeats on a schedule (APScheduler, default: every 24 hours).

## Why JSON APIs instead of scraping
Greenhouse and Lever both expose clean public JSON endpoints for their job boards
(e.g. `boards-api.greenhouse.io/v1/boards/{token}/jobs`). Using these instead of
parsing HTML means the tool doesn't break every time a company redesigns their
careers page — HTML scraping is fragile by nature.

RemoteOK was the one exception that revealed something useful: it initially looked
like it needed HTML scraping (their job listings are loaded via JavaScript, so
`requests` couldn't see them in the raw page source). Before writing a scraper for
it, I checked whether RemoteOK exposed a JSON feed of its own — it does
(`remoteok.com/api`) — so I used that instead. Worth checking for an API before
reaching for BeautifulSoup, even on sites that don't obviously advertise one.

## A real bug I hit and how I fixed it
My first attempt used guessed board tokens (`razorpay`, `zerodha`) and got 404s from
both. Rather than keep guessing, I wrote `find_company_token.py`, a small script that
tests a list of candidate token spellings against both the Greenhouse and Lever APIs
and reports which ones actually resolve, and how many jobs each returns. That's how
I found the real token for Razorpay (`razorpaysoftwareprivatelimited`) and confirmed
Zerodha isn't on either platform at all — it uses a custom in-house careers site.

## Companies currently tracked
| Company | Platform |
|---|---|
| Razorpay | Greenhouse |
| Postman | Greenhouse |
| Zenoti | Greenhouse |
| Slice | Greenhouse |
| CRED | Lever |
| Meesho | Lever |
| RemoteOK | Native JSON API |

## Tech stack
Python · SQLite · Telegram Bot API · APScheduler · Requests · PyYAML

## Setup
```bash
pip install -r requirements.txt
cp config.example.yaml config.yaml
# edit config.yaml with your Telegram bot token, chat ID, and target companies
python main.py
```

To find working board tokens for other companies:
```bash
python find_company_token.py
```

## Known limitations
- Only supports companies on Greenhouse, Lever, or RemoteOK. Many companies —
  especially regional or smaller ones — run custom career sites that would need
  their own scraper per site.
- No retry logic on transient network failures yet; a failed check is simply
  skipped until the next scheduled run.
- Keyword matching is currently substring-based (case-insensitive), not fuzzy —
  a role titled "Pythonista" wouldn't match a "python" keyword, for example.

## Possible next steps
- Add HTML-scraping support for a couple of custom career sites
- Add retry-with-backoff for failed requests
- Small web dashboard to browse alert history instead of only Telegram
