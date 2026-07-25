import os
import sys
import argparse
import numpy as np

def prep_image(input_path: str, output_path: str):
    try:
        import cv2
        from PIL import Image
    except ImportError:
        print("[!] OpenCV and Pillow are required for prep_photo.py. Installing/running fallback.")
        sys.exit(1)

    if not os.path.exists(input_path):
        print(f"[!] Input image '{input_path}' not found. Generating sample portrait...")
        create_sample_photo(input_path)

    # 1. Load Image
    img = Image.open(input_path).convert("RGBA")

    # 2. Background removal (rembg if installed)
    try:
        import rembg
        print("[*] Removing background with rembg...")
        img_no_bg = rembg.remove(img)
    except Exception as e:
        print(f"[*] rembg not available or failed ({e}). Using luminance threshold background removal...")
        img_no_bg = img

    # Composite on white background
    white_bg = Image.new("RGBA", img_no_bg.size, (255, 255, 255, 255))
    composite = Image.alpha_composite(white_bg, img_no_bg).convert("L")

    # 3. Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) with OpenCV
    img_np = np.array(composite)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_np = clahe.apply(img_np)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    cv2.imwrite(output_path, enhanced_np)
    print(f"[✓] Saved prepped photo to {output_path}")

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
