import os
import argparse

def generate_info_card(output_path: str):
    width = 490
    height = 370

    # Real profile details extracted from Harsh Vangar's LinkedIn profile
    lines = [
        ("user", "Harsh Vangar (harshvangar2702-debug)", "#58a6ff", True),
        ("Now", "Full-Stack Developer @ Tech Surya IT Solutions", "#79c0ff", False),
        ("Focus", "UI/UX Design & User-Centric Web Experiences", "#79c0ff", False),
        ("Edu", "CS Diploma, MSBTE Maharashtra", "#79c0ff", False),
        ("sep1", "-- Stack & Skills", "#8b949e", False),
        ("Frontend", "React.js, JavaScript, HTML5/CSS3, UI/UX Design", "#ffa657", False),
        ("Backend", "Python, Node.js, RESTful APIs, SQL", "#a5d6ff", False),
        ("Projects", "AirCanvas (Gesture AI), SIH Hackathon App", "#d2a8ff", False),
        ("Tools", "Figma, Git, GitHub Actions, VS Code", "#ff7b72", False),
        ("sep2", "-- Highlights & Achievements", "#8b949e", False),
        ("hl1", "• Winner/Participant: Smart India Hackathon (SIH 2023)", "#56d364", False),
        ("hl2", "• Built AirCanvas (Vision Pro inspired AI gesture drawing)", "#56d364", False),
    ]

    lines_svg = []
    y_pos = 60
    line_spacing = 24

    for idx, (label, val, col, is_bold) in enumerate(lines):
        if label.startswith("sep"):
            lines_svg.append(f'''
    <g>
      <text x="22" y="{y_pos}" class="sep-text">{val}</text>
    </g>''')
            y_pos += 20
        elif label.startswith("hl"):
            lines_svg.append(f'''
    <g>
      <text x="22" y="{y_pos}" class="hl-text" fill="{col}">{val}</text>
    </g>''')
            y_pos += 22
        elif label == "user":
            lines_svg.append(f'''
    <g>
      <text x="22" y="{y_pos}" class="user-text">{val}</text>
    </g>''')
            y_pos += 24
        else:
            lines_svg.append(f'''
    <g>
      <text x="22" y="{y_pos}" class="key-text">{label}</text>
      <text x="110" y="{y_pos}" class="val-text" fill="{col}">{val}</text>
    </g>''')
            y_pos += line_spacing

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; rx: 10px; }}
    .title-bar {{ fill: #161b22; rx: 10px; }}
    .dot-red {{ fill: #ff5f56; }}
    .dot-yellow {{ fill: #ffbd2e; }}
    .dot-green {{ fill: #27c93f; }}
    .title-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 11px; fill: #8b949e; font-weight: bold; }}
    
    .user-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 14px; fill: #58a6ff; font-weight: bold; }}
    .key-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12px; fill: #ffa657; font-weight: bold; }}
    .val-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 11.5px; font-weight: 500; }}
    .sep-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 11.5px; fill: #8b949e; font-weight: bold; }}
    .hl-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 11px; font-weight: 500; }}
  </style>

  <!-- Container Box -->
  <rect width="100%" height="100%" class="bg" />

  <!-- Terminal Title Bar -->
  <path d="M 0,10 A 10,10 0 0,1 10,0 L {width-10},0 A 10,10 0 0,1 {width},10 L {width},32 L 0,32 Z" class="title-bar" />
  <circle cx="18" cy="16" r="4.5" class="dot-red" />
  <circle cx="32" cy="16" r="4.5" class="dot-yellow" />
  <circle cx="46" cy="16" r="4.5" class="dot-green" />
  <text x="{width/2}" y="20" text-anchor="middle" class="title-text">harshvangar2702-debug@github: ~$ neofetch</text>

  <!-- Lines -->
  {''.join(lines_svg)}
</svg>
'''

    if os.path.dirname(output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"[+] Generated Neofetch info card SVG at {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate Neofetch SVG info card.")
    parser.add_argument("--output", type=str, default="info-card.svg", help="Output SVG path")
    args = parser.parse_args()

    generate_info_card(args.output)

if __name__ == "__main__":
    main()
