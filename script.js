document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById('image-upload');
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    document.getElementById('result').innerText = `Result: ${result.output}`;

    // Display uploaded image
    if (result.image_url) {
        const uploadedImage = document.createElement('img');
        uploadedImage.src = result.image_url;
        uploadedImage.alt = 'Uploaded Image';
        uploadedImage.style.maxWidth = '100%';
        
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = ''; // Clear previous content
        resultDiv.appendChild(uploadedImage);
    }
});
