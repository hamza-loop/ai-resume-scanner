import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from docx import Document
from groq import Groq
from pydantic import BaseModel as BaseModel1
from pypdf import PdfReader

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

job_description = """
Hamza Info Tech is seeking a proactive Security Engineer to protect our cloud infrastructure, networks, and applications. You will build automated defenses, manage vulnerabilities, respond to incidents, and partner with developers to embed security across our engineering lifecycle.

Key Responsibilities

• Infrastructure & Cloud Security: Secure our cloud environment ([AWS/Azure/GCP]), networks, and endpoints using IAM, firewalls, and encryption.
• Vulnerability & Threat Management: Run vulnerability scans, coordinate penetration tests, and monitor SIEM alerts to detect and fix security gaps.
• Incident Response: Investigate security incidents, lead containment efforts, and perform root-cause analysis.
• Security Automation: Develop scripts (Python/Bash) to automate threat detection and routine security workflows.
• AppSec Collaboration: Guide software and DevOps teams at Hamza Info Tech on secure coding practices and CI/CD security.

Qualifications

• Experience: [3+] years in cybersecurity, cloud security, or infrastructure engineering.
• Core Skills: Strong knowledge of networking (TCP/IP, DNS), Linux/Windows security, OWASP Top 10, and cloud platforms.
• Coding: Proficiency in Python, Bash, or Go for security automation.
• Bonus: Familiarity with Kubernetes, Terraform, SOC 2 / ISO 27001, or certifications like Security+, CISSP, or AWS Security.

Why Join Hamza Info Tech?

• Competitive compensation and comprehensive health benefits
• Flexible work model and dedicated budget for certifications
• High-impact role in a fast-growing, engineering-first team
"""

class JobDescription(BaseModel1):
    role: str
    required_skills: list[str]
    preferred_skills: list[str]
    minimum_experience: float | None = None
    educational_expectations: str | None = None
    responsibilities: list[str]

class Exprience(BaseModel1):
    company: str | None = None
    role: str | None = None
    deuration: str | None = None
    discription: str | None = None
    skills_used: list[str] | None = None

class Resume(BaseModel1):
    name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    total_experience_year: float | None = None
    skills: list[str] = []
    experience: list[Exprience] = []
    projects: list[str] = []
    cartificate: list[str] = []

class MatchResult(BaseModel1):
    candidate_name: str | None = None
    matching_skills: list[str] = []
    missing_important_skills: list[str] = []
    experience_requirement_met: bool
    score: float
    details: str

jobd_schema = JobDescription.model_json_schema()

system_prompt = f"""
you are an expert HR assistant.

your job is to analyze the job description and extract the relevant information based on this schema, return only valid json maching this schema. Do not add any extra information or explanation.
{jobd_schema}

IMPORTANT: 
Do not return the schema itself.
Do not return field like "properties" or "type" or "required" or "description" in the output.
Do not return any extra information or explanation.

fill the schema with actual information extracted from the job description. If a field is not present in the job description, return null for that field. Do not invent information
"""

user_prompt = f"""
analyze the following job description and extract the relevant information based on the schema provided in the system prompt. Return only valid JSON matching the schema. Do not add any extra information or explanation.
{job_description}
"""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format={"type": "json_object"}
)

job_data = json.loads(response.choices[0].message.content)
job = JobDescription(**job_data)

print("Minimum Experience:", job.minimum_experience)
print("Educational Expectations:", job.educational_expectations)

resume_schema = Resume.model_json_schema()

def final_score(job, resume):
    match_schema = MatchResult.model_json_schema()
    prompt = f"""
    you are an expert HR recruiter.
    compare the candidate's resume with job description 

    Job Description: {job.model_dump_json(indent=2)}
    Candidate Resume: {resume.model_dump_json(indent=2)}
    Return a JSON object matching this schema: {match_schema}

    Give me:
    1. Candidate name 
    2. Matching skills
    3. Missing important skills
    4. Whether experience requirement is met
    5. Overall match percentage between 0 to 100 in the 'score' field
    6. A short final verdict on whether the candidate is suitable for the role in the 'details' field.

    keep the response concise and easy to understand.
    """
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    data = json.loads(response.choices[0].message.content)
    return MatchResult(**data)

def parse_resume(resume_text):
    system_prompt = f"""
    you are an expert resume parser.
    Extract the relevant information based on its meaning, not only based on exact section headings.
    Different resumes may have different section headings such as Experience, Work Experience, Professional Experience, Work History, Employment, Projects, or Internships.

    Skills may also appear in the skills section, work experience, projects, internships, education, or certifications.

    Return only valid JSON matching this schema:
    {resume_schema}

    IMPORTANT Rules:
    1. Do not invent information. If a field is not present in the resume, return null for that field.
    2. If a list field is empty, return an empty list.
    3. Include internship experience in the experience list.
    4. Extract skills mentioned in the resume, even if they are not in a dedicated skills section.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Parse the following resume:\n\n{resume_text}"}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"}
    )
    data = json.loads(response.choices[0].message.content)
    return Resume(**data)

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def read_docx(file_path):
    document = Document(file_path)
    text = ""
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"
    
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    text += cell.text + "\n"
    return text

def read_resume(file_path):
    if file_path.suffix.lower() == ".pdf":
        return read_pdf(file_path)
    elif file_path.suffix.lower() == ".docx":
        return read_docx(file_path)
    else:
        return None

# Direct file path execution
file_path = Path("sample_resume.pdf")

if file_path.exists() and file_path.suffix.lower() in [".pdf", ".docx"]:
    print("\nProcessing:", file_path.name)
    resume_text = read_resume(file_path)
    
    parsed_resume = parse_resume(resume_text)
    time.sleep(5)
    
    result = final_score(job, parsed_resume)
    time.sleep(5)
    
    print("\n--- EVALUATION RESULT ---")
    print("Candidate:", parsed_resume.name)
    print("Score:", result.score, "%")
    print("Experience Met:", result.experience_requirement_met)
    print("Matching Skills:", ", ".join(result.matching_skills))
    print("Missing Skills:", ", ".join(result.missing_important_skills))
    print("Verdict:", result.details)
else:
    print(f"File not found or unsupported format: {file_path}")
