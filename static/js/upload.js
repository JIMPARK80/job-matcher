document.addEventListener('DOMContentLoaded', function() { // when the page is loaded
    const fileInput = document.getElementById('fileInput'); // get the file input
    const selectedFileName = document.getElementById('selectedFileName'); // get the file name
    const uploadForm = document.getElementById('uploadForm'); // get the form   

    // file input change event
    fileInput.addEventListener('change', (e) => { // when file input changes
        if (e.target.files.length) { // if there is a file
            selectedFileName.textContent = e.target.files[0].name; // show the file name
            selectedFileName.classList.add('has-file'); // add a class to the file name
        } else { // if there is no file
            selectedFileName.textContent = 'No file selected'; // show "No file selected"
            selectedFileName.classList.remove('has-file'); // remove the class from the file name
        }
    });

    // form submit event
    uploadForm.addEventListener('submit', (e) => { // when the form is submitted
        if (!fileInput.files.length && !selectedFileName.textContent.includes('.pdf')) { // if there is no file or the file is not a PDF
            e.preventDefault(); // prevent the default behavior 
            alert('Please select a PDF file'); // show an alert
        }
    });
}); 

