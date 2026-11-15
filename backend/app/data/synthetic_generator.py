import os
import json
from fpdf import FPDF
import docx
from docx.shared import Pt, Inches, RGBColor

TEST_RESUMES_DIR = os.path.join(os.path.dirname(__file__), "test_resumes")
os.makedirs(TEST_RESUMES_DIR, exist_ok=True)

SAMPLE_JD = """Title: Senior Backend Engineer (Python / FastAPI)
Company: CloudScale Technologies
Location: Remote (US / Global)
Experience Required: 4+ years of relevant backend software engineering experience
Education: Bachelor's or Master's degree in Computer Science, Software Engineering, or related technical field

About the Role:
We are seeking an experienced Senior Backend Engineer to architect, build, and scale our high-throughput distributed microservices. You will lead API design, optimize database queries, implement asynchronous worker pipelines, and maintain CI/CD and cloud deployment infrastructure.

Key Requirements:
- 4+ years of professional backend software development experience.
- Strong proficiency in Python 3 and modern async frameworks (FastAPI or Flask).
- Deep experience with relational databases, specifically PostgreSQL, query optimization, and schema design.
- Hands-on experience with containerization using Docker and orchestration with Kubernetes.
- Practical experience with cloud infrastructure, particularly Amazon Web Services (AWS) or Google Cloud Platform (GCP).
- Proven track record building and securing scalable REST APIs and microservice architectures.
- Solid understanding of Git version control, unit testing (pytest), and CI/CD automation pipelines.

Preferred / Bonus Skills:
- Experience with Redis caching and asynchronous messaging (RabbitMQ or Kafka).
- Familiarity with frontend frameworks (React or Next.js) for full-stack collaboration.
"""

CANDIDATES = [
    {
        "id": "cand_01",
        "name": "Alex Morgan",
        "filename": "Alex_Morgan_Resume.pdf",
        "format": "pdf",
        "layout": "standard",
        "expected_rank": 1,
        "email": "alex.morgan@email.com",
        "phone": "(555) 234-5678",
        "title": "Senior Backend Engineer",
        "degree": "Master of Science in Computer Science",
        "total_years": 6.5,
        "relevant_years": 6.5,
        "skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS", "REST API", "Git", "Redis", "CI/CD", "Linux", "Microservices"],
        "summary": "Accomplished Senior Backend Engineer with 6.5 years designing high-throughput distributed architectures, REST APIs, and asynchronous microservices using Python and FastAPI.",
        "experience": [
            {
                "role": "Lead Backend Engineer",
                "company": "DataStream Inc",
                "dates": "Jan 2021 - Present",
                "bullets": [
                    "Architected and deployed 12 microservices using FastAPI and PostgreSQL handling 25,000 requests per second.",
                    "Containerized services with Docker and managed deployment pipelines on Amazon Web Services (AWS) using ECS and Lambda.",
                    "Implemented Redis distributed caching layer cutting database query latency by 45% across core endpoints.",
                    "Mentored junior engineers and led code reviews adhering to strict pytest unit testing standards."
                ]
            },
            {
                "role": "Backend Software Developer",
                "company": "Nexus Web Systems",
                "dates": "Jun 2018 - Dec 2020",
                "bullets": [
                    "Developed high-volume REST APIs in Python using Flask and PostgreSQL with SQLAlchemy ORM.",
                    "Automated deployment processes with GitHub Actions CI/CD and Docker containers.",
                    "Optimized complex SQL queries and database indexes, improving report generation speeds by 3x."
                ]
            }
        ]
    },
    {
        "id": "cand_02",
        "name": "Sarah Chen",
        "filename": "Sarah_Chen_Resume.pdf",
        "format": "pdf",
        "layout": "standard",
        "expected_rank": 2,
        "email": "sarah.chen@techmail.com",
        "phone": "(555) 345-6789",
        "title": "Senior Full-Stack Engineer",
        "degree": "Bachelor of Science in Computer Science",
        "total_years": 5.2,
        "relevant_years": 5.2,
        "skills": ["Python", "FastAPI", "React", "PostgreSQL", "Docker", "REST API", "Git", "TypeScript", "Tailwind CSS"],
        "summary": "Versatile Full-Stack Engineer with 5.2 years building end-to-end web applications, scalable Python backend services, and dynamic React frontends.",
        "experience": [
            {
                "role": "Senior Full-Stack Developer",
                "company": "Fintech Solutions Ltd",
                "dates": "Mar 2021 - Present",
                "bullets": [
                    "Built secure transaction processing backend using Python FastAPI and PostgreSQL database with ACID compliance.",
                    "Engineered modern responsive customer dashboard in React with TypeScript and Tailwind CSS.",
                    "Containerized all full-stack applications with Docker and established automated testing with pytest and Jest."
                ]
            },
            {
                "role": "Software Engineer",
                "company": "BrightApps Studio",
                "dates": "Jan 2019 - Feb 2021",
                "bullets": [
                    "Designed RESTful APIs in Python and integrated third-party payment gateways (Stripe, Plaid).",
                    "Maintained PostgreSQL schemas and performed query optimization for real-time reporting."
                ]
            }
        ]
    },
    {
        "id": "cand_03",
        "name": "David Kumar",
        "filename": "David_Kumar_Resume.pdf",
        "format": "pdf",
        "layout": "two_column",
        "expected_rank": 3,
        "email": "david.kumar@inbox.org",
        "phone": "(555) 456-7890",
        "title": "Mid-Level Backend Developer",
        "degree": "Bachelor of Technology in Information Technology",
        "total_years": 3.8,
        "relevant_years": 3.8,
        "skills": ["Python", "Django", "FastAPI", "PostgreSQL", "Docker", "Git", "REST API", "Linux"],
        "summary": "Backend developer with 3.8 years constructing resilient backend systems in Python, migrating legacy Django monoliths to async FastAPI services.",
        "experience": [
            {
                "role": "Backend Developer",
                "company": "Apex Software Labs",
                "dates": "Jul 2021 - Present",
                "bullets": [
                    "Migrated legacy Django services to async FastAPI microservices, increasing throughput by 60%.",
                    "Wrote complex PostgreSQL stored procedures and optimized database schema migrations.",
                    "Configured Docker containers for local development and staging environments."
                ]
            },
            {
                "role": "Junior Backend Developer",
                "company": "CloudForge",
                "dates": "May 2020 - Jun 2021",
                "bullets": [
                    "Maintained REST APIs and wrote unit tests using pytest with 85% test coverage.",
                    "Resolved production bugs and collaborated on Git version-controlled release branches."
                ]
            }
        ]
    },
    {
        "id": "cand_04",
        "name": "Marcus Vance",
        "filename": "Marcus_Vance_Resume.docx",
        "format": "docx",
        "layout": "standard",
        "expected_rank": 4,
        "email": "m.vance@cloudops.net",
        "phone": "(555) 567-8901",
        "title": "Cloud DevOps Engineer",
        "degree": "Bachelor of Science in Computer Systems",
        "total_years": 5.0,
        "relevant_years": 4.0,
        "skills": ["AWS", "Docker", "Kubernetes", "Python", "Terraform", "CI/CD", "Linux", "Bash", "Git"],
        "summary": "DevOps Engineer specializing in AWS cloud infrastructure, Kubernetes orchestration, and automated CI/CD pipelines with strong Python scripting expertise.",
        "experience": [
            {
                "role": "Senior DevOps Engineer",
                "company": "SkyHigh Cloud Systems",
                "dates": "Jan 2021 - Present",
                "bullets": [
                    "Managed AWS cloud infrastructure (EKS, EC2, RDS, S3) using Terraform Infrastructure as Code (IaC).",
                    "Orchestrated Docker microservices on Kubernetes clusters supporting 50+ enterprise clients.",
                    "Automated deployment workflows with GitHub Actions CI/CD, reducing deployment cycle times from hours to minutes."
                ]
            },
            {
                "role": "Site Reliability Engineer",
                "company": "InfraNet Global",
                "dates": "Jan 2019 - Dec 2020",
                "bullets": [
                    "Wrote Python automation scripts for server monitoring, log aggregation, and anomaly alerting.",
                    "Maintained Linux Ubuntu server farms and configured Nginx reverse proxies."
                ]
            }
        ]
    },
    {
        "id": "cand_05",
        "name": "Elena Rostova",
        "filename": "Elena_Rostova_Resume.pdf",
        "format": "pdf",
        "layout": "standard",
        "expected_rank": 5,
        "email": "elena.rostova@devmail.io",
        "phone": "(555) 678-9012",
        "title": "Frontend Software Engineer",
        "degree": "Bachelor of Science in Software Engineering",
        "total_years": 4.2,
        "relevant_years": 2.0,
        "skills": ["React", "JavaScript", "TypeScript", "Next.js", "Redux", "Tailwind CSS", "HTML5", "CSS3", "REST API", "Git"],
        "summary": "Passionate Frontend Developer with 4.2 years specializing in responsive single-page applications, UI state management with Redux, and React components.",
        "experience": [
            {
                "role": "Frontend Developer",
                "company": "Vivid Interfaces",
                "dates": "Feb 2021 - Present",
                "bullets": [
                    "Engineered modern web UI with React, Next.js, and TypeScript serving 100k daily active users.",
                    "Integrated REST APIs and WebSockets for real-time analytics dashboards.",
                    "Wrote automated end-to-end tests using Cypress and unit tests using Jest."
                ]
            },
            {
                "role": "Junior Web Developer",
                "company": "PixelCraft Studios",
                "dates": "Jan 2020 - Jan 2021",
                "bullets": [
                    "Developed interactive landing pages using JavaScript, HTML5, and CSS3 / Tailwind CSS.",
                    "Collaborated with backend engineers to consume RESTful endpoints."
                ]
            }
        ]
    },
    {
        "id": "cand_06",
        "name": "Brian O'Connor",
        "filename": "Brian_OConnor_Resume.pdf",
        "format": "pdf",
        "layout": "table",
        "expected_rank": 6,
        "email": "brian.oconnor@datalab.org",
        "phone": "(555) 789-0123",
        "title": "Data Engineer",
        "degree": "Master of Science in Data Analytics",
        "total_years": 3.5,
        "relevant_years": 3.0,
        "skills": ["Python", "SQL", "PostgreSQL", "Pandas", "NumPy", "Docker", "Git", "Linux", "Apache Spark"],
        "summary": "Data Engineer focused on ETL pipeline construction, data warehouse modeling, and analytical API services utilizing Python and PostgreSQL.",
        "experience": [
            {
                "role": "Data Engineer",
                "company": "Insight Data Partners",
                "dates": "Oct 2021 - Present",
                "bullets": [
                    "Built ETL data ingestion pipelines using Python, Pandas, and PostgreSQL processing 5M records daily.",
                    "Containerized batch processing jobs with Docker and scheduled tasks with Apache Airflow.",
                    "Wrote high-performance SQL analytical queries and built data marts for business intelligence."
                ]
            },
            {
                "role": "Junior Data Analyst",
                "company": "Metrics Pulse",
                "dates": "May 2020 - Sep 2021",
                "bullets": [
                    "Cleaned and structured unstructured datasets in Python using NumPy and Pandas.",
                    "Maintained relational database schemas in PostgreSQL and generated weekly KPI reports."
                ]
            }
        ]
    },
    {
        "id": "cand_07",
        "name": "Priya Sharma",
        "filename": "Priya_Sharma_Resume.docx",
        "format": "docx",
        "layout": "standard",
        "expected_rank": 7,
        "email": "priya.sharma@youngdev.io",
        "phone": "(555) 890-1234",
        "title": "Junior Python Developer",
        "degree": "Bachelor of Science in Computer Science",
        "total_years": 1.8,
        "relevant_years": 1.8,
        "skills": ["Python", "FastAPI", "SQLite", "Git", "REST API", "pytest", "Docker"],
        "summary": "Energetic Junior Python Developer with 1.8 years building microservices and REST APIs with FastAPI, seeking to accelerate backend engineering skills.",
        "experience": [
            {
                "role": "Junior Backend Developer",
                "company": "Sprout Tech Labs",
                "dates": "Jul 2022 - Present",
                "bullets": [
                    "Assisted in developing REST APIs in Python using FastAPI and SQLite.",
                    "Created automated test cases with pytest and maintained Git repository branches.",
                    "Packaged microservice components into Docker images for testing."
                ]
            }
        ]
    },
    {
        "id": "cand_08",
        "name": "James Wilson",
        "filename": "James_Wilson_Resume.pdf",
        "format": "pdf",
        "layout": "standard",
        "expected_rank": 8,
        "email": "j.wilson@enterprisecode.com",
        "phone": "(555) 901-2345",
        "title": "Senior Java Developer",
        "degree": "Bachelor of Science in Computer Science",
        "total_years": 6.2,
        "relevant_years": 2.5,
        "skills": ["Java", "Spring Boot", "MySQL", "Microservices", "REST API", "Docker", "Git", "Hibernate"],
        "summary": "Enterprise Java Developer with 6.2 years creating enterprise software architectures, RESTful services, and microservices in Spring Boot and MySQL.",
        "experience": [
            {
                "role": "Senior Java Engineer",
                "company": "Apex Financial Systems",
                "dates": "Feb 2020 - Present",
                "bullets": [
                    "Designed distributed banking microservices using Java 17 and Spring Boot.",
                    "Configured MySQL relational databases with Hibernate ORM.",
                    "Built secure REST APIs and containerized applications with Docker."
                ]
            },
            {
                "role": "Software Developer",
                "company": "Legacy Tech Corp",
                "dates": "Jun 2017 - Jan 2020",
                "bullets": [
                    "Maintained J2EE enterprise applications and migrated modules to Spring Boot microservices.",
                    "Collaborated in Agile scrums and managed version control with Git."
                ]
            }
        ]
    },
    {
        "id": "cand_09",
        "name": "Maya Lin",
        "filename": "Maya_Lin_Resume.docx",
        "format": "docx",
        "layout": "standard",
        "expected_rank": 9,
        "email": "maya.lin@bootcampalumni.org",
        "phone": "(555) 012-3456",
        "title": "Associate Web Developer",
        "degree": "Coding Bootcamp Certificate in Full-Stack Web Development",
        "total_years": 0.9,
        "relevant_years": 0.9,
        "skills": ["Python", "Flask", "JavaScript", "HTML5", "CSS3", "Git", "SQLite"],
        "summary": "Recent full-stack coding bootcamp graduate eager to contribute foundational Python and web development skills to an innovative engineering team.",
        "experience": [
            {
                "role": "Software Engineering Intern",
                "company": "StartUp Catalyst",
                "dates": "May 2023 - Present",
                "bullets": [
                    "Built prototype web apps using Python Flask and SQLite backends.",
                    "Designed responsive UI elements using HTML5, CSS3, and JavaScript.",
                    "Participated in weekly Git code reviews and sprint planning meetings."
                ]
            }
        ]
    },
    {
        "id": "cand_10",
        "name": "Lucas Scott",
        "filename": "Lucas_Scott_Resume.pdf",
        "format": "pdf",
        "layout": "standard",
        "expected_rank": 10,
        "email": "lucas.scott@qualityhub.com",
        "phone": "(555) 123-7890",
        "title": "QA Automation Engineer",
        "degree": "Bachelor of Science in Information Systems",
        "total_years": 3.2,
        "relevant_years": 1.0,
        "skills": ["Selenium", "Python", "Unit Testing", "pytest", "CI/CD", "Git", "Jenkins"],
        "summary": "Quality Assurance Automation Engineer with 3.2 years designing automated test suites, Selenium frameworks, and regression testing pipelines.",
        "experience": [
            {
                "role": "QA Automation Engineer",
                "company": "VerifySoft Global",
                "dates": "Jan 2022 - Present",
                "bullets": [
                    "Constructed automated UI testing frameworks using Python and Selenium WebDriver.",
                    "Integrated automated test runs into Jenkins CI/CD deployment pipelines.",
                    "Wrote comprehensive unit and integration tests using pytest."
                ]
            }
        ]
    },
    {
        "id": "cand_11",
        "name": "Daniel Martinez",
        "filename": "Daniel_Martinez_Resume.docx",
        "format": "docx",
        "layout": "standard",
        "expected_rank": 11,
        "email": "daniel.martinez@analyticsedge.com",
        "phone": "(555) 234-8901",
        "title": "Business Intelligence Analyst",
        "degree": "Bachelor of Business Administration in Finance",
        "total_years": 3.5,
        "relevant_years": 0.5,
        "skills": ["SQL", "Excel", "Tableau", "PowerBI", "Pandas", "Agile"],
        "summary": "Business Intelligence Analyst with 3.5 years translating complex enterprise data into executive dashboards, financial forecasts, and KPI metrics.",
        "experience": [
            {
                "role": "BI Analyst",
                "company": "Global Logistics Corp",
                "dates": "Jul 2021 - Present",
                "bullets": [
                    "Designed executive financial dashboards in Tableau and PowerBI.",
                    "Wrote SQL queries to extract data from corporate data warehouses.",
                    "Utilized Excel macros and Python Pandas for monthly financial reconciliations."
                ]
            }
        ]
    },
    {
        "id": "cand_12",
        "name": "Chloe Dubois",
        "filename": "Chloe_Dubois_Resume.pdf",
        "format": "pdf",
        "layout": "standard",
        "expected_rank": 12,
        "email": "chloe.dubois@creativepixel.com",
        "phone": "(555) 345-9012",
        "title": "Senior UI/UX Graphic Designer",
        "degree": "Bachelor of Fine Arts in Graphic Design",
        "total_years": 4.5,
        "relevant_years": 0.0,
        "skills": ["Figma", "Adobe XD", "Illustrator", "Photoshop", "CSS", "Wireframing"],
        "summary": "Creative UI/UX and Graphic Designer with 4.5 years crafting brand identities, responsive web design wireframes, and design systems in Figma.",
        "experience": [
            {
                "role": "Lead UI/UX Designer",
                "company": "Aesthetic Studio",
                "dates": "Jan 2020 - Present",
                "bullets": [
                    "Created high-fidelity wireframes, mockups, and interactive prototypes in Figma.",
                    "Conducted user research studies and usability testing for mobile apps.",
                    "Designed marketing assets and illustrations in Adobe Creative Suite."
                ]
            }
        ]
    }
]


def generate_pdf(c, output_path):
    pdf = FPDF(format="A4")
    pdf.set_margins(12, 12, 12)
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    
    # Header: Name & Contact
    pdf.set_font("Helvetica", style="B", size=18)
    pdf.cell(0, 9, c["name"], new_x="LMARGIN", new_y="NEXT", align="L")
    
    pdf.set_font("Helvetica", size=9.5)
    pdf.set_text_color(80, 80, 80)
    contact_line = f"{c['email']}  |  {c['phone']}  |  {c['title']}"
    pdf.cell(0, 6, contact_line, new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(2)
    
    # Horizontal rule
    pdf.set_draw_color(200, 200, 200)
    pdf.line(12, pdf.get_y(), 198, pdf.get_y())
    pdf.ln(3)
    
    if c.get("layout") == "two_column":
        # Two-column layout
        y_start = pdf.get_y()
        
        # Left column (Skills & Education): width 55
        pdf.set_xy(12, y_start)
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(55, 6, "TECHNICAL SKILLS", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=9)
        pdf.set_text_color(60, 60, 60)
        for s in c["skills"]:
            pdf.cell(55, 5, f"- {s}", new_x="LMARGIN", new_y="NEXT")
            
        pdf.ln(3)
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(55, 6, "EDUCATION", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=8.5)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(55, 4.5, c["degree"])
        
        # Right column (Summary & Experience): width 125, start at x=72
        pdf.set_xy(72, y_start)
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(124, 6, "SUMMARY", new_x="LEFT", new_y="NEXT")
        pdf.set_font("Helvetica", size=9)
        pdf.set_text_color(50, 50, 50)
        pdf.set_x(72)
        pdf.multi_cell(124, 4.5, c["summary"])
        pdf.ln(3)
        
        pdf.set_x(72)
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(124, 6, "WORK EXPERIENCE", new_x="LEFT", new_y="NEXT")
        
        for exp in c["experience"]:
            pdf.set_x(72)
            pdf.set_font("Helvetica", style="B", size=9.5)
            pdf.set_text_color(20, 20, 20)
            pdf.cell(124, 5.5, f"{exp['role']} - {exp['company']}", new_x="LEFT", new_y="NEXT")
            pdf.set_x(72)
            pdf.set_font("Helvetica", style="I", size=8.5)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(124, 4.5, exp["dates"], new_x="LEFT", new_y="NEXT")
            
            pdf.set_font("Helvetica", size=8.5)
            pdf.set_text_color(50, 50, 50)
            for b in exp["bullets"]:
                pdf.set_x(72)
                pdf.multi_cell(124, 4.5, f"* {b}")
            pdf.ln(2)

    elif c.get("layout") == "table":
        # Table layout for skills and education
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, "PROFESSIONAL SUMMARY", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=9.5)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 4.5, c["summary"])
        pdf.ln(3)
        
        # Table of Skills & Degree
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, "SKILLS & QUALIFICATIONS", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", style="B", size=9)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(45, 6, "Category", border=1, fill=True)
        pdf.cell(140, 6, "Details", border=1, new_x="LMARGIN", new_y="NEXT", fill=True)
        
        pdf.set_font("Helvetica", size=8.5)
        pdf.cell(45, 6, "Technical Stack", border=1)
        pdf.cell(140, 6, ", ".join(c["skills"]), border=1, new_x="LMARGIN", new_y="NEXT")
        
        pdf.cell(45, 6, "Academic Degree", border=1)
        pdf.cell(140, 6, c["degree"], border=1, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        
        # Experience
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, "PROFESSIONAL EXPERIENCE", new_x="LMARGIN", new_y="NEXT")
        for exp in c["experience"]:
            pdf.set_font("Helvetica", style="B", size=9.5)
            pdf.cell(125, 5.5, f"{exp['role']} | {exp['company']}")
            pdf.set_font("Helvetica", style="I", size=8.5)
            pdf.cell(60, 5.5, exp["dates"], new_x="LMARGIN", new_y="NEXT", align="R")
            pdf.set_font("Helvetica", size=9)
            pdf.set_text_color(50, 50, 50)
            for b in exp["bullets"]:
                pdf.set_x(12)
                pdf.multi_cell(0, 4.5, f"- {b}")
            pdf.ln(2)

    else:
        # Standard 1-column layout
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, "PROFESSIONAL SUMMARY", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=9.5)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 4.5, c["summary"])
        pdf.ln(3)
        
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, "TECHNICAL SKILLS", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=9)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 4.5, ", ".join(c["skills"]))
        pdf.ln(3)
        
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, "WORK EXPERIENCE", new_x="LMARGIN", new_y="NEXT")
        for exp in c["experience"]:
            pdf.set_font("Helvetica", style="B", size=9.5)
            pdf.cell(125, 5.5, f"{exp['role']} - {exp['company']}")
            pdf.set_font("Helvetica", style="I", size=8.5)
            pdf.cell(60, 5.5, exp["dates"], new_x="LMARGIN", new_y="NEXT", align="R")
            pdf.set_font("Helvetica", size=9)
            pdf.set_text_color(50, 50, 50)
            for b in exp["bullets"]:
                pdf.set_x(12)
                pdf.multi_cell(0, 4.5, f"* {b}")
            pdf.ln(2)
            
        pdf.set_font("Helvetica", style="B", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, "EDUCATION", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=9.5)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 5.5, c["degree"], new_x="LMARGIN", new_y="NEXT")

    pdf.output(output_path)


def generate_docx(c, output_path):
    doc = docx.Document()
    
    # Title / Name
    p_name = doc.add_paragraph()
    run_name = p_name.add_run(c["name"])
    run_name.font.size = Pt(18)
    run_name.font.bold = True
    
    # Contact
    p_contact = doc.add_paragraph()
    run_contact = p_contact.add_run(f"{c['email']} | {c['phone']} | {c['title']}")
    run_contact.font.size = Pt(9.5)
    run_contact.font.color.rgb = RGBColor(100, 100, 100)
    
    # Summary
    doc.add_heading("PROFESSIONAL SUMMARY", level=2)
    p_sum = doc.add_paragraph(c["summary"])
    p_sum.style.font.size = Pt(10)
    
    # Skills
    doc.add_heading("TECHNICAL SKILLS", level=2)
    p_skills = doc.add_paragraph(", ".join(c["skills"]))
    p_skills.style.font.size = Pt(10)
    
    # Experience
    doc.add_heading("WORK EXPERIENCE", level=2)
    for exp in c["experience"]:
        p_role = doc.add_paragraph()
        r1 = p_role.add_run(f"{exp['role']} - {exp['company']}")
        r1.bold = True
        r1.font.size = Pt(11)
        r2 = p_role.add_run(f"  ({exp['dates']})")
        r2.italic = True
        r2.font.size = Pt(9.5)
        
        for b in exp["bullets"]:
            doc.add_paragraph(b, style='List Bullet')
            
    # Education
    doc.add_heading("EDUCATION", level=2)
    p_edu = doc.add_paragraph(c["degree"])
    p_edu.style.font.size = Pt(10)
    
    doc.save(output_path)


def main():
    print(f"Generating test resumes in {TEST_RESUMES_DIR}...")
    
    # Write sample JD
    jd_path = os.path.join(os.path.dirname(__file__), "sample_jd.txt")
    with open(jd_path, "w", encoding="utf-8") as f:
        f.write(SAMPLE_JD.strip())
    print(f"Wrote Sample JD to {jd_path}")
    
    ground_truth = []
    
    for c in CANDIDATES:
        out_file = os.path.join(TEST_RESUMES_DIR, c["filename"])
        if c["format"] == "pdf":
            generate_pdf(c, out_file)
        else:
            generate_docx(c, out_file)
        print(f"Generated {c['format'].upper()}: {c['filename']} ({c['layout']})")
        
        ground_truth.append({
            "id": c["id"],
            "name": c["name"],
            "filename": c["filename"],
            "format": c["format"],
            "layout": c["layout"],
            "expected_rank": c["expected_rank"],
            "total_years_exp": c["total_years"],
            "relevant_years_exp": c["relevant_years"],
            "skills": c["skills"],
            "degree": c["degree"]
        })
        
    gt_path = os.path.join(os.path.dirname(__file__), "ground_truth.json")
    with open(gt_path, "w", encoding="utf-8") as f:
        json.dump({
            "target_jd": "Senior Backend Engineer (Python / FastAPI)",
            "required_years": 4.0,
            "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS", "REST API", "Git"],
            "preferred_skills": ["Redis", "RabbitMQ", "React", "Next.js"],
            "candidates": ground_truth
        }, f, indent=2)
    print(f"Wrote Ground Truth to {gt_path}")


if __name__ == "__main__":
    main()
