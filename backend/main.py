from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from label_generator import LabelGenerator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io
from PIL import Image
from reportlab.lib.utils import ImageReader

app = Flask(__name__)
CORS(app)

label_generator = LabelGenerator()

@app.route('/api/preview', methods=['POST'])
def generate_preview():
    try:
        print("\n=== New Preview Request ===")
        print(f"Request headers: {dict(request.headers)}")
        data = request.get_json()
        print(f"Received data: {data}")
        
        text = data.get('text', '')
        print(f"Extracted text: '{text}'")
        
        if not text:
            print("Error: No text provided")
            return jsonify({'error': 'No text provided'}), 400
            
        preview_base64 = label_generator.generate_preview_base64(text)
        print("Successfully generated preview")
        return jsonify({'image': preview_base64})
    except Exception as e:
        print(f"Error in generate_preview: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json()
        text = data.get('text', '')
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        # Create PDF buffer
        pdf_buffer = io.BytesIO()
        page_width, page_height = letter
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        
        # Get label image and convert to temporary file
        label_buffer = label_generator.generate_label(text)
        temp_image = Image.open(label_buffer)
        temp_buffer = io.BytesIO()
        temp_image.save(temp_buffer, format='PNG')
        temp_buffer.seek(0)
        
        # Define label dimensions and spacing
        label_width = 2.6 * inch
        label_height = 1.37 * inch
        row_spacing = 0.05 * inch
        col_spacing = 0.05 * inch
        
        # Calculate margins
        total_width = (3 * label_width) + (2 * col_spacing)
        margin_left = (page_width - total_width) / 2
        total_height = (6 * label_height) + (5 * row_spacing)
        margin_bottom = (page_height - total_height) / 2
        
        # Add labels to PDF
        for row in range(6):
            for col in range(3):
                x = margin_left + (col * (label_width + col_spacing))
                y = page_height - (margin_bottom + (row * (label_height + row_spacing)) + label_height)
                c.drawImage(
                    ImageReader(temp_buffer),
                    x,
                    y,
                    width=label_width,
                    height=label_height,
                    mask=None
                )
                temp_buffer.seek(0)  # Reset buffer position for next use
        
        c.save()
        pdf_buffer.seek(0)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='labels.pdf'
        )
        
    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='127.0.0.1', port=8080, debug=True) 