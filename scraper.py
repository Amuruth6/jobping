import requests

from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (JobPing Bot)"}



def fetch_greenhouse_jobs(board_token: str):
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        jobs = []
        for job in data.get("jobs", []):
            try:
                jobs.append({
                    "id": f"greenhouse_{job['id']}",
                    "title": job["title"],
                    "url": job["absolute_url"],
                })
            except KeyError as e:
                print(f"[WARN] Skipping malformed job entry from {board_token}: missing {e}")
                continue
        return jobs
    except requests.RequestException as e:
        print(f"[ERROR] Greenhouse fetch failed for {board_token}: {e}")
        return []
    except ValueError as e:  # bad JSON
        print(f"[ERROR] Greenhouse returned invalid JSON for {board_token}: {e}")
        return []


def fetch_lever_jobs(board_token):
    """Lever also exposes a public JSON API."""
    url = f"https://api.lever.co/v0/postings/{board_token}?mode=json"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        jobs = []
        for job in data:
            try:
                jobs.append({
                    "id": f"lever_{job['id']}",
                    "title": job["text"],
                    "url": job["hostedUrl"],
                })
            except KeyError as e:
                print(f"[WARN] Skipping malformed job entry from {board_token}: missing {e}")
                continue
        return jobs
    except requests.RequestException as e:
        print(f"[ERROR] Lever fetch failed for {board_token}: {e}")
        return []
    except ValueError as e:  # bad JSON
        print(f"[ERROR] Lever returned invalid JSON for {board_token}: {e}")
        return []


def fetch_jobs_for_company(company: dict):
    platform = company["platform"].lower()
    token = company.get("board_token")

    if platform == "greenhouse":
        return fetch_greenhouse_jobs(token)
    elif platform == "lever":
        return fetch_lever_jobs(token)
    elif platform == "remoteok":
        return fetch_remoteok_jobs()
    else:
        print(f"[WARN] Unsupported platform '{platform}' for {company['name']}")
        return []
    

def fetch_remoteok_jobs():
    """RemoteOK exposes a free public JSON API — no HTML parsing needed."""
    url = "https://remoteok.com/api"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        jobs = []
        # The first item in RemoteOK's response is always a legal/metadata notice, not a job
        for entry in data[1:]:
            try:
                jobs.append({
                    "id": f"remoteok_{entry['id']}",
                    "title": entry["position"],
                    "url": entry["url"],
                })
            except KeyError as e:
                print(f"[WARN] Skipping malformed RemoteOK entry: missing {e}")
                continue
        return jobs
    except requests.RequestException as e:
        print(f"[ERROR] RemoteOK fetch failed: {e}")
        return []
    except ValueError as e:
        print(f"[ERROR] RemoteOK returned invalid JSON: {e}")
        return []