import requests
import base64
from PIL import Image
import io
import os
import PyPDF2

def test_preview():
    url = "http://127.0.0.1:8080/api/preview"
    test_text = "$10.00"
    print(f"\nTesting preview with text: '{test_text}'")
    
    try:
        payload = {"text": test_text}
        print(f"Sending payload: {payload}")
        
        response = requests.post(url, json=payload)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("Preview generated successfully!")
            response_data = response.json()
            print(f"Response data keys: {response_data.keys()}")
            
            # Save the preview image
            img_data = response_data['image']
            if not img_data.startswith('data:image/png;base64,'):
                print("Warning: Image data doesn't have expected prefix")
            img_data = img_data.replace('data:image/png;base64,', '')
            img_bytes = base64.b64decode(img_data)
            
            # Save and open the image
            output_path = 'test_preview.png'
            with open(output_path, 'wb') as f:
                f.write(img_bytes)
            print(f"Preview saved as '{output_path}'")
            print(f"File size: {os.path.getsize(output_path)} bytes")
            
            # Open and display image properties
            with Image.open(output_path) as img:
                print(f"Image size: {img.size}")
                print(f"Image mode: {img.mode}")
                print(f"Image format: {img.format}")
                img.show()
            return True
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("Connection Error: Make sure the Flask server is running on http://127.0.0.1:8080")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

def test_pdf():
    url = "http://127.0.0.1:8080/api/generate-pdf"
    test_text = "$10.00"
    print(f"\nTesting PDF generation with text: '{test_text}'")
    
    try:
        payload = {"text": test_text}
        print(f"Sending payload: {payload}")
        
        response = requests.post(url, json=payload)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("PDF generated successfully!")
            
            # Save the PDF
            output_path = 'test_labels.pdf'
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"PDF saved as '{output_path}'")
            print(f"File size: {os.path.getsize(output_path)} bytes")
            
            # Analyze PDF properties
            with open(output_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                num_pages = len(pdf_reader.pages)
                print(f"Number of pages: {num_pages}")
                
                # Get page size of first page
                page = pdf_reader.pages[0]
                width = float(page.mediabox.width)
                height = float(page.mediabox.height)
                print(f"Page size: {width} x {height} points")
            
            return True
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("Connection Error: Make sure the Flask server is running on http://127.0.0.1:8080")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

def run_all_tests():
    print("Starting tests...")
    tests_passed = 0
    total_tests = 2
    
    if test_preview():
        tests_passed += 1
    if test_pdf():
        tests_passed += 1
        
    print(f"\nTests completed: {tests_passed}/{total_tests} passed")
    return tests_passed == total_tests

if __name__ == "__main__":
    run_all_tests()