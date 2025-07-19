import base64
import json
import glob
import os
from datetime import datetime

def extract_image_package():
    """Extract PNG files from the JSON package"""
    
    # Find the most recent image package
    package_files = glob.glob("image_package_*.json")
    
    if not package_files:
        print("❌ No image package file found!")
        print("💡 Make sure to run 'python package_images.py' on the remote first")
        return
    
    # Use the most recent package file
    package_file = max(package_files, key=os.path.getctime)
    print(f"📦 Found package: {package_file}")
    
    # Load package data
    try:
        with open(package_file, 'r') as f:
            package_data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading package file: {e}")
        return
    
    print(f"📅 Package created: {package_data['created']}")
    print(f"📊 Total files: {package_data['total_files']}")
    print(f"\n🔄 Extracting images...")
    
    extracted_count = 0
    
    for filename, image_info in package_data["images"].items():
        try:
            # Decode base64 image data
            image_data = base64.b64decode(image_info["data"])
            
            # Write PNG file
            with open(filename, "wb") as f:
                f.write(image_data)
            
            file_size = len(image_data)
            print(f"   ✅ {filename} ({file_size/1024:.1f} KB)")
            extracted_count += 1
            
        except Exception as e:
            print(f"   ❌ Error extracting {filename}: {e}")
    
    print(f"\n🎉 Successfully extracted {extracted_count}/{package_data['total_files']} images!")
    print(f"📂 PNG files are now available in your local directory")
    
    # Clean up package file
    try:
        os.remove(package_file)
        print(f"🗑️  Cleaned up package file: {package_file}")
    except:
        pass

def list_available_images():
    """List all PNG files in current directory"""
    png_files = glob.glob("*.png")
    
    if png_files:
        print(f"\n📊 Available PNG files ({len(png_files)}):")
        for i, png_file in enumerate(sorted(png_files), 1):
            size = os.path.getsize(png_file) / 1024 if os.path.exists(png_file) else 0
            print(f"   {i}. {png_file} ({size:.1f} KB)")
    else:
        print("\n📂 No PNG files found in current directory")

if __name__ == "__main__":
    extract_image_package()
    list_available_images()