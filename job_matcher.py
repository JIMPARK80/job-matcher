print("hello world")


import pdfplumber # Extracts text from PDF files / PDF에서 텍스트 찾는 모듈
import requests # Send HTTP requests / HTTP 요청을 보내는 모듈
from bs4 import BeautifulSoup # Parses HTML / HTML을 파싱하는 모듈
import re # regex support / 정규식 지원

def extract_keywords_from_resume(pdf_path): # 이력서에서 기술 키워드 추출
    with pdfplumber.open(pdf_path) as pdf: # open the PDF file / PDF 파일을 열고
        text = '' # initialize the text variable / 텍스트 변수 초기화
        for page in pdf.pages: # iterate over the pages / 페이지를 반복
            page_text = page.extract_text() # extract text from the page / 페이지에서 텍스트 추출
            if page_text:
                text += page_text # Combine all text / 모든 텍스트 결합
    
    tech_keywords = [ 
        'JavaScript', 'React', 'Python', 'Django', 'Java', 'Spring', 
        'SQL', 'AWS', 'Docker', 'Kubernetes' , 'HTML', 'CSS', 'Node.js',
        'TypeScript', 'Angular', 'Vue.js', 'Flask', 'REST', 'API', 'Git', 'CI/CD'
    ] # List of tech keywords / 기술 키워드 목록

    # Check if each keyword is present in the text / 각 키워드가 텍스트에 있는지 확인
    keywords_found = {keyword: bool(re.search(re.escape(keyword), text, re.IGNORECASE)) for keyword in tech_keywords} 
    # Check if the keyword is found in the text / 키워드가 텍스트에 있는지 확인
    
    return keywords_found # Return the matched keywords / 일치하는 키워드 반환


if __name__ == "__main__": # Run the code if the script is executed / 스크립트가 실행되면 코드 실행
    resume_pdf = "PDF/resume.pdf" # Path to the resume PDF / 이력서 PDF 경로
    print("📁 Trying to open:", resume_pdf) # Print resume file / 이력서 파일 출력   
    result = extract_keywords_from_resume(resume_pdf) # Extract keywords from the resume / 이력서에서 키워드 추출
    
    print("\n keywords found in resume: ") # Print the keywords found in the resume / 이력서에서 찾은 키워드 출력
    for keyword, found in result.items(): # Iterate over the keywords / 키워드 반복
        status = "OK" if found else "Not Found" # Check if the keyword is found / 키워드가 있는지 확인
        print(f"{status}: {keyword}") # Print the status and the keyword / 상태와 키워드 출력