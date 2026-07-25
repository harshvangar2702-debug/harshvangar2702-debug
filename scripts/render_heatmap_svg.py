import os
import json
import argparse
from datetime import datetime

PALETTE = [
    "#161b22",  # Level 0 (None)
    "#0e4429",  # Level 1
    "#006d32",  # Level 2
    "#26a641",  # Level 3
    "#39d353",  # Level 4
    "#69f0a0"   # Level 5 (High intensity top end)
]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAY_NAMES = ["Mon", "", "Wed", "", "Fri", ""]

def render_svg(data_path: str, output_path: str):
    if not os.path.exists(data_path):
        print(f"[!] File not found: {data_path}. Run fetch_contributions.py first.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)

    # Grid specifications
    cell_size = 11
    cell_gap = 4
    step = cell_size + cell_gap
    offset_x = 40
    offset_y = 35

    # Group days by week columns (up to 53 weeks)
    weeks = []
    current_week = []

    for d in days:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        wday = dt.weekday()  # Mon=0, Sun=6 (GitHub calendar: Sun=0 to Sat=6 or Mon=0)
        
        current_week.append(d)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
            
    if current_week:
        weeks.append(current_week)

    width = offset_x + (len(weeks) * step) + 20
    height = offset_y + (7 * step) + 40

    # Build Month labels
    month_labels_svg = []
    last_month = -1
    for w_idx, week in enumerate(weeks):
        if week:
            dt = datetime.strptime(week[0]["date"], "%Y-%m-%d")
            if dt.month != last_month:
                last_month = dt.month
                x_pos = offset_x + (w_idx * step)
                month_labels_svg.append(
                    f'<text x="{x_pos}" y="22" class="label">{MONTH_NAMES[dt.month - 1]}</text>'
                )

    # Build Day labels (Mon, Wed, Fri)
    day_labels_svg = []
    for d_idx, day_name in enumerate(["Mon", "Wed", "Fri"]):
        if day_name:
            y_pos = offset_y + ((d_idx * 2 + 1) * step) - 3
            day_labels_svg.append(
                f'<text x="12" y="{y_pos}" class="label">{day_name}</text>'
            )

    # Build Rectangles with diagonal CSS animation delays
    rects_svg = []
    for w_idx, week in enumerate(weeks):
        for d_idx, day in enumerate(week):
            level = min(day.get("level", 0), len(PALETTE) - 1)
            color = PALETTE[level]
            x_pos = offset_x + (w_idx * step)
            y_pos = offset_y + (d_idx * step)
            count = day.get("count", 0)
            date_str = day.get("date", "")
            
            # Stagger delay diagonally (column + row index)
            delay = round((w_idx + d_idx) * 0.02, 3)
            
            rects_svg.append(
                f'<rect x="{x_pos}" y="{y_pos}" width="{cell_size}" height="{cell_size}" rx="2" ry="2" '
                f'fill="{color}" class="day-box" style="animation-delay: {delay}s;">'
                f'<title>{count} contributions on {date_str}</title>'
                f'</rect>'
            )

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .bg {{ fill: #0d1117; rx: 8px; }}
    .title {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; fill: #58a6ff; font-weight: bold; }}
    .label {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 10px; fill: #8b949e; }}
    .stats {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 11px; fill: #c9d1d9; }}
    .accent {{ fill: #39d353; font-weight: bold; }}

    .day-box {{
      opacity: 0;
      transform-origin: center;
      animation: reveal 0.4s ease-out forwards;
    }}

    @keyframes reveal {{
      0% {{
        opacity: 0;
        transform: scale(0.3);
      }}
      100% {{
        opacity: 1;
        transform: scale(1);
      }}
    }}
  </style>

  <!-- Background container -->
  <rect width="100%" height="100%" class="bg" />

  <!-- Month Header Labels -->
  {''.join(month_labels_svg)}

  <!-- Day Sidebar Labels -->
  {''.join(day_labels_svg)}

  <!-- Heatmap Boxes -->
  <g>
    {''.join(rects_svg)}
  </g>

  <!-- Footer Stats -->
  <g transform="translate({offset_x}, {height - 15})">
    <text x="0" y="0" class="stats">
      <tspan class="accent">{total_contribs:,}</tspan> contributions in the last year
      <tspan fill="#8b949e"> • </tspan>
      Streak: <tspan class="accent">{current_streak} days</tspan> (Best: {longest_streak} days)
    </text>
  </g>

  <!-- Legend -->
  <g transform="translate({width - 130}, {height - 23})">
    <text x="0" y="9" class="label">Less</text>
    <rect x="30" y="0" width="10" height="10" rx="2" fill="{PALETTE[0]}" />
    <rect x="43" y="0" width="10" height="10" rx="2" fill="{PALETTE[1]}" />
    <rect x="56" y="0" width="10" height="10" rx="2" fill="{PALETTE[2]}" />
    <rect x="69" y="0" width="10" height="10" rx="2" fill="{PALETTE[3]}" />
    <rect x="82" y="0" width="10" height="10" rx="2" fill="{PALETTE[4]}" />
    <text x="98" y="9" class="label">More</text>
  </g>
</svg>
'''

    if os.path.dirname(output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"[+] Generated heatmap SVG at {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Render SVG contribution heatmap.")
    parser.add_argument("--input", type=str, default="data/contributions.json", help="Input JSON path")
    parser.add_argument("--output", type=str, default="contrib-heatmap.svg", help="Output SVG path")
    args = parser.parse_args()

    render_svg(args.input, args.output)

if __name__ == "__main__":
    main()
