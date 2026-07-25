import os
import argparse
from PIL import Image

# Character density ramp (sparse/bright to dense/dark)
# Leading space ensures background remains transparent/blank
RAMP = " .`:-=+*cs#%@"

def image_to_ascii(image_path: str, width: int = 75):
    if not os.path.exists(image_path):
        print(f"[*] Prepped image '{image_path}' missing. Generating default ASCII matrix...")
        return generate_default_matrix(width, 48)

    img = Image.open(image_path).convert("L")
    aspect_ratio = img.height / img.width
    # Font character aspect ratio correction (~0.55 in monospace fonts)
    height = int(width * aspect_ratio * 0.55)
    img_resized = img.resize((width, height), Image.Resampling.LANCZOS)

    ascii_rows = []
    pixels = img_resized.getdata()
    
    for y in range(height):
        row = []
        for x in range(width):
            brightness = pixels[y * width + x]
            # Map 0..255 to character index in RAMP
            char_idx = int((brightness / 255) * (len(RAMP) - 1))
            row.append(RAMP[char_idx])
        ascii_rows.append("".join(row))

    return ascii_rows

def generate_default_matrix(width: int, height: int):
    rows = []
    for y in range(height):
        row = []
        for x in range(width):
            # Create a stylized geometric avatar pattern
            dist = ((x - width/2)**2 + (y - height/2)**2)**0.5
            val = int((dist / (width/2)) * (len(RAMP) - 1))
            val = max(0, min(len(RAMP) - 1, val))
            row.append(RAMP[val])
        rows.append("".join(row))
    return rows

def generate_ascii_svg(image_path: str, output_path: str, char_width: int = 75):
    ascii_rows = image_to_ascii(image_path, char_width)
    row_count = len(ascii_rows)

    font_size = 7
    line_height = 8.5
    char_spacing = 4.2

    svg_width = int(char_width * char_spacing) + 40
    svg_height = int(row_count * line_height) + 50

    # SMIL typing animation parameters
    row_duration = 0.05  # seconds per row
    
    clip_paths = []
    text_elements = []

    for idx, row_text in enumerate(ascii_rows):
        clip_id = f"row-clip-{idx}"
        y_pos = 35 + (idx * line_height)
        start_delay = round(0.1 + (idx * row_duration), 3)

        # Escape HTML entities for SVG compatibility
        safe_text = (
            row_text.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                    .replace('"', "&quot;")
                    .replace(" ", "&#160;")
        )

        # ClipPath wiping left to right
        clip_paths.append(f'''
    <clipPath id="{clip_id}">
      <rect x="0" y="{y_pos - 7}" width="0" height="{line_height + 2}">
        <animate attributeName="width" from="0" to="{svg_width}" begin="{start_delay}s" dur="0.25s" fill="freeze" />
      </rect>
    </clipPath>''')

        # Row Text Element
        text_elements.append(f'''
    <text x="20" y="{y_pos}" clip-path="url(#{clip_id})" class="ascii-text">{safe_text}</text>''')

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">
  <style>
    .bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1px; rx: 10px; }}
    .title-bar {{ fill: #161b22; rx: 10px; }}
    .dot-red {{ fill: #ff5f56; }}
    .dot-yellow {{ fill: #ffbd2e; }}
    .dot-green {{ fill: #27c93f; }}
    .title-text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 11px; fill: #8b949e; font-weight: bold; }}
    .ascii-text {{
      font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
      font-size: {font_size}px;
      fill: #8b949e;
      letter-spacing: 0px;
      white-space: pre;
    }}
  </style>

  <!-- Container Box -->
  <rect width="100%" height="100%" class="bg" />

  <!-- Terminal Title Bar -->
  <path d="M 0,10 A 10,10 0 0,1 10,0 L {svg_width-10},0 A 10,10 0 0,1 {svg_width},10 L {svg_width},26 L 0,26 Z" class="title-bar" />
  <circle cx="16" cy="13" r="4.5" class="dot-red" />
  <circle cx="29" cy="13" r="4.5" class="dot-yellow" />
  <circle cx="42" cy="13" r="4.5" class="dot-green" />
  <text x="{svg_width/2}" y="17" text-anchor="middle" class="title-text">portrait.ascii</text>

  <defs>
    {''.join(clip_paths)}
  </defs>

  <!-- ASCII Rows -->
  <g>
    {''.join(text_elements)}
  </g>
</svg>
'''

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"[+] Generated self-typing ASCII portrait SVG at {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert photo to self-typing ASCII SVG.")
    parser.add_argument("--image", type=str, default="data/source-prepped.png", help="Prepped image path")
    parser.add_argument("--output", type=str, default="avi-ascii.svg", help="Output SVG path")
    parser.add_argument("--width", type=int, default=85, help="Character width matrix")
    args = parser.parse_args()

    generate_ascii_svg(args.image, args.output, args.width)

if __name__ == "__main__":
    main()
