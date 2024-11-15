from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os

class LabelGenerator:
    def __init__(self):
        print("Initializing LabelGenerator...")
        # Load template image
        template_path = os.path.join(os.path.dirname(__file__), 'label_template.png')
        try:
            self.template = Image.open(template_path)
            print(f"Template loaded successfully from: {template_path}")
            print(f"Template size: {self.template.size}")
            # Store dimensions from template
            self.width_px, self.height_px = self.template.size
        except Exception as e:
            print(f"Error loading template: {str(e)}")
            raise Exception(f"Failed to load template from {template_path}")
        
        # Load font
        self.font = self._load_font()
        
    def _load_font(self):
        """Load bundled font"""
        FONT_SIZE = 250
        # Try Arial first as it's more reliable with special characters
        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'timesbd.ttf')
        
        try:
            print(f"\nLoading bundled font from: {font_path}")
            if not os.path.exists(font_path):
                raise Exception(f"Bundled font not found at {font_path}")
                
            # Remove the encoding parameter as it might be causing issues
            font = ImageFont.truetype(font_path, FONT_SIZE)
            
            # Test the font with the dollar sign specifically
            test_text = "$"
            img = Image.new('RGB', (100, 100))
            draw = ImageDraw.Draw(img)
            try:
                draw.text((10, 10), test_text, font=font, fill='black')
                print("Successfully tested dollar sign rendering")
            except Exception as e:
                print(f"Failed to render dollar sign: {e}")
                raise
                
            print("Successfully loaded bundled font")
            return font
            
        except Exception as e:
            print(f"Failed to load bundled font: {str(e)}")
            raise Exception("Could not load required font file")

    def generate_label(self, text):
        print(f"\nGenerating label for text: '{text}'")
        img = self.template.copy()
        
        # Convert image to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        draw = ImageDraw.Draw(img)
        
        try:
            # Ensure text is properly encoded
            text = text.encode('utf-8').decode('utf-8')
            print(f"Encoded text: {[ord(c) for c in text]}")  # Debug character codes
            
            # Calculate text position
            left, top, right, bottom = draw.textbbox((0, 0), text, font=self.font)
            text_width = right - left
            text_height = bottom - top
            
            # Center the text
            x = (img.width - text_width) / 2 - left
            y = (img.height - text_height) / 2 - top
            
            # Draw text in black
            draw.text((x, y), text, font=self.font, fill='black')
            print("Text drawn successfully")
            
        except Exception as e:
            print(f"Error drawing text: {e}")
            draw.text((10, 10), f"Error: {str(e)}", font=ImageFont.load_default(), fill='red')
        
        # Save to buffer
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG', dpi=(300, 300))
        img_byte_arr.seek(0)
        return img_byte_arr

    def generate_preview_base64(self, text):
        img_byte_arr = self.generate_label(text)
        encoded = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{encoded}" 