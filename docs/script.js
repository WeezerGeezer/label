document.addEventListener('DOMContentLoaded', function() {
    const API_URL = 'https://label-generator-424740197089.us-central1.run.app/api';
    const priceInput = document.getElementById('priceInput');
    const generateBtn = document.getElementById('generateBtn');
    const exportPdfBtn = document.getElementById('exportPdfBtn');
    const previewImage = document.getElementById('previewImage');
    const messageBox = document.getElementById('messageBox');

    function showMessage(message, isError = false) {
        messageBox.textContent = message;
        messageBox.className = isError ? 'error' : 'success';
        setTimeout(() => {
            messageBox.textContent = '';
            messageBox.className = '';
        }, 5000);
    }

    generateBtn.addEventListener('click', async function() {
        const price = priceInput.value.trim();
        if (!price) {
            showMessage('Please enter a price', true);
            return;
        }

        try {
            const response = await fetch(`${API_URL}/preview`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                mode: 'cors',
                body: JSON.stringify({ text: price })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            previewImage.src = data.image;
            previewImage.style.display = 'block';
            showMessage('Preview generated successfully!');
        } catch (error) {
            console.error('Error:', error);
            showMessage('Error generating preview: ' + error.message, true);
        }
    });

    exportPdfBtn.addEventListener('click', async function() {
        const price = priceInput.value.trim();
        if (!price) {
            showMessage('Please enter a price', true);
            return;
        }

        try {
            const response = await fetch(`${API_URL}/generate-pdf`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                mode: 'cors',
                body: JSON.stringify({ text: price })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'labels.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            showMessage('PDF generated and downloaded successfully!');
        } catch (error) {
            console.error('Error:', error);
            showMessage('Error generating PDF: ' + error.message, true);
        }
    });
});