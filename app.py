from collections import Counter # Counter for keyword frequency
from flask import Flask, render_template, request, jsonify, session # Flask for web app
from io import BytesIO # BytesIO for file handling  
import os
import uuid
from datetime import datetime
from job_matcher import (
    extract_keywords_from_resume, # Extract keywords from resume
    search_google_jobs, # Search Google jobs
    match_roles_with_priority, # Match roles with priority
    extract_text_from_pdf, # Extract text from PDF
    extract_profile_info # Extract profile info
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit
app.secret_key = 'your-secret-key-123'  # 고정된 시크릿 키 사용

# 임시 저장소 (실제 프로덕션에서는 데이터베이스 사용 권장)
RESUME_DATA = {}

@app.route('/')
def index():
    # 새로운 세션 시작
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/submit_pdf', methods=['POST'])
def submit_pdf():
    user_id = session.get('user_id')
    if not user_id:
        session['user_id'] = str(uuid.uuid4())
        user_id = session['user_id']

    location = request.form.get('location', 'Toronto')
    
    # 파일이 새로 업로드된 경우
    if 'resume' in request.files and request.files['resume'].filename:
        file = request.files['resume']
        if not file.filename.endswith('.pdf'):
            return "Only PDF files are supported", 400
            
        try:
            # 파일 처리
            file_content = file.read()
            text = extract_text_from_pdf(file_content)
            keywords = extract_keywords_from_resume(file_content, is_pdf=True)
            profile_info = extract_profile_info(text)
            
            # 처리된 데이터 저장
            RESUME_DATA[user_id] = {
                'filename': file.filename,
                'keywords': keywords,
                'profile': profile_info,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            print(f"[Error] Resume PDF processing failed: {e}")
            return f"❌ Error processing resume: {str(e)}", 500
    
    # 저장된 데이터 사용
    user_data = RESUME_DATA.get(user_id, {})
    if not user_data:
        return "Please upload a PDF file first", 400

    keywords = user_data.get('keywords', [])
    profile_info = user_data.get('profile', {})
    filename = user_data.get('filename', '')

    # 직무 매칭
    matched_roles, unique_roles, top_roles = match_roles_with_priority(keywords)

    # 구글 검색 링크 생성
    job_links = [
        (role, f"https://www.google.com/search?q={role.replace(' ', '+')}+jobs+in+{location.replace(' ', '+')}")
        for role in top_roles
    ]

    return render_template(
        'index.html',
        keywords=keywords,
        filename=filename,
        matched_roles=matched_roles,
        google_links=job_links,
        unique_roles=unique_roles,
        location=location,
        top_roles=top_roles,
        profile=profile_info,
    )

# ------------------------------
# Real-time Google Job Preview
# ------------------------------
@app.route("/job_preview/<role>/<city>")
def job_preview(role, city):
    jobs = search_google_jobs(role, city)
    return jsonify(jobs[:5])


# ------------------------------
# File size exceeded error handling
# ------------------------------
@app.errorhandler(413)
def file_too_large(e):
    return "❌ File too large. Please upload a PDF under 2MB.", 413

# 주기적으로 오래된 데이터 정리 (실제 환경에서는 더 나은 방법 사용 필요)
def cleanup_old_data():
    current_time = datetime.now()
    for user_id in list(RESUME_DATA.keys()):
        data_time = RESUME_DATA[user_id]['timestamp']
        if (current_time - data_time).total_seconds() > 3600:  # 1시간 이상 된 데이터
            del RESUME_DATA[user_id]

if __name__ == '__main__':
    app.run(debug=True)
