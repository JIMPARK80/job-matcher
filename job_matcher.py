import pdfplumber
import re

# 1. Technical Keywords Extraction Function / 기술 키워드 추출 함수 
def extract_keywords_from_resume(pdf_path): # PDF 경로
    with pdfplumber.open(pdf_path) as pdf: # Open PDF / PDF 열기
        text = '' # Initialize text / 텍스트 초기화
        for page in pdf.pages: # Loop through each page / 각 페이지 반복
            page_text = page.extract_text() # Extract text from page / 페이지에서 텍스트 추출
            if page_text: # If text exists / 텍스트가 있는 경우
                text += page_text # Append text / 텍스트 추가

    tech_keywords = [ 
        'JavaScript', 'React', 'Python', 'Java', 'HTML', 'CSS', 'Node.js', 'SQL', 'AWS',
        'Docker', 'Kubernetes', 'Spring', 'Hibernate', 'Django', 'MongoDB', 'Angular', 'Bootstrap',
        'Vue.js', 'Flask', 'REST', 'API', 'Git', 'CI/CD', 'Jenkins', 'Agile', 'Scrum', 'Kanban',
        'TDD', 'C++', 'C#', 'Ruby', 'PHP', 'Swift', 'Objective-C'
    ] # List of technical keywords / 기술 키워드 목록

    # improved accurarcy: using word boundaries  / 정확도 개선: 단어 경계 사용
    keywords_found = [
        keyword for keyword in tech_keywords 
        if re.search(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE)
    ] # Extract keywords from text / 텍스트에서 키워드 추출

    return keywords_found # Return keywords / 키워드 반환

# 2. Create a Google Search link / 구글 검색 링크 생성
def google_job_url(keyword, location="Toronto"): # Default location: Toronto / 기본 위치: 토론토
    query = f"{keyword} job in {location}" # Create query / 쿼리 생성
    
     # Return Google search link / 구글 검색 링크 반환
    return f"https://www.google.com/search?q={query.replace(' ', '+')}"

# 3. Main run / 메인 실행
if __name__ == "__main__":
    resume_pdf = "PDF/resume.pdf"  # PDF path / PDF 경로

    try: # Try to extract keywords / 키워드 추출 시
        keywords = extract_keywords_from_resume(resume_pdf)

        # Print keywords / 키워드 출력
        print("\n📄 Keywords found in your resume:")
        print(", ".join(keywords))
        print("\n🔗 Google job search links:")
        for kw in keywords: # Print Google job search links / 구글 직업 검색 링크 출력
            print(f"- {kw}: {google_job_url(kw)}") 

    except FileNotFoundError: # If file not found / 파일을 찾을 수 없는 경우
        print(f"❌ Could not find file: {resume_pdf}")
    except Exception as e: # If error occurred / 오류 발생 시
        print(f"❌ Error occurred: {e}")
