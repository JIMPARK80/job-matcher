from flask import Flask, render_template, request, redirect, jsonify
from io import BytesIO
from job_matcher import extract_keywords_from_resume, keyword_to_roles, google_job_urls_from_roles, role_descriptions, search_google_jobs

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB 제한

# 홈 및 이력서 업로드 처리
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return "No file uploaded", 400

        file = request.files['resume']
        if file.filename == '':
            return "No file selected", 400

        if not file.filename.endswith('.pdf'):
            return "Only PDF files are supported", 400

        file_stream = file.read()

        try:
            # 키워드 추출
            keywords = extract_keywords_from_resume(file_stream)

            # 키워드 편집 페이지 렌더링
            return render_template(
                'edit_keywords.html',
                keywords=keywords,
                filename=file.filename
            )

        except Exception as e:
            print(f"[Error] Resume processing failed: {e}")
            return "❌ An error occurred while processing your resume. Please try again later.", 500

    return render_template('index.html')

# 편집된 키워드 처리 → 결과 페이지 렌더링
@app.route('/process_keywords', methods=['POST'])
def process_keywords():
    edited = request.form.get('edited_keywords', '')
    filename = request.form.get('filename', 'resume.pdf')

    # 쉼표로 분리된 문자열 → 키워드 리스트
    keywords = [kw.strip().lower() for kw in edited.split(',') if kw.strip()]

    matched_roles = {
        kw: keyword_to_roles.get(kw, ["(no match)"])
        for kw in keywords
    }

    # 중복 제거 및 정렬
    unique_roles = sorted(set(
        role for roles in matched_roles.values() for role in roles if role != "(no match)"
    ))

    # 역할 설명 가져오기
    role_desc = get_role_descriptions(unique_roles)

    # 구글 검색 링크 생성
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


# 실시간 구글 Job 미리보기 API
@app.route("/job_preview/<role>/<city>")
def job_preview(role, city):
    jobs = search_google_jobs(role, city)
    return jsonify(jobs[:5])  # 최대 5개 반환


# 파일 용량 초과 에러 처리
@app.errorhandler(413)
def file_too_large(e):
    return "❌ File too large. Please upload a PDF under 2MB.", 413


# 역할 설명 반환 함수
def get_role_descriptions(roles):
    return {
        role: role_descriptions.get(role.lower(), "(description not available)")
        for role in roles
    }


if __name__ == '__main__':
    app.run(debug=True)