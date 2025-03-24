from flask import Flask, render_template, request, redirect, jsonify
from io import BytesIO
from job_matcher import (
    extract_keywords_from_resume,
    keyword_to_roles,
    google_job_urls_from_roles,
    role_descriptions,
    search_google_jobs
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limited size 제한


# ------------------------------
# Home Page /  홈 페이지 (index.html)
# ------------------------------
@app.route('/')
def index():
    return render_template('index.html')


# ------------------------------
# PDF Uploading file /  업로드 처리
# ------------------------------
@app.route('/submit_pdf', methods=['POST'])
def submit_pdf():
    if 'resume' not in request.files:
        return "No file uploaded", 400

    file = request.files['resume']
    if file.filename == '':
        return "No file selected", 400

    if not file.filename.endswith('.pdf'):
        return "Only PDF files are supported", 400

    file_stream = file.read()
    location = request.form.get('location', 'Toronto') # ✅ 위치 추가 기본값

    try:
        keywords = extract_keywords_from_resume(file_stream, is_pdf=True)

        matched_roles = {
            kw: keyword_to_roles.get(kw.lower(), ["(no match)"])
            for kw in keywords
        }

        unique_roles = sorted(set(
            role for roles in matched_roles.values() for role in roles if role != "(no match)"
        ))

        role_desc = get_role_descriptions(unique_roles)
        job_links = google_job_urls_from_roles(matched_roles, location)  # ✅ 위치 포함

        return render_template(
            'index.html',
            keywords=keywords,
            filename=file.filename,
            matched_roles=matched_roles,
            google_links=job_links,
            role_desc=role_desc,
            unique_roles=unique_roles,
            location=location  # ✅ 템플릿에 전달
        )

    except Exception as e:
        print(f"[Error] Resume PDF processing failed: {e}")
        return "❌ Error processing resume.", 500
    
    
# ------------------------------
# Input Text and run resume /  텍스트 입력 이력서 처리
# -> 나중에 하기 / To be done later
# ------------------------------

# ------------------------------
# 결과 페이지 렌더링 함수
# ------------------------------
def show_result_page(keywords, filename):
    keywords = [kw.strip().lower() for kw in keywords if kw.strip()]

    matched_roles = {
        kw: keyword_to_roles.get(kw, ["(no match)"])
        for kw in keywords
    }

    unique_roles = sorted(set(
        role for roles in matched_roles.values() for role in roles if role != "(no match)"
    ))

    role_desc = get_role_descriptions(unique_roles)
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
    
    
# ------------------------------
# 실시간 Google Job 미리보기
# ------------------------------
@app.route("/job_preview/<role>/<city>")
def job_preview(role, city):
    jobs = search_google_jobs(role, city)
    return jsonify(jobs[:5])

# ------------------------------
# 파일 용량 초과 에러 처리
# ------------------------------
@app.errorhandler(413)
def file_too_large(e):
    return "❌ File too large. Please upload a PDF under 2MB.", 413

# ------------------------------
# 역할 설명 반환 함수
# ------------------------------
def get_role_descriptions(roles):
    return {
        role: role_descriptions.get(role.lower(), "(description not available)")
        for role in roles
    }

# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)