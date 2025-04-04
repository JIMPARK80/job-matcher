from collections import Counter # Counter for keyword frequency
from flask import Flask, render_template, request, jsonify, session # Flask for web app
from io import BytesIO # BytesIO for file handling  
import os
import uuid # UUID for unique user ID
from datetime import datetime # datetime for timestamp
from job_matcher import ( # job matcher
    extract_keywords_from_resume, # Extract keywords from resume
    search_google_jobs, # Search Google jobs
    match_roles_with_priority, # Match roles with priority
    extract_text_from_pdf, # Extract text from PDF
    extract_profile_info # Extract profile info
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit
app.secret_key = 'your-secret-key-123' # secret key

# temporary storage (recommended to use a database in production)
RESUME_DATA = {}

@app.route('/')
def index(): # index page
    # start a new session
    if 'user_id' not in session: # if there is no user ID
        session['user_id'] = str(uuid.uuid4()) # create a new user ID
    return render_template('index.html') # render the index page

@app.route('/submit_pdf', methods=['POST']) # submit the PDF file
def submit_pdf(): # submit the PDF file
    user_id = session.get('user_id') # get the user ID
    if not user_id: # if there is no user ID
        session['user_id'] = str(uuid.uuid4()) # create a new user ID
        user_id = session['user_id'] # update the user ID

    location = request.form.get('location', 'Toronto') # get the location
    
    if 'resume' in request.files and request.files['resume'].filename: # if there is a resume file
        file = request.files['resume'] # get the resume file
        if not file.filename.endswith('.pdf'): # if the file is not a PDF
            return "Only PDF files are supported", 400 # return an error
            
        try:
            # process the file
            file_content = file.read() # read the file
            text = extract_text_from_pdf(file_content) # extract the text from the file
            keywords = extract_keywords_from_resume(file_content, is_pdf=True) # extract the keywords from the file
            profile_info = extract_profile_info(text) # extract the profile info from the file
            
            # save the processed data
            RESUME_DATA[user_id] = { # save the processed data
                'filename': file.filename, # save the file name
                'keywords': keywords, # save the keywords
                'profile': profile_info, # save the profile info
                'timestamp': datetime.now() # save the timestamp
            }
            
        except Exception as e: # if there is an error
            print(f"[Error] Resume PDF processing failed: {e}") # print the error
            return f"❌ Error processing resume: {str(e)}", 500 # return an error
    
    # use the saved data
    user_data = RESUME_DATA.get(user_id, {}) # get the user data
    if not user_data: # if there is no user data
        return "Please upload a PDF file first", 400 # return an error

    keywords = user_data.get('keywords', []) # get the keywords
    profile_info = user_data.get('profile', {}) # get the profile info
    filename = user_data.get('filename', '') # get the file name

    # match roles
    matched_roles, unique_roles, top_roles = match_roles_with_priority(keywords) # match the roles

    # create google search links
    job_links = [
        (role, f"https://www.google.com/search?q={role.replace(' ', '+')}+jobs+in+{location.replace(' ', '+')}")
        for role in top_roles # for each role
    ]

    return render_template( # render the index page
        'index.html', # index.html
        keywords=keywords, # keywords
        filename=filename, # file name
        matched_roles=matched_roles, # matched roles
        google_links=job_links, # google links
        unique_roles=unique_roles, # unique roles
        location=location, # location
        top_roles=top_roles, # top roles
        profile=profile_info, # profile info
    )

# ------------------------------
# Real-time Google Job Preview
# ------------------------------
@app.route("/job_preview/<role>/<city>") # real-time google job preview
def job_preview(role, city): # real-time google job preview
    jobs = search_google_jobs(role, city) # search the google jobs
    return jsonify(jobs[:5])


# ------------------------------
# File size exceeded error handling
# ------------------------------
@app.errorhandler(413) # file size exceeded error handling
def file_too_large(e): # file size exceeded error handling
    return "❌ File too large. Please upload a PDF under 2MB.", 413 # return an error

# ------------------------------
# Cleanup old data
# ------------------------------
def cleanup_old_data(): # cleanup the old data
    current_time = datetime.now() # get the current time
    for user_id in list(RESUME_DATA.keys()): # for each user ID
        data_time = RESUME_DATA[user_id]['timestamp'] # get the data time
        if (current_time - data_time).total_seconds() > 3600: # if the data is older than 1 hour
            del RESUME_DATA[user_id] # delete the data

if __name__ == '__main__':
    app.run(debug=True) # run the app
