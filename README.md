# AI Resume Scanner

### AI-Powered Resume Screening and Job Matching System

AI Resume Scanner is a Python-based application designed to automate resume analysis and candidate evaluation against job descriptions using Large Language Models (LLMs).

The system extracts structured information from resumes, analyzes job requirements, identifies skill gaps, and generates an AI-based candidate matching score.

## Key Features

- **Intelligent Resume Parsing:** Extract candidate information, skills, professional experience, projects, and certifications.
- **Job Description Analysis:** Identify required skills, preferred qualifications, responsibilities, and experience requirements.
- **AI-Powered Matching:** Compare candidate qualifications with job requirements.
- **Skill Gap Analysis:** Identify matching skills and missing important skills.
- **Candidate Evaluation:** Generate an estimated compatibility score between 0 and 100.
- **Multiple Document Formats:** Support for PDF and DOCX resume files.
- **Structured Data Extraction:** Use Pydantic models to validate and organize extracted information.
- **Automated Assessment:** Generate a concise evaluation of candidate suitability.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Large Language Models (LLMs) | Resume analysis and intelligent matching |
| Pydantic | Structured data validation |
| PyPDF | PDF text extraction |
| python-docx | DOCX document processing |
| python-dotenv | Environment variable management |

## Project Workflow

The application follows a structured resume evaluation pipeline:

1. **Job Description Processing:** Extract relevant information, skills, qualifications, and responsibilities.
2. **Resume Extraction:** Read and extract text from PDF or DOCX files.
3. **Information Parsing:** Convert unstructured resume content into structured candidate information.
4. **Skill Analysis:** Identify candidate skills and professional experience.
5. **Matching & Evaluation:** Compare the parsed resume against job requirements.
6. **Final Assessment:** Generate a matching score, missing skills, and candidate suitability evaluation.

## Project Structure

```text
ai-resume-scanner/
│
├── ai_resume_scanner.py
├── README.md
├── requirements.txt
├── .gitignore
└── .env
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/hamza-loop/ai-resume-scanner.git

cd ai-resume-scanner
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate the environment:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project directory and configure the API credentials required by the current LLM integration.

Keep API credentials private. Never upload your `.env` file to GitHub.

### 5. Add a Resume

Place a resume named `sample_resume.pdf` in the project directory.

The application currently supports PDF and DOCX document parsing.

### 6. Run the Application

```bash
python3 ai_resume_scanner.py
```

The application processes the configured job description and resume, then displays the evaluation results in the terminal.

## Sample Evaluation Output

The application generates the following information:

```text
--- EVALUATION RESULT ---

Candidate: Candidate Name

Score: 85%

Experience Met: False

Matching Skills:
Python, Networking, Linux

Missing Skills:
Cloud Security, Kubernetes

Verdict:
Candidate demonstrates relevant technical
skills but does not fully meet the experience
requirements.
```

*Illustrative output only.*

## Current Limitations

- Processes one configured resume at a time.
- Job descriptions are currently defined within the Python source code.
- Resume input currently uses a predefined file path.
- Matching scores are AI-generated estimates and may require human verification.
- Image-based PDFs may require additional OCR functionality.
- Requires an external LLM API integration.

## Future Improvements

- [ ] Interactive web interface using Streamlit.
- [ ] Support for multiple resume uploads.
- [ ] Dynamic job description input.
- [ ] Provider-independent LLM integration.
- [ ] Improved candidate scoring and evaluation.
- [ ] Downloadable candidate assessment reports.
- [ ] Unit testing and improved error handling.
- [ ] Resume comparison and candidate ranking.

## Project Objective

The objective of this project is to explore how Artificial Intelligence and Large Language Models can automate document understanding, information extraction, and intelligent candidate evaluation.

It demonstrates the practical application of Python, structured data validation, document processing, and LLM-based analysis in an HR technology use case.

## Author

**Md Hamza**

B.Tech Computer Science & Engineering (Artificial Intelligence)

Jamia Hamdard University

- GitHub: [@hamza-loop](https://github.com/hamza-loop)
- Project Repository: [AI Resume Scanner](https://github.com/hamza-loop/ai-resume-scanner)

## Disclaimer

This project is developed for educational and experimental purposes. AI-generated scores and candidate evaluations should not be considered definitive hiring decisions. Human review is recommended for all recruitment decisions.
