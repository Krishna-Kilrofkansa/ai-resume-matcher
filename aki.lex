\documentclass[letterpaper,11pt]{article}

\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage[usenames,dvipsnames,svgnames,table]{xcolor}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{geometry}

\geometry{top=0.25in, bottom=0.25in, left=0.3in, right=0.3in}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \vspace{-5pt}\bfseries\raggedright\normalsize\uppercase
}{}{0em}{}[\color{black}\titlerule\vspace{-4pt}]

\newcommand{\resumeItem}[1]{
  \item\small{#1\vspace{1pt}}
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-1pt}\item
    \begin{tabular*}{\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{\small#1} & \small#2 \\
      \textit{\small#3} & \textit{\small#4} \\
    \end{tabular*}\vspace{-6pt}
}

\newcommand{\resumeProjectHeading}[2]{
  \vspace{-1pt}\item
    \begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & \small#2 \\
    \end{tabular*}\vspace{-3pt}
}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}\vspace{-4pt}}
\newcommand{\resumeItemListStart}{\begin{itemize}[leftmargin=0.15in, topsep=0pt, itemsep=0pt, parsep=0pt]}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-4pt}}

\begin{document}

%---------- HEADING ----------
\begin{center}
  {\Huge\textbf{Aakarshak Swaraj}} \\[3pt]
  \small
  +91-81416 23953 \;$|$\;
  \href{mailto:aakarshak.work@gmail.com}{aakarshak.work@gmail.com} \;$|$\;
  \href{https://www.linkedin.com/in/aakarshak-swaraj-a3ba21290}{LinkedIn} \;$|$\;
  \href{https://akiportfolio.vercel.app/}{Portfolio} \;$|$\;
  \href{https://github.com/Krishna-Kilrofkansa}{GitHub} \;$|$\;
  Chennai, India
\end{center}
\vspace{-6pt}

%-----------PROFESSIONAL SUMMARY-----------
\section{Professional Summary}
\small{Final-year Computer Science student with two analytics internships. Experienced in building modular ETL workflows and predictive models using \textbf{Python}, \textbf{SQL}, \textbf{PySpark}, and \textbf{Kedro}. Skilled in \textbf{PowerBI} dashboarding and statistical data validation to support strategic business decisions.}
\vspace{-2pt}

%-----------EDUCATION-----------
\section{Education}
\resumeSubHeadingListStart
  \resumeSubheading
    {Vellore Institute of Technology}{July 2023 -- July 2027}
    {B.Tech in Computer Science, Specialization in AIML (GPA: 8.62/10.0)}{Chennai, India}
\resumeSubHeadingListEnd

%-----------WORK EXPERIENCE-----------
\section{Work Experience}
\resumeSubHeadingListStart

  \resumeSubheading
    {SDE Intern $|$ Taslasoft $|$ Hyderabad, India}{February 2026 -- July 2026}
    {}{}
    \vspace{-12pt}
    \resumeItemListStart
      \resumeItem{Engineered a social media data pipeline in \textbf{Python} analyzing \textbf{10,000+ daily posts}. Deployed a 3-tier NLP classification model achieving \textbf{95\% precision} across 200+ flagged events.}
    \resumeItemListEnd

  \resumeSubheading
    {SDE Intern $|$ Qcecuring Technologies $|$ Delhi, India}{October 2025 -- December 2025}
    {}{}
    \vspace{-12pt}
    \resumeItemListStart
      \resumeItem{Architected an enterprise certificate lifecycle management service in \textbf{Python}. Enforced quorum-based approvals and immutable audit logs across \textbf{50+ enterprise assets}.}
    \resumeItemListEnd

\resumeSubHeadingListEnd

%-----------PROJECTS-----------
\section{Projects}
\resumeSubHeadingListStart

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/retail-demand-pipeline}{Retail Store Sales \& Demand Forecasting Pipeline}} \href{https://github.com/Krishna-Kilrofkansa/retail-demand-pipeline}{\textcolor{blue}{GitHub}} $|$ \textit{Kedro, PySpark, Python, PowerBI, SQL, Scikit-learn}}{}
    \resumeItemListStart
      \resumeItem{Developed a modular data processing framework with \textbf{Kedro} and \textbf{PySpark} across \textbf{1,000+ store locations}. Integrated programmatic schema validation and interactive \textbf{PowerBI} stockout alerts.}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/FIFA-WorldCup-2026-Prediction}{FIFA World Cup 2026 Probabilistic Forecasting System}} \href{https://github.com/Krishna-Kilrofkansa/FIFA-WorldCup-2026-Prediction}{\textcolor{blue}{GitHub}} $|$ \textit{Python, Scikit-learn, NumPy, SciPy, Statistical Modeling}}{}
    \resumeItemListStart
      \resumeItem{Formulated a probabilistic forecasting engine combining forward-in-time \textbf{Elo ratings} with squad-strength features. Executed \textbf{20,000 Monte Carlo simulations} across 900+ matches without data leakage.}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/ipl-prediction}{IPL Match Analytics \& Decision Support System}} \href{https://github.com/Krishna-Kilrofkansa/ipl-prediction}{\textcolor{blue}{GitHub}} $|$ \textit{Python, Scikit-learn, SQLite, Pandas, NumPy, Optimization}}{}
    \resumeItemListStart
      \resumeItem{Designed an outcome prediction model scoring \textbf{AUC 0.81} across 1,169 matches using an ensemble classifier. Built a constrained linear optimization algorithm for team selection with SQLite data ingestion.}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/VARUNA}{VARUNA -- Disaster Incident Triage Platform (SIH 2025)}} \href{https://github.com/Krishna-Kilrofkansa/VARUNA}{\textcolor{blue}{GitHub}} $|$ \textit{Python, NLP, OpenCV, Data Validation}}{}
    \resumeItemListStart
      \resumeItem{Led a \textbf{5-person team} to build an incident triage platform processing \textbf{5,000+ monthly reports}. Implemented dual CV and NLP verification filters that reduced false submissions by \textbf{$\sim$35\%} (Ranked \textbf{51st nationally}).}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/ecoloop}{Eco-Loop -- Automated HVAC Control Agent}} \href{https://github.com/Krishna-Kilrofkansa/ecoloop}{\textcolor{blue}{GitHub}} $|$ \textit{Python, Pydantic, LLMs, Risk Management, Guardrails}}{}
    \resumeItemListStart
      \resumeItem{Implemented an HVAC control agent with \textbf{Pydantic schema validation}. Enforced runtime boundary limits and deterministic safety fallbacks to prevent out-of-bound states and maintain operational stability.}
    \resumeItemListEnd

\resumeSubHeadingListEnd

%-----------TECHNICAL SKILLS-----------
\section{Technical Skills}
\begin{itemize}[leftmargin=0in, label={}, itemsep=0pt, topsep=0pt, parsep=0pt]
\small\item{
\textbf{Languages \& Core:} Python, SQL (PostgreSQL, MySQL, SQLite), PySpark, C++ \\
\textbf{Data Engineering \& Pipelines:} Kedro, Microsoft Fabric, Apache Spark (PySpark), ETL/ELT Pipelines, Data Modeling, Pandas, NumPy \\
\textbf{Analytics \& Machine Learning:} Statistical Modeling, Predictive Analytics, Forecasting, Scikit-learn, PyTorch, Monte Carlo Simulation, NLP \\
\textbf{BI \& Visualization:} PowerBI, Tableau, Matplotlib, Seaborn, Executive Dashboarding \\
\textbf{QA, Risk \& Standards:} Data Quality Assurance, CI/CD, Git, Docker, Code Quality \& Risk Management, Linux, Jupyter
}
\end{itemize}
\vspace{-5pt}

%-----------CERTIFICATIONS-----------
\section{Certifications}
\begin{itemize}[leftmargin=0.15in, itemsep=0pt, topsep=0pt, parsep=0pt]
  \small
  \item \textbf{Generative AI Using IBM Watsonx} -- IBM \href{https://courses.vit.skillsnetwork.site/certificates/cb164478ebbc423cb0f9f18a502d59f6}{\textcolor{blue}{Certificate}} \hfill June 2025
  \item \textbf{Supervised Machine Learning: Regression and Classification} -- DeepLearning.AI \href{https://www.coursera.org/account/accomplishments/verify/TLP3MHO43N32}{\textcolor{blue}{Certificate}} \hfill December 2024
  \item \textbf{Anthropic AI Courses} \href{https://verify.skilljar.com/c/ufc5sweipoht}{\textcolor{blue}{Certificate}} \hfill May 2026
\end{itemize}

%-----------ACHIEVEMENTS-----------
\section{Achievements}
\begin{itemize}[leftmargin=0.15in, itemsep=0pt, topsep=0pt, parsep=0pt]
  \small
  \item \textbf{Gold Level -- WorldQuant BRAIN International Quant Championship:} Top 20\% globally in quantitative analytics and alpha modeling. \hfill June 2026
  \item \textbf{SIH 2025 -- VARUNA:} Shortlisted from \textbf{864 teams} to top 150 nationally; ranked \textbf{51st} in second round. \hfill September 2025
  \item \textbf{National Semi-Finalist, Flipkart GRID 7.0:} Techno-commercial analytics hackathon by Flipkart Early Careers. \hfill August 2025
  \item \textbf{National Finalist, 3rd Runner-up -- DATASET '24:} Built an end-to-end AI system in 36 hours; earned a \textbf{Nokia internship offer}. \hfill December 2024
  \item \textbf{LeetCode:} Solved 300+ algorithmic and data structure problems across Python and C++. \hfill July 2026
\end{itemize}

\end{document}
