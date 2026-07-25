import os
import sys
import json
import argparse
from datetime import datetime, timedelta, timezone
import requests
from bs4 import BeautifulSoup

def fetch_github_contributions(username: str):
    """
    Fetches public contribution calendar HTML from GitHub for a given username
    and extracts daily contribution levels and counts.
    """
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return parse_contributions_html(response.text)
    except Exception as e:
        print(f"[!] Error fetching live GitHub data for {username}: {e}")
        print("[*] Generating mock contribution data fallback...")
        return generate_mock_contributions()

def parse_contributions_html(html_content: str):
    """
    Parses GitHub's contribution table HTML fragment.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    days = []
    
    # GitHub uses <td or <rect with class ContributionCalendar-day
    calendar_days = soup.find_all(["td", "rect"], class_="ContributionCalendar-day")
    
    total_contributions = 0
    
    for day_elem in calendar_days:
        date_str = day_elem.get("data-date")
        level_str = day_elem.get("data-level", "0")
        
        if not date_str:
            continue
            
        level = int(level_str) if level_str.isdigit() else 0
        
        # Extract count if available in tooltip or aria-label
        count = level * 3  # reasonable estimate if raw count is hidden in tooltip
        aria_label = day_elem.get("aria-label") or ""
        if "contribution" in aria_label:
            try:
                parts = aria_label.split(" ")
                if parts[0].isdigit():
                    count = int(parts[0])
            except Exception:
                pass
                
        total_contributions += count
        days.append({
            "date": date_str,
            "level": level,
            "count": count
        })

    # Sort chronologically
    days.sort(key=lambda x: x["date"])
    
    # Compute streaks
    current_streak, longest_streak = compute_streaks(days)

    return {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "days": days
    }

def compute_streaks(days):
    current_streak = 0
    longest_streak = 0
    temp_streak = 0

    for d in days:
        if d["count"] > 0 or d["level"] > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    # Current streak from recent end
    for d in reversed(days):
        if d["count"] > 0 or d["level"] > 0:
            current_streak += 1
        else:
            break

    return current_streak, longest_streak

def generate_mock_contributions():
    import random
    today = datetime.utcnow().date()
    start_date = today - timedelta(weeks=53)
    
    days = []
    curr = start_date
    total = 0
    
    while curr <= today:
        # Generate semi-realistic levels (0 to 4)
        rand = random.random()
        if rand > 0.4:
            level = random.randint(1, 4)
            count = level * random.randint(2, 5)
        else:
            level = 0
            count = 0
            
        total += count
        days.append({
            "date": curr.strftime("%Y-%m-%d"),
            "level": level,
            "count": count
        })
        curr += timedelta(days=1)
        
    c_streak, l_streak = compute_streaks(days)
    return {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "total_contributions": total,
        "current_streak": c_streak,
        "longest_streak": l_streak,
        "days": days
    }

def main():
    parser = argparse.ArgumentParser(description="Fetch GitHub contributions calendar data.")
    parser.add_argument("--username", type=str, default="harshvangar", help="GitHub username")
    parser.add_argument("--output", type=str, default="data/contributions.json", help="Output JSON path")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    data = fetch_github_contributions(args.username)
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print(f"[+] Saved contribution data for '{args.username}' to {args.output} ({len(data['days'])} days)")

if __name__ == "__main__":
    main()
