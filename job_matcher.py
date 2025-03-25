from io import BytesIO  # BytesIO: A stream implementation using an in-memory bytes buffer
import pdfplumber # pdfplumber: A tool for extracting text and images from PDFs
import re # re: Regular expression operations
from serpapi import GoogleSearch # serpapi: A Python client for SerpApi
import os # os: Miscellaneous operating system interfaces
from collections import Counter # Counter: A dict subclass for counting hashable objects


# API Key는 환경변수 또는 config 파일로 관리 권장
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "5d7dfa49adb35300690962c2996ad37aebeaf8e3c66d89fc8eddff5aa9d1d117")

def search_google_jobs(query, location="Toronto"):
    params = {
        "q": f"{query} jobs in {location}",
        "location": location,
        "hl": "en",
        "api_key": SERPAPI_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    print("[DEBUG] SERPAPI 응답 구조:")
    import pprint; pprint.pprint(results)

    # 아래는 fallback 로직 포함
    if "jobs_results" in results:
        return results["jobs_results"]
    elif "organic_results" in results:
        return results["organic_results"]
    else:
        return []

def extract_text_from_pdf(input_data):
    with pdfplumber.open(BytesIO(input_data)) as pdf:
        text = ''
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def extract_profile_info(text):
    import re
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone_match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
    linkedin_match = re.search(r"(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9-_]+", text)

    return {
        "email": email_match.group(0) if email_match else "",
        "phone": phone_match.group(0) if phone_match else "",
        "linkedin": linkedin_match.group(0) if linkedin_match else ""
    }


# 1. Technical Keywords Extraction Function / 기술 키워드 추출 함수 
def extract_keywords_from_resume(input_data, is_pdf=True):
    try:
        with pdfplumber.open(BytesIO(input_data)) as pdf:
            text = ''
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"[PDF Error] {e}")
        raise

        
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
    "javascript": ["Frontend Developer", "Web Developer"],
    "react": ["Frontend Developer", "UI Engineer"],
    "python": ["Backend Developer", "Data Analyst", "ML Engineer"],
    "java": ["Backend Developer", "Android Developer"],
    "html": ["Frontend Developer", "Web Developer"],
    "css": ["Frontend Developer", "UI Developer"],
    "node.js": ["Full Stack Developer", "Backend Developer"],
    "sql": ["Data Analyst", "Database Developer", "BI Developer"],
    "aws": ["Cloud Engineer", "DevOps Engineer"],
    "docker": ["DevOps Engineer", "Cloud Architect"],
    "kubernetes": ["DevOps Engineer", "Cloud Engineer"],
    "spring": ["Java Developer", "Backend Developer"],
    "hibernate": ["Java Developer", "Backend Developer"],
    "django": ["Backend Developer", "Python Developer"],
    "mongodb": ["Backend Developer", "Database Engineer"],
    "angular": ["Frontend Developer", "UI Engineer"],
    "bootstrap": ["Frontend Developer", "UI Engineer"],
    "vue.js": ["Frontend Developer"],
    "flask": ["Backend Developer", "Python Developer"],
    "rest": ["Backend Developer", "API Developer"],
    "api": ["API Developer", "Software Engineer"],
    "git": ["Software Developer", "Version Control Specialist"],
    "ci/cd": ["DevOps Engineer", "Automation Engineer"],
    "jenkins": ["DevOps Engineer", "CI/CD Engineer"],
    "agile": ["Scrum Master", "Project Manager", "Agile Coach"],
    "scrum": ["Scrum Master", "Agile Facilitator"],
    "kanban": ["Project Manager", "Scrum Master"],
    "tdd": ["Software Engineer", "QA Engineer"],
    "c++": ["Embedded Developer", "Game Developer", "Software Engineer"],
    "c#": ["Game Developer", ".NET Developer"],
    "ruby": ["Web Developer", "Backend Developer"],
    "php": ["Web Developer", "Backend Developer"],
    "swift": ["iOS Developer"],
    "objective-c": ["iOS Developer"],
    "unity": ["Game Developer", "XR Developer"],
    "tensorflow": ["ML Engineer", "Deep Learning Engineer"],
    "pytorch": ["ML Engineer", "Deep Learning Engineer"],
    "unreal engine": ["Game Developer", "3D Simulation Developer"],
    "machine learning": ["ML Engineer", "AI Researcher"],
    "deep learning": ["Deep Learning Engineer", "AI Researcher"],
    "computer vision": ["Computer Vision Engineer", "AI Developer"],
    "nlp": ["NLP Engineer", "AI Researcher"],
    "big data": ["Data Engineer", "Data Scientist"],
    "figma": ["UI/UX Designer", "Web Designer"],
    "photoshop": ["Graphic Designer", "UI/UX Designer"],
    "illustrator": ["Graphic Designer", "UI/UX Designer"],
    "catia": ["Optical Design Engineer"],
    "speos": ["Optical Design Engineer"],
    "jira": ["QA Tester", "Project Coordinator"],
    "trello": ["Project Coordinator"],
    "problem-solving": ["QA Tester", "Software Developer"]
}


# 1-2. Match Roles with Priority / 역할과 우선순위 매칭
def match_roles_with_priority(keywords):
    all_roles = []
    matched_roles = {}
    
    for kw in keywords:
        kw_lower = kw.lower()
        roles = keyword_to_roles.get(kw_lower, [])
        matched_roles[kw_lower] = roles
        all_roles.extend(roles)

    role_counter = Counter(all_roles)
    top_3_roles = [role for role, _ in role_counter.most_common(3)]
    unique_roles = sorted(set(all_roles ))
    return matched_roles, unique_roles, top_3_roles


# 2. Create a Google Search link / 구글 검색 링크 생성
def google_job_urls_from_roles(matched_roles, location="Toronto"):
    job_links = []
    for roles in matched_roles.values():
        for role in roles:
            query = f"{role} job in {location}"
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            job_links.append((role, url))
    return job_links



