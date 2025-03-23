📄 Resume-Based Job Matcher (Python)
This is a simple Python script that extracts technical keywords from a resume PDF and checks which ones are present. It's the first step in building a smart job-matching system.

✅ Features
Extracts keywords from any PDF resume
Checks presence of key tech terms (e.g. Python, JavaScript, AWS)
Prints out what's found and what's missing
CLI-based and easy to use

📌 Usage
Place your resume PDF in the root folder.
Rename it to resume.pdf or change the name in the code.
Run:
python job_matcher.py
🛠️ Tech Stack
This project is built using the following technologies:

📄 Frontend
HTML5 – Page structure and file upload form
CSS3 – Basic styling (optionally extendable with Bootstrap)
Jinja2 – Flask templating engine for dynamic rendering


⚙️ Backend
Python 3.13 – Core language
Flask – Lightweight web framework for routing and rendering
pdfplumber – Extracts text from uploaded PDF resumes
re (Regex) – Matches technical keywords from resume
io.BytesIO – Handles in-memory file streams (useful in serverless environments)


🔍 Core Logic Features
Extracts technical keywords from uploaded PDF
Maps keywords to relevant job roles using a predefined dictionary
Generates Google search links based on suggested job titles


☁️ Deployment
Vercel
Serverless deployment of Flask app
File uploads handled using memory (no filesystem access)
Great for lightweight, scalable web services


💡 Future Improvements
Add login & profile saving features
Integrate with job search APIs (e.g., Indeed, LinkedIn)
Use AI for smarter keyword-role-job matching
Save job matches or portfolios for later reference
Made with ❤️ and Python 3.13 by Jinsung ParkS
