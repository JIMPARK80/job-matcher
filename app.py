from flask import Flask, render_template, request, redirect
from io import BytesIO
from job_matcher import extract_keywords_from_resume, keyword_to_roles, google_job_urls_from_roles

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # Limited size as 2MB

# Home page / 홈 페이지
@app.route('/')
def index():
    return render_template('index.html')


# Upload resume / 이력서 업로드
@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return "No file uploaded", 400
    
    # Get the file / 파일 가져오기
    file = request.files['resume']
    if file.filename == '':
        return "No file selected", 400
    
    # Check if the file is a PDF / 파일이 PDF인지 확인
    if not file.filename.endswith('.pdf'):
        return "Only PDF files are supported", 400
    
    file_stream = file.read()
    
    try: 
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
        
    except Exception as e:
        print(f"[Error] Resume processing failed: {e}")  # 서버 로그 출력
        return "❌ An error occurred while processing your resume. Please try again later.", 500

# Error handling / 오류 처리
@app.errorhandler(413)
def file_too_large(e):
    return "❌ File too large. Please upload a PDF under 2MB.", 413


if __name__ == '__main__':
    app.run(debug=True)
