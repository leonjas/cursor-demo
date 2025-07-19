import os
import glob
from PIL import Image
import base64
from io import BytesIO

def list_generated_images():
    """List all generated PNG files with their sizes"""
    png_files = glob.glob("*.png")
    png_files.sort()
    
    print("📊 Generated Visualization Files:")
    print("=" * 50)
    
    for i, file in enumerate(png_files, 1):
        if os.path.exists(file):
            size = os.path.getsize(file)
            size_kb = size / 1024
            
            # Try to get image dimensions
            try:
                with Image.open(file) as img:
                    width, height = img.size
                    print(f"{i}. {file}")
                    print(f"   Size: {size_kb:.1f} KB")
                    print(f"   Dimensions: {width}x{height} pixels")
                    print()
            except Exception as e:
                print(f"{i}. {file} - Error reading: {e}")
                
def create_html_viewer():
    """Create an HTML file to view all images"""
    png_files = glob.glob("*.png")
    png_files.sort()
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Score Visualizations</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .image-container { margin: 20px 0; text-align: center; }
            .image-container img { max-width: 100%; height: auto; border: 1px solid #ddd; }
            .image-title { font-weight: bold; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>Student Score Data Visualizations</h1>
    """
    
    for file in png_files:
        title = file.replace('.png', '').replace('_', ' ').title()
        html_content += f"""
        <div class="image-container">
            <div class="image-title">{title}</div>
            <img src="{file}" alt="{title}">
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    with open("visualizations_viewer.html", "w") as f:
        f.write(html_content)
    
    print("📄 Created 'visualizations_viewer.html' - you can download and open this in a browser!")

if __name__ == "__main__":
    list_generated_images()
    create_html_viewer()
    
    print("\n💡 To view images:")
    print("1. Download the PNG files to your local machine")
    print("2. Or download 'visualizations_viewer.html' and open in browser")
    print("3. Or copy the script files locally and run there")