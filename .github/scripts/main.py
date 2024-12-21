from PIL import Image
import os
from pathlib import Path
import shutil

def optimize_image(input_path, output_path, max_width=1920):
    """
    Optimize an image by:
    1. Resizing if wider than max_width while maintaining aspect ratio
    2. Converting to progressive JPEG
    3. Optimizing quality
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Calculate new dimensions if needed
            if img.width > max_width:
                ratio = max_width / img.width
                new_size = (max_width, int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(output_path,
                    'JPEG',
                    quality=85,
                    optimize=True,
                    progressive=True)
            
            # Get file size reduction
            original_size = os.path.getsize(input_path)
            optimized_size = os.path.getsize(output_path)
            reduction = (original_size - optimized_size) / original_size * 100
            
            print(f"Optimized {input_path}")
            print(f"Size reduction: {reduction:.1f}%")
            
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

def main():
    # Define paths
    input_dir = Path("images")
    output_dir = Path("image_optimize")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Process all images in input directory
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    
    for input_path in input_dir.rglob("*"):
        if input_path.suffix.lower() in image_extensions:
            # Create relative path for output
            relative_path = input_path.relative_to(input_dir)
            output_path = output_dir / relative_path.with_suffix('.jpg')
            
            # Optimize image
            optimize_image(str(input_path), str(output_path))

if __name__ == "__main__":
    main()
