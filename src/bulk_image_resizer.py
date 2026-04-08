import os
import argparse
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

def process_image(file_path: str, output_dir: str, max_width: int):
    filename = os.path.basename(file_path)
    try:
        with Image.open(file_path) as img:
            # Calculate new dimensions while preserving aspect ratio
            width_percent = (max_width / float(img.size[0]))
            new_height = int((float(img.size[1]) * float(width_percent)))
            
            # Only resize if the image is wider than the max_width
            if img.size[0] > max_width:
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Save compressed
            output_path = os.path.join(output_dir, f"compressed_{filename}")
            if img.mode in ("RGBA", "P"): 
                img = img.convert("RGB")
                
            img.save(output_path, optimize=True, quality=85)
            return True
            
    except Exception as e:
        print(f"Failed to process {filename}: {e}")
        return False

def main(input_dir: str, output_dir: str, max_width: int = 1920):
    os.makedirs(output_dir, exist_ok=True)
    images = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    
    print(f"Found {len(images)} images. Processing in parallel...")
    success_count = 0
    
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_image, img, output_dir, max_width) for img in images]
        for future in futures:
            if future.result():
                success_count += 1
                
    print(f"✅ Success! Processed {success_count}/{len(images)} images.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk Image Resizer")
    parser.add_argument("--input", "-i", type=str, required=True, help="Input directory")
    parser.add_argument("--output", "-o", type=str, default="output", help="Output directory")
    parser.add_argument("--width", "-w", type=int, default=1920, help="Max width in pixels")
    args = parser.parse_args()
    
    main(args.input, args.output, args.width)
