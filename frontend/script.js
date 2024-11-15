const API_URL = 'http://127.0.0.1:8080';

const priceInput = document.getElementById('priceInput');
const generateBtn = document.getElementById('generateBtn');
const previewImage = document.getElementById('previewImage');
const downloadPdfBtn = document.getElementById('downloadPdfBtn');
const loading = document.getElementById('loading');
const error = document.getElementById('error');

async function generatePreview() {
    try {
        error.style.display = 'none';
        loading.style.display = 'block';
        previewImage.style.display = 'none';
        downloadPdfBtn.style.display = 'none';
        
        const response = await fetch(`${API_URL}/api/preview`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: priceInput.value })
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate preview');
        }
        
        const data = await response.json();
        previewImage.src = data.image;
        previewImage.style.display = 'block';
        downloadPdfBtn.style.display = 'block';
        
    } catch (err) {
        error.textContent = err.message;
        error.style.display = 'block';
    } finally {
        loading.style.display = 'none';
    }
}

async function downloadPdf() {
    try {
        error.style.display = 'none';
        loading.style.display = 'block';
        
        const response = await fetch(`${API_URL}/api/generate-pdf`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: priceInput.value })
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate PDF');
        }
        
        // Create blob from response and download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'labels.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
    } catch (err) {
        error.textContent = err.message;
        error.style.display = 'block';
    } finally {
        loading.style.display = 'none';
    }
}

generateBtn.addEventListener('click', generatePreview);
downloadPdfBtn.addEventListener('click', downloadPdf);

// Optional: Enable generate on Enter key
priceInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        generatePreview();
    }
});
