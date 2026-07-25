import os
import argparse

def generate_info_card(output_path: str):
    width = 490
    height = 370

    # Information specs
    specs = [
        ("OS", "Arch Linux x86_64 / macOS", "#79c0ff"),
        ("Host", "GitHub Profile Terminal v2.4", "#79c0ff"),
        ("Uptime", "99.98% (Continuous Integration)", "#79c0ff"),
        ("Shell", "zsh 5.9 (x86_64-apple-darwin22.0)", "#79c0ff"),
        ("Role", "Senior Full-Stack Engineer & Architect", "#ffa657"),
        ("Now", "Building animated SVG profile tools", "#a5d6ff"),
        ("Prev", "Distributed Systems Lead @ TechCorp", "#a5d6ff"),
        ("Stack", "Python, TypeScript, React, Go, Docker, K8s", "#d2a8ff"),
        ("Focus", "Web Performance, CLI Tools, Open Source", "#ff7b72"),
        ("Highlights", "9.3k+ Yearly Commits, 50+ PRs Merged", "#56d364"),
    ]

    lines_svg = []
    start_y = 75
    line_height = 26

    for idx, (key, val, val_color) in enumerate(specs):
        y_pos = start_y + (idx * line_height)
        delay = round(0.1 + (idx * 0.08), 2)

        lines_svg.append(f'''
    <g class="card-line" style="animation-delay: {delay}s;">
      <text x="30" y="{y_pos}" class="key-text">{key}:</text>
      <text x="130" y="{y_pos}" class="val-text" fill="{val_color}">{val}</text>
    </g>''')

    # Color palette bar (Neofetch signature bottom dots/blocks)
    colors = ["#ff7b72", "#ffa657", "#d2a8ff", "#79c0ff", "#56d364", "#e3b341"]
    color_blocks_svg = []
    block_x_start = 30
    block_y = start_y + (len(specs) * line_height) + 12

    for idx, col in enumerate(colors):
        x = block_x_start + (idx * 28)
        delay = round(0.1 + ((len(specs) + idx) * 0.08), 2)
        color_blocks_svg.append(f'''
    <rect x="{x}" y="{block_y}" width="22" height="12" rx="3" fill="{col}" class="card-line" style="animation-delay: {delay}s;" />''')

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; rx: 10px; }}
    .title-bar {{ fill: #161b22; rx: 10px; }}
    .dot-red {{ fill: #ff5f56; }}
    .dot-yellow {{ fill: #ffbd2e; }}
    .dot-green {{ fill: #27c93f; }}
    .title-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12px; fill: #8b949e; font-weight: bold; }}
    
    .key-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; fill: #58a6ff; font-weight: bold; }}
    .val-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 13px; font-weight: 500; }}

    .card-line {{
      opacity: 0;
      transform: translateY(8px);
      animation: fadeInSlide 0.4s ease-out forwards;
    }}

    @keyframes fadeInSlide {{
      0% {{
        opacity: 0;
        transform: translateY(8px);
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
  <path d="M 0,10 A 10,10 0 0,1 10,0 L {width-10},0 A 10,10 0 0,1 {width},10 L {width},36 L 0,36 Z" class="title-bar" />
  <circle cx="20" cy="18" r="5.5" class="dot-red" />
  <circle cx="36" cy="18" r="5.5" class="dot-yellow" />
  <circle cx="52" cy="18" r="5.5" class="dot-green" />
  <text x="{width/2}" y="22" text-anchor="middle" class="title-text">harshvangar2702-debug@github: ~ (neofetch)</text>

  <!-- Info Key-Value Rows -->
  {''.join(lines_svg)}

  <!-- Bottom Color Blocks -->
  {''.join(color_blocks_svg)}
</svg>
'''

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
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
