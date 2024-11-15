from PIL import Image, ImageDraw, ImageFont
import os
from PIL import __version__
print(__version__)

try:
    image = Image.new("RGB", (400, 100), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Try the default font
    font = ImageFont.load_default()
    
    test_text = "ABC 123"
    draw.text((10, 30), test_text, font=font, fill=(0, 0, 0))
    
    output_path = os.path.join(os.path.dirname(__file__), "output.png")
    image.save(output_path)
    print(f"Image saved as: {output_path}")

except Exception as e:
    print(f"Error: {str(e)}")