import os
import sys
import argparse
import numpy as np

def prep_image(input_path: str, output_path: str):
    try:
        from PIL import Image
    except ImportError:
        print("[!] Pillow is required for prep_photo.py.")
        sys.exit(1)

    if not os.path.exists(input_path):
        print(f"[!] Input image '{input_path}' not found. Generating sample portrait...")
        create_sample_photo(input_path)

    # 1. Load Image
    img = Image.open(input_path).convert("RGBA")

    # 2. Composite on white background and convert to grayscale
    if img.mode == 'RGBA':
        white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        composite = Image.alpha_composite(white_bg, img).convert("L")
    else:
        composite = img.convert("L")

    # 3. Apply contrast enhancement
    try:
        import cv2
        img_np = np.array(composite)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced_np = clahe.apply(img_np)
        enhanced_img = Image.fromarray(enhanced_np)
    except Exception:
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(composite)
        enhanced_img = enhancer.enhance(2.0)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    enhanced_img.save(output_path)
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
