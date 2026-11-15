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
  Hyderabad, India
\end{center}
\vspace{-6pt}

%-----------PROFESSIONAL SUMMARY-----------
\section{Professional Summary}
\small{Computer Science student (AIML) with 2 software engineering internships and strong foundations in Python, C++, Java, and applied AI/ML. Experienced in building game simulations, probabilistic forecasting engines, and automated quality verification systems. Proven track record in developing high-performance data pipelines, algorithmic optimizers, and automated API validation testbeds.}
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
      \resumeItem{Engineered a real-time data processing pipeline in \textbf{Python} analyzing \textbf{10,000+ daily events}. Deployed an automated 3-tier NLP classification testbed achieving \textbf{95\% precision} with sub-second latency.}
    \resumeItemListEnd

  \resumeSubheading
    {SDE Intern $|$ Qcecuring Technologies $|$ Delhi, India}{October 2025 -- December 2025}
    {}{}
    \vspace{-12pt}
    \resumeItemListStart
      \resumeItem{Architected a secure certificate management and verification engine in \textbf{Python} and \textbf{C++}. Implemented multi-approver quorum workflows, automated integrity checks, and immutable audit logs across \textbf{50+ assets}.}
    \resumeItemListEnd

\resumeSubHeadingListEnd

%-----------PROJECTS-----------
\section{Projects}
\resumeSubHeadingListStart

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/FIFA-WorldCup-2026-Prediction}{FIFA World Cup 2026 Simulation \& Probabilistic Forecasting}} \href{https://github.com/Krishna-Kilrofkansa/FIFA-WorldCup-2026-Prediction}{\textcolor{blue}{GitHub}} $|$ \textit{Python, Scikit-learn, NumPy, SciPy, Game Analytics}}{}
    \resumeItemListStart
      \resumeItem{Formulated a probabilistic match outcome simulator combining dynamic \textbf{Elo ratings} with squad-strength features. Executed \textbf{20,000 Monte Carlo simulations} across 900+ matches to model tournament outcomes with zero data leakage.}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/ipl-prediction}{Sports Match Analytics \& Game Decision Engine}} \href{https://github.com/Krishna-Kilrofkansa/ipl-prediction}{\textcolor{blue}{GitHub}} $|$ \textit{Python, Scikit-learn, SQLite, Pandas, Optimization}}{}
    \resumeItemListStart
      \resumeItem{Designed a match outcome predictor scoring \textbf{AUC 0.81} across 1,169 matches with ensemble learning. Built a constrained linear optimization algorithm for team roster selection under budget and role limits.}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/VARUNA}{VARUNA -- Automated Verification \& Incident Triage System (SIH 2025)}} \href{https://github.com/Krishna-Kilrofkansa/VARUNA}{\textcolor{blue}{GitHub}} $|$ \textit{Python, OpenCV, NLP, Quality Verification}}{}
    \resumeItemListStart
      \resumeItem{Led a \textbf{5-person team} to build an automated data verification platform processing \textbf{5,000+ monthly submissions}. Implemented computer vision and NLP validation checks that cut false reports by \textbf{$\sim$35\%} (Ranked \textbf{51st nationally}).}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/tslate}{TSlate -- Low-Latency Offline Neural Engine}} \href{https://github.com/Krishna-Kilrofkansa/tslate}{\textcolor{blue}{GitHub}} $|$ \textit{C++, Python, JNI/NDK, Model Optimization}}{}
    \resumeItemListStart
      \resumeItem{Engineered an offline translation runtime in \textbf{C++} integrating INT8 quantized models. Achieved \textbf{$<$15s} end-to-end execution latency using custom C++ bindings and memory-efficient data structures.}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/ecoloop}{Eco-Loop -- Automated Testing \& Safety Guardrail Agent}} \href{https://github.com/Krishna-Kilrofkansa/ecoloop}{\textcolor{blue}{GitHub}} $|$ \textit{Python, Pydantic, Test Automation, QA}}{}
    \resumeItemListStart
      \resumeItem{Built an automated control agent with strict \textbf{Pydantic schema validation} and test assertions. Enforced runtime boundary limits and deterministic fallback rules to guarantee operational stability and prevent invalid states.}
    \resumeItemListEnd

\resumeSubHeadingListEnd

%-----------TECHNICAL SKILLS-----------
\section{Technical Skills}
\begin{itemize}[leftmargin=0in, label={}, itemsep=0pt, topsep=0pt, parsep=0pt]
\small\item{
\textbf{Languages:} Python, C++, Java, JavaScript, SQL, C\# \\
\textbf{AI/ML \& Data Analysis:} Scikit-learn, PyTorch, Monte Carlo Simulation, OpenCV, NLP, Pandas, NumPy, SciPy \\
\textbf{Verification, Testing \& QA (QVS):} Test Automation, Automated Validation Pipelines, Pydantic Validation, API Testing, Integrity Verification \\
\textbf{Backend \& Systems:} REST APIs, Fast Execution Engines, Data Structures, Linux, Git, Docker, CI/CD, Jupyter
}
\end{itemize}
\vspace{-5pt}

%-----------CERTIFICATIONS-----------
\section{Certifications}
\begin{itemize}[leftmargin=0.15in, itemsep=0pt, topsep=0pt, parsep=0pt]
  \small
  \item \textbf{Supervised Machine Learning: Regression and Classification} -- DeepLearning.AI \href{https://www.coursera.org/account/accomplishments/verify/TLP3MHO43N32}{\textcolor{blue}{Certificate}} \hfill December 2024
  \item \textbf{Generative AI Using IBM Watsonx} -- IBM \href{https://courses.vit.skillsnetwork.site/certificates/cb164478ebbc423cb0f9f18a502d59f6}{\textcolor{blue}{Certificate}} \hfill June 2025
  \item \textbf{Anthropic AI Courses} \href{https://verify.skilljar.com/c/ufc5sweipoht}{\textcolor{blue}{Certificate}} \hfill May 2026
\end{itemize}

%-----------ACHIEVEMENTS-----------
\section{Achievements}
\begin{itemize}[leftmargin=0.15in, itemsep=0pt, topsep=0pt, parsep=0pt]
  \small
  \item \textbf{LeetCode:} Solved 300+ algorithmic and data structure problems across C++, Java, and Python. \hfill July 2026
  \item \textbf{Gold Level -- WorldQuant BRAIN International Quant Championship:} Top 20\% globally in quantitative modeling. \hfill June 2026
  \item \textbf{SIH 2025 -- VARUNA:} Shortlisted from \textbf{864 teams} to top 150 nationally; ranked \textbf{51st} in second round. \hfill September 2025
  \item \textbf{National Semi-Finalist, Flipkart GRID 7.0:} Techno-commercial hackathon by Flipkart Early Careers. \hfill August 2025
  \item \textbf{National Finalist, 3rd Runner-up -- DATASET '24:} Built an end-to-end AI system in 36 hours; earned a \textbf{Nokia internship offer}. \hfill December 2024
\end{itemize}

\end{document}
