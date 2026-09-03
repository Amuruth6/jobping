import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (JobPing Bot)"}


def try_greenhouse(token):
    url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            job_count = len(data.get("jobs", []))
            return job_count
    except requests.RequestException:
        pass
    return None


def try_lever(token):
    url = f"https://api.lever.co/v0/postings/{token}?mode=json"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return len(data)
    except requests.RequestException:
        pass
    return None


def check_company(name_variants):
    """Try several likely token spellings for a company name."""
    print(f"\nChecking possible tokens: {name_variants}")
    for token in name_variants:
        gh = try_greenhouse(token)
        if gh is not None:
            print(f"  ✅ Greenhouse match: '{token}' → {gh} jobs found")
        lv = try_lever(token)
        if lv is not None:
            print(f"  ✅ Lever match: '{token}' → {lv} jobs found")
        if gh is None and lv is None:
            print(f"  ❌ '{token}' — no match on either platform")


if __name__ == "__main__":
    # Add guesses for each company you want to check.
    # Try lowercase, no spaces, common suffixes like "inc", "technologies", etc.
    # Bangalore-based tech companies (larger, more likely to use Greenhouse/Lever)
    check_company(["freshworks"])       # Chennai-based, already tried, 0 jobs — try again later
    check_company(["zoho"])             # Chennai-based
    check_company(["chargebee"])        # Chennai-based
    check_company(["darwinbox"])
    check_company(["whatfix"])
    check_company(["clevertap"])
    check_company(["hasura"])
    check_company(["browserstack"])
    check_company(["postman"])          # already confirmed ✅
    check_company(["applied-ai", "appliedai"])
    check_company(["zluri"])
    check_company(["zenoti"])           # Chennai-based  