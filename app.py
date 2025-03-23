from flask import Flask, render_template, request, redirect, jsonify
from io import BytesIO
from job_matcher import extract_keywords_from_resume, keyword_to_roles, google_job_urls_from_roles, role_descriptions, search_google_jobs

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
        # 키워드 추출 / Extract keywords
        keywords = extract_keywords_from_resume(file_stream)

        # 키워드 편집 페이지로 렌더링 / Render the keyword editing page
        return render_template(
            'edit_keywords.html',
            keywords = keywords,
            filename = file.filename
        )
        
    except Exception as e:
        print(f"[Error] Resume processing failed: {e}")  # 서버 로그 출력
        return "❌ An error occurred while processing your resume. Please try again later.", 500

# Process edited keywords -> result page / 편집된 키워드 처리 -> 결과 페이지 렌더링
@app.route('/process_keywords', methods=['POST'])
def process_keywords():
    edited = request.form.get('edited_keywords', '')
    filename = request.form.get('filename', 'resume.pdf')

    # 문자열 → 키워드 리스트로 변환 (쉼표로 분리)
    keywords = [kw.strip().lower() for kw in edited.split(',') if kw.strip()]

    matched_roles = {
        kw: keyword_to_roles.get(kw, ["(no match)"])
        for kw in keywords
    }
    
    
    unique_roles = sorted(set(
        role for roles in matched_roles.values() for role in roles if role != "(no match)"
    )) # 중복 제거 및 정렬 / Remove duplicates and sort
    
    # 역할 설명 가져오기 / Get role descriptions
    role_desc = get_role_descriptions(unique_roles)
    
    # 구글 검색 링크 생성 / Create Google search links
    job_links = google_job_urls_from_roles(matched_roles)


    return render_template( 
        'result.html',
        keywords=keywords,
        matched_roles=matched_roles,
        google_links=job_links,
        filename=filename,
        role_desc=role_desc,
        unique_roles=unique_roles 
    )

@app.route("/job_preview/<role>/<city>")
def job_preview(role, city):
    jobs = search_google_jobs(role, city)
    return jsonify(jobs[:5])  # 최대 5개만 반환


# Error handling / 오류 처리
@app.errorhandler(413)
def file_too_large(e):
    return "❌ File too large. Please upload a PDF under 2MB.", 413



def get_role_descriptions(roles):
    return {
        role: role_descriptions.get(role.lower(), "(description not available)")
        for role in roles
    }


if __name__ == '__main__':
    app.run(debug=True)
