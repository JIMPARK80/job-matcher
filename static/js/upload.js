document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const selectedFileName = document.getElementById('selectedFileName');
    const uploadForm = document.getElementById('uploadForm');

    // 파일 선택 시 파일명 표시
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            selectedFileName.textContent = e.target.files[0].name;
            selectedFileName.classList.add('has-file');
        } else {
            selectedFileName.textContent = '선택된 파일 없음';
            selectedFileName.classList.remove('has-file');
        }
    });

    // 폼 제출 처리
    uploadForm.addEventListener('submit', (e) => {
        if (!fileInput.files.length && !selectedFileName.textContent.includes('.pdf')) {
            e.preventDefault();
            alert('Please select a PDF file');
        }
    });
}); 