import os
import sys
import argparse
import numpy as np

def prep_image(input_path: str, output_path: str):
    try:
        from PIL import Image, ImageEnhance, ImageOps
    except ImportError:
        print("[!] Pillow is required for prep_photo.py.")
        sys.exit(1)

    if not os.path.exists(input_path):
        print(f"[!] Input image '{input_path}' not found. Generating sample portrait...")
        create_sample_photo(input_path)

    # 1. Load Image
    img = Image.open(input_path).convert("RGBA")

    # 2. Crop to focus on face and upper torso of Harsh
    w, h = img.size
    left = int(w * 0.15)
    top = int(h * 0.05)
    right = int(w * 0.85)
    bottom = int(h * 0.85)
    img_cropped = img.crop((left, top, right, bottom))

    # 3. Composite on clean background and convert to grayscale
    white_bg = Image.new("RGBA", img_cropped.size, (255, 255, 255, 255))
    composite = Image.alpha_composite(white_bg, img_cropped).convert("L")

    # 4. Apply high-contrast subject tuning (enhances face features, sunglasses, jacket)
    enhancer = ImageEnhance.Contrast(composite)
    enhanced = enhancer.enhance(1.9)

    # 5. Brightness adjustment for clear ASCII mapping
    bright_enhancer = ImageEnhance.Brightness(enhanced)
    final_img = bright_enhancer.enhance(1.1)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    final_img.save(output_path)
    print(f"[+] Saved prepped photo to {output_path}")
    return

def create_sample_photo(path: str):
    """Creates a basic facial profile placeholder image if no input photo is supplied."""
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (400, 500), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    # Head & Shoulder silhouette
    draw.ellipse([100, 60, 300, 300], fill=(60, 60, 60))
    draw.ellipse([50, 250, 350, 520], fill=(40, 40, 40))
    # Glasses
    draw.rectangle([130, 140, 190, 180], outline=(255, 255, 255), width=6)
    draw.rectangle([210, 140, 270, 180], outline=(255, 255, 255), width=6)
    draw.line([190, 160, 210, 160], fill=(255, 255, 255), width=6)
    
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    img.save(path)

def main():
    parser = argparse.ArgumentParser(description="Prep photo for ASCII SVG conversion.")
    parser.add_argument("input", type=str, nargs="?", default="data/source-photo.jpg", help="Input photo path")
    parser.add_argument("--output", type=str, default="data/source-prepped.png", help="Output prepped image path")
    args = parser.parse_args()

    prep_image(args.input, args.output)

if __name__ == "__main__":
    main()
