import base64
import glob
import json
import os
from datetime import datetime

def create_image_package():
    """Package all PNG files into a JSON file that can be synced locally"""
    
    png_files = glob.glob("*.png")
    png_files.sort()
    
    if not png_files:
        print("No PNG files found!")
        return
    
    print(f"📦 Packaging {len(png_files)} PNG files...")
    
    # Create package data
    package_data = {
        "created": datetime.now().isoformat(),
        "total_files": len(png_files),
        "images": {}
    }
    
    for png_file in png_files:
        if os.path.exists(png_file):
            file_size = os.path.getsize(png_file)
            print(f"   Processing: {png_file} ({file_size/1024:.1f} KB)")
            
            # Read and encode image as base64
            with open(png_file, "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            package_data["images"][png_file] = {
                "filename": png_file,
                "size_bytes": file_size,
                "data": image_data
            }
    
    # Save package file
    package_filename = f"image_package_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(package_filename, 'w') as f:
        json.dump(package_data, f)
    
    package_size = os.path.getsize(package_filename)
    print(f"\n✅ Created: {package_filename}")
    print(f"📊 Package size: {package_size/1024/1024:.1f} MB")
    print(f"📂 Contains {len(png_files)} images")
    print(f"\n💡 This JSON file will sync to your local environment!")
    print(f"💡 Run 'python extract_images.py' locally to unpack the images")

if __name__ == "__main__":
    create_image_package()