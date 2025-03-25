from collections import Counter
from flask import Flask, render_template, request, jsonify
from io import BytesIO
from job_matcher import (
    extract_keywords_from_resume,
    role_descriptions,
    search_google_jobs,
    match_roles_with_priority,
    extract_text_from_pdf,  # Added missing import
    extract_profile_info  # Added missing import
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB 제한


# ------------------------------
# Home Page
# ------------------------------
@app.route('/')
def index():
    return render_template('index.html')


# ------------------------------
# PDF Uploading 처리
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
    location = request.form.get('location', 'Toronto')

    try:
        keywords = extract_keywords_from_resume(file_stream, is_pdf=True)
        text = extract_text_from_pdf(file_stream)
        profile_info = extract_profile_info(text)

        # 👉 역할 매칭
        matched_roles, unique_roles, top_roles = match_roles_with_priority(keywords)
        role_desc = get_role_descriptions(unique_roles)

        # 👉 상위 3개 직무만 구글 링크 생성
        job_links = [
            (role, f"https://www.google.com/search?q={role.replace(' ', '+')}+jobs+in+{location.replace(' ', '+')}")
            for role in top_roles
        ]

        return render_template(
            'index.html',
            keywords=keywords,
            filename=file.filename,
            matched_roles=matched_roles,
            google_links=job_links,
            role_desc=role_desc,
            unique_roles=unique_roles,
            location=location,
            top_roles=top_roles,
            profile=profile_info,
        )

    except Exception as e:
        print(f"[Error] Resume PDF processing failed: {e}")
        return "❌ Error processing resume.", 500


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
