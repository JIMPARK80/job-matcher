from flask import Flask, render_template, request, redirect
from io import BytesIO
from job_matcher import extract_keywords_from_resume, keyword_to_roles, google_job_urls_from_roles

app = Flask(__name__)

# Home page / 홈 페이지
@app.route('/')
def index():
    return render_template('index.html')


# Upload resume / 이력서 업로드
@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['resume']
    if file.filename == '':
        return "No file selected", 400
    
    if not file.filename.endswith('.pdf'):
        return "Only PDF files are supported", 400
    
    file_stream = file.read()
    
    # keywords extraction / 키워드 추출
    keywords = extract_keywords_from_resume(file_stream)

    # Suggested position per keyword / 키워드 별 제안된 포지션
    matched_roles = {
        kw: keyword_to_roles.get(kw, ["(no match)"])
        for kw in keywords
    }
    
    job_links = google_job_urls_from_roles(matched_roles)

    return render_template(
        'result.html',
        keywords = keywords,
        matched_roles = matched_roles,
        google_links = job_links,
        filename = file.filename
    )

if __name__ == '__main__':
    app.run(debug=True)
