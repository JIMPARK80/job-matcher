from io import BytesIO  # BytesIO: A stream implementation using an in-memory bytes buffer
import pdfplumber # pdfplumber: A tool for extracting text and images from PDFs
import re # re: Regular expression operations

# 1. Technical Keywords Extraction Function / 기술 키워드 추출 함수 
def extract_keywords_from_resume(file_stream): # PDF 경로
    with pdfplumber.open(BytesIO(file_stream)) as pdf: # Open PDF / PDF 열기
        text = '' # Initialize text / 텍스트 초기화
        for page in pdf.pages: # Loop through each page / 각 페이지 반복
            page_text = page.extract_text() # Extract text from page / 페이지에서 텍스트 추출
            if page_text: # If text exists / 텍스트가 있는 경우
                text += page_text # Append text / 텍스트 추가

    tech_keywords = [ 
        'JavaScript', 'React', 'Python', 'Java', 'HTML', 'CSS', 'Node.js', 'SQL', 'AWS',
        'Docker', 'Kubernetes', 'Spring', 'Hibernate', 'Django', 'MongoDB', 'Angular', 'Bootstrap',
        'Vue.js', 'Flask', 'REST', 'API', 'Git', 'CI/CD', 'Jenkins', 'Agile', 'Scrum', 'Kanban',
        'TDD', 'C++', 'C#', 'Ruby', 'PHP', 'Swift', 'Objective-C', 'Unity', 'TensorFlow', 'PyTorch',
        'Unreal Engine', 'Machine Learning', 'Deep Learning', 'Computer Vision', 'NLP', 'Big Data',
    
    ] # List of technical keywords / 기술 키워드 목록

    # improved accurarcy: using word boundaries  / 정확도 개선: 단어 경계 사용
    keywords_found = [
        keyword for keyword in tech_keywords 
        if re.search(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE)
    ] # Extract keywords from text / 텍스트에서 키워드 추출

    return keywords_found # Return keywords / 키워드 반환

keyword_to_roles = {
    "JavaScript": ["Frontend Developer", "Web Developer"],
    "React": ["Frontend Developer", "UI Engineer"],
    "Python": ["Backend Developer", "Data Analyst", "ML Engineer"],
    "Java": ["Backend Developer", "Android Developer"],
    "HTML": ["Frontend Developer", "Web Developer"],
    "CSS": ["Frontend Developer", "UI Developer"],
    "Node.js": ["Full Stack Developer", "Backend Developer"],
    "SQL": ["Data Analyst", "Database Developer", "BI Developer"],
    "AWS": ["Cloud Engineer", "DevOps Engineer"],
    "Docker": ["DevOps Engineer", "Cloud Architect"],
    "Kubernetes": ["DevOps Engineer", "Cloud Engineer"],
    "Spring": ["Java Developer", "Backend Developer"],
    "Hibernate": ["Java Developer", "Backend Developer"],
    "Django": ["Backend Developer", "Python Developer"],
    "MongoDB": ["Backend Developer", "Database Engineer"],
    "Angular": ["Frontend Developer", "UI Engineer"],
    "Bootstrap": ["Frontend Developer", "UI Engineer"],
    "Vue.js": ["Frontend Developer"],
    "Flask": ["Backend Developer", "Python Developer"],
    "REST": ["Backend Developer", "API Developer"],
    "API": ["API Developer", "Software Engineer"],
    "Git": ["Software Developer", "Version Control Specialist"],
    "CI/CD": ["DevOps Engineer", "Automation Engineer"],
    "Jenkins": ["DevOps Engineer", "CI/CD Engineer"],
    "Agile": ["Scrum Master", "Project Manager", "Agile Coach"],
    "Scrum": ["Scrum Master", "Agile Facilitator"],
    "Kanban": ["Project Manager", "Scrum Master"],
    "TDD": ["Software Engineer", "QA Engineer"],
    "C++": ["Embedded Developer", "Game Developer", "Software Engineer"],
    "C#": ["Game Developer", ".NET Developer"],
    "Ruby": ["Web Developer", "Backend Developer"],
    "PHP": ["Web Developer", "Backend Developer"],
    "Swift": ["iOS Developer"],
    "Objective-C": ["iOS Developer"],
    "Unity": ["Game Developer", "XR Developer"],
    "TensorFlow": ["ML Engineer", "Deep Learning Engineer"],
    "PyTorch": ["ML Engineer", "Deep Learning Engineer"],
    "Unreal Engine": ["Game Developer", "3D Simulation Developer"],
    "Machine Learning": ["ML Engineer", "AI Researcher"],
    "Deep Learning": ["Deep Learning Engineer", "AI Researcher"],
    "Computer Vision": ["Computer Vision Engineer", "AI Developer"],
    "NLP": ["NLP Engineer", "AI Researcher"],
    "Big Data": ["Data Engineer", "Data Scientist"]
}



# 2. Create a Google Search link / 구글 검색 링크 생성
def google_job_urls_from_roles(matched_roles, location="Toronto"):
    job_links = []
    for roles in matched_roles.values():
        for role in roles:
            query = f"{role} job in {location}"
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            job_links.append((role, url))
    return job_links


# 3. Main run / 메인 실행
if __name__ == "__main__":
    resume_pdf = "PDF/resume.pdf"  # PDF path / PDF 경로

    try: # Try to extract keywords / 키워드 추출 시
        keywords = extract_keywords_from_resume(resume_pdf)

        # Print keywords / 키워드 출력
        print("\n📄 Keywords found in your resume:")
        print(", ".join(keywords))
        
        # Suggested roles per keyword / 키워드 별 제안된 역할
        print("\n💼 Suggested roles per keyword:")
        for kw in keywords:
            roles = keyword_to_roles.get(kw, ["(No specific match)"])
            print(f"- {kw}: {', '.join(roles)}")

        # Google links / 구글 링크
        print("\n🔗 Google job search links:")
        for kw in keywords: # Print Google job search links / 구글 직업 검색 링크 출력
            print(f"- {kw}: {google_job_urls_from_roles(kw)}") 

    except FileNotFoundError: # If file not found / 파일을 찾을 수 없는 경우
        print(f"❌ Could not find file: {resume_pdf}")
    except Exception as e: # If error occurred / 오류 발생 시
        print(f"❌ Error occurred: {e}")

