document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const error = document.getElementById('error');
    const summaryContent = document.getElementById('summary-content');
    const errorMessage = document.getElementById('error-message');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const file = fileInput.files[0];
        if (!file) {
            showError('Please select a file.');
            return;
        }

        // Check file type
        const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
        if (!allowedTypes.includes(file.type)) {
            showError('Please upload a PDF or image file (JPG/PNG).');
            return;
        }

        // Check file size (16MB limit)
        if (file.size > 16 * 1024 * 1024) {
            showError('File size must be less than 16MB.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        const length = document.getElementById('length-select').value;
        formData.append('length', length);

        showLoading();

        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            if (data.error) {
                showError(data.error);
            } else {
                showResult(data.summary);
            }
        })
        .catch(err => {
            hideLoading();
            showError('An error occurred while processing your request.');
        });
    });

    function showLoading() {
        loading.style.display = 'block';
        result.style.display = 'none';
        error.style.display = 'none';
    }

    function hideLoading() {
        loading.style.display = 'none';
    }

    function showResult(summary) {
        summaryContent.innerHTML = summary;
        result.style.display = 'block';
        error.style.display = 'none';
        // Add fade-in animation
        result.style.opacity = '0';
        result.style.transform = 'translateY(20px)';
        setTimeout(() => {
            result.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            result.style.opacity = '1';
            result.style.transform = 'translateY(0)';
        }, 100);
    }

    function showError(message) {
        errorMessage.textContent = message;
        error.style.display = 'block';
        result.style.display = 'none';
    }

    // Drag and drop functionality
    const uploadArea = document.querySelector('.upload-area');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        uploadArea.classList.add('highlight');
    }

    function unhighlight(e) {
        uploadArea.classList.remove('highlight');
    }

    uploadArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            fileInput.files = files;
            // Update the label to show the selected file name
            const fileName = files[0].name;
            document.querySelector('.upload-text').textContent = fileName;
        }
    }
});
