import os
import argparse

def generate_info_card(output_path: str):
    width = 490
    height = 370

    # Structured Neofetch content matching Avi Vashishta's layout
    lines = [
        ("user", "harshvangar2702-debug", "#58a6ff", True),
        ("Now", "Frontend & UI Specialist", "#79c0ff", False),
        ("Prev", "Web Application Engineer", "#79c0ff", False),
        ("Edu", "B.Tech in Computer Science", "#79c0ff", False),
        ("sep1", "-- Stack", "#8b949e", False),
        ("Frontend", "React, Next.js, TypeScript, Tailwind, CSS3", "#ffa657", False),
        ("Backend", "Node.js, Express, Python, REST APIs", "#a5d6ff", False),
        ("AI / ML", "LangChain, OpenAI API, Vercel AI SDK", "#d2a8ff", False),
        ("Cloud", "Vercel, Docker, Git, GitHub Actions", "#ff7b72", False),
        ("sep2", "-- Highlights", "#8b949e", False),
        ("hl1", "• Crafting pixel-perfect, responsive UI design systems", "#56d364", False),
        ("hl2", "• Building interactive animated web components & SVGs", "#56d364", False),
    ]

    lines_svg = []
    y_pos = 62
    line_spacing = 24

    for idx, (label, val, col, is_bold) in enumerate(lines):
        delay = round(0.08 + (idx * 0.06), 2)
        
        if label.startswith("sep"):
            # Section divider like "-- Stack" or "-- Highlights"
            lines_svg.append(f'''
    <g class="card-line" style="animation-delay: {delay}s;">
      <text x="25" y="{y_pos}" class="sep-text">{val}</text>
    </g>''')
            y_pos += 20
        elif label.startswith("hl"):
            # Bullet highlight line
            lines_svg.append(f'''
    <g class="card-line" style="animation-delay: {delay}s;">
      <text x="25" y="{y_pos}" class="hl-text" fill="{col}">{val}</text>
    </g>''')
            y_pos += 22
        elif label == "user":
            lines_svg.append(f'''
    <g class="card-line" style="animation-delay: {delay}s;">
      <text x="25" y="{y_pos}" class="user-text">{val}</text>
    </g>''')
            y_pos += 24
        else:
            # Standard Key: Value row
            lines_svg.append(f'''
    <g class="card-line" style="animation-delay: {delay}s;">
      <text x="25" y="{y_pos}" class="key-text">{label}</text>
      <text x="115" y="{y_pos}" class="val-text" fill="{col}">{val}</text>
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
    
    .user-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 15px; fill: #58a6ff; font-weight: bold; }}
    .key-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12px; fill: #ffa657; font-weight: bold; }}
    .val-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12px; font-weight: 500; }}
    .sep-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12px; fill: #8b949e; font-weight: bold; }}
    .hl-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 11.5px; font-weight: 500; }}

    .card-line {{
      opacity: 0;
      transform: translateY(6px);
      animation: fadeInSlide 0.35s ease-out forwards;
    }}

    @keyframes fadeInSlide {{
      0% {{
        opacity: 0;
        transform: translateY(6px);
      }}
      100% {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}
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
