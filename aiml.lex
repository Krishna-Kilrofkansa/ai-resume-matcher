\documentclass[letterpaper,10pt]{article}

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
  \vspace{-7pt}\bfseries\raggedright\normalsize\uppercase
}{}{0em}{}[\color{black}\titlerule\vspace{-5pt}]

\newcommand{\resumeItem}[1]{
  \item\normalsize{#1\vspace{0pt}}
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-1pt}\item
    \begin{tabular*}{\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{\small#1} & \small#2 \\
      \textit{\small#3} & \textit{\small#4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
  \vspace{-1pt}\item
    \begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & \small#2 \\
    \end{tabular*}\vspace{-4pt}
}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}\vspace{-5pt}}
\newcommand{\resumeItemListStart}{\begin{itemize}[leftmargin=0.15in, topsep=0pt, itemsep=0pt, parsep=0pt]}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

\begin{document}

%---------- HEADING ----------
\begin{center}
  {\LARGE\textbf{Aakarshak Swaraj}} \\[2pt]
  \small
  +91-81416 23953 \;$|$\;
  \href{mailto:aakarshak.work@gmail.com}{aakarshak.work@gmail.com} \;$|$\;
  \href{https://www.linkedin.com/in/aakarshak-swaraj-a3ba21290}{LinkedIn} \;$|$\;
  \href{https://akiportfolio.vercel.app/}{Portfolio} \;$|$\;
  \href{https://github.com/Krishna-Kilrofkansa}{GitHub} \;$|$\;
  Bengaluru, India
\end{center}
\vspace{-6pt}

%-----------PROFESSIONAL SUMMARY-----------
\section{Professional Summary}
\small{AI/ML Engineer with 2 internships and 7+ production-grade projects in deep learning, NLP, and computer vision. Improved medical image classification to \textbf{93.4\% accuracy} using ResNet50 with SimCLR contrastive learning, elevated sports prediction to \textbf{AUC 0.81} via ensemble methods, and drove \textbf{95\% precision} on a transformer-based NLP pipeline deployed for civic monitoring. Skilled in Python, PyTorch, Transformers, OpenCV, scikit-learn, model optimization, and prompt engineering.}
\vspace{-2pt}

%-----------EDUCATION-----------
\section{Education}
\resumeSubHeadingListStart
  \resumeSubheading
    {Vellore Institute of Technology}{July 2023 -- July 2027 (Expected)}
    {B.Tech in Computer Science, Specialization in AIML; GPA: 8.62/10.0}{Chennai, India}
\resumeSubHeadingListEnd

%-----------WORK EXPERIENCE-----------
\section{Work Experience}
\resumeSubHeadingListStart

  \resumeSubheading
    {SDE Intern $|$ Taslasoft $|$ Hyderabad, India}{February 2026 -- April 2026}
    {}{}
    \vspace{-12pt}
    \resumeItemListStart
      \resumeItem{Developed a real-time social intelligence pipeline in \textbf{Python} monitoring \textbf{15+ subreddits} and analyzing \textbf{10,000+ posts daily}, mapping incident activity to geographic clusters through a geo-temporal aggregation system with sub-second latency.}
      \resumeItem{Reached \textbf{95\% precision} on a 3-stage NLP detection pipeline (keyword filtering $\rightarrow$ sentiment analysis $\rightarrow$ transformer classification) with human-in-the-loop validation, flagging \textbf{200+ harmful posts} during the pilot deployment.}
    \resumeItemListEnd

  \resumeSubheading
    {SDE Intern $|$ Qcecuring Technologies $|$ Delhi, India}{October 2025 -- December 2025}
    {}{}
    \vspace{-12pt}
    \resumeItemListStart
      \resumeItem{Architected a self-service code-signing platform with client-side hashing, reducing key-exposure incidents to \textbf{zero} and cutting artifact signing time by \textbf{60\%} compared to the previous manual workflow.}
      \resumeItem{Delivered a \textbf{PKI-as-a-Service} module supporting \textbf{50+ enterprise certificates}, with quorum-based multi-approver workflows, automated lifecycle management, and tamper-proof audit logging for compliance.}
    \resumeItemListEnd

\resumeSubHeadingListEnd

%-----------PROJECTS-----------
\section{Projects}
\resumeSubHeadingListStart

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/FIFA-WorldCup-2026-Prediction}{FIFA World Cup 2026 Prediction}} \href{https://github.com/Krishna-Kilrofkansa/FIFA-WorldCup-2026-Prediction}{\textcolor{blue}{GitHub}} $|$ \textit{Python, Scikit-learn, NumPy, SciPy, Matplotlib}}{}
    \resumeItemListStart
      \resumeItem{Built a multinomial logistic regression model fusing forward-in-time \textbf{Elo ratings} with squad-strength features across \textbf{900+ international matches}; ran \textbf{20,000 Monte Carlo} simulations to forecast title probabilities, backtested on 2018 and 2022 World Cups with temporally-correct splits and \textbf{log-loss below baseline}.}
    \resumeItemListEnd
    
  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/tslate}{TSlate -- Offline Voice Translator}} \href{https://github.com/Krishna-Kilrofkansa/tslate}{\textcolor{blue}{GitHub}} $|$ \textit{C++, Whisper.cpp, NLLB-200}}{}
    \resumeItemListStart
      \resumeItem{Engineered a fully offline Android voice translator (Hindi/Hinglish $\rightarrow$ Kannada) targeting \textbf{$<$15s} end-to-end latency by integrating Whisper.cpp (ggml-tiny) for STT and \textbf{NLLB-200 600M INT8} for neural translation}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{Breast Cancer Detection} $|$ \textit{Python, PyTorch, ResNet50, SimCLR, Deep Learning}}{}
    \resumeItemListStart
      \resumeItem{Fine-tuned \textbf{ResNet50} with SimCLR contrastive pretraining on \textbf{7,909 BreakHis} histopathology images, reaching \textbf{93.4\% accuracy} and \textbf{0.92 F1-score} --- a $\sim$7\% gain over the CNN baseline --- using PyTorch with augmentation-heavy preprocessing.}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/ipl-prediction}{IPL Match Prediction \& Decision Support}} \href{https://github.com/Krishna-Kilrofkansa/ipl-prediction}{\textcolor{blue}{GitHub}} $|$ \textit{Python, Scikit-learn, SQLite, Pandas, NumPy}}{}
    \resumeItemListStart
      \resumeItem{Designed an IPL outcome predictor scoring \textbf{AUC 0.81} across 1,169 matches (2008--2026) using a tuned soft-voting ensemble with 20+ engineered features and an SQLite-backed incremental retraining pipeline; implemented a constrained \textbf{Playing XI optimizer} enforcing role composition and overseas limits.}
    \resumeItemListEnd

  \resumeProjectHeading
    {\href{https://varuna001.vercel.app/}{\textbf{VARUNA -- Disaster Reporting Platform (SIH 2025)}} \href{https://github.com/Krishna-Kilrofkansa/VARUNA}{\textcolor{blue}{GitHub}} $|$ \textit{Next.js, Python, OpenCV, NLP}}{}
    \resumeItemListStart
      \resumeItem{Led a \textbf{5-person team} to build VARUNA, processing \textbf{5,000+ monthly reports} with a multi-stage CV+NLP validation pipeline that reduced false submissions by $\sim$\textbf{35\%}; deployed OpenCV for image verification and transformer-based text classification for report triage.}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/EYERIS}{EYERIS -- Privacy-Preserving Autonomous Robot}} \href{https://github.com/Krishna-Kilrofkansa/EYERIS}{\textcolor{blue}{GitHub}} $|$ \textit{Python, OpenCV, MediaPipe, Arduino}}{}
    \resumeItemListStart
      \resumeItem{Deployed a privacy-preserving robot with \textbf{$<$50ms} real-time human detection latency via MediaPipe pose estimation and OpenCV, eliminating camera-based identification while maintaining a \textbf{$\sim$30cm} obstacle avoidance threshold across \textbf{3 lab environments}.}
    \resumeItemListEnd

\resumeSubHeadingListEnd

%-----------TECHNICAL SKILLS-----------
\section{Technical Skills}
\begin{itemize}[leftmargin=0in, label={}, itemsep=0pt, topsep=0pt, parsep=0pt]
\small\item{
\textbf{ML \& AI:} PyTorch, Scikit-learn, Transformers, OpenCV, NLP, LLMs, RAG, Fine-Tuning, Prompt Engineering, Model Optimization \\
\textbf{Languages:} Python, C++, JavaScript \quad
\textbf{Data:} Pandas, NumPy, SciPy, Matplotlib \\
\textbf{Backend \& Systems:} FastAPI, Node.js, REST APIs \\
\textbf{Databases:} PostgreSQL, MySQL, MongoDB, SQLite \quad
\textbf{Cloud \& DevOps:} AWS (EC2, S3, Lambda), Docker, CI/CD \\
\textbf{Tools:} Git, Linux, Jupyter
}
\end{itemize}
\vspace{-5pt}

%-----------CERTIFICATIONS-----------
\section{Certifications}
\begin{itemize}[leftmargin=0.15in, itemsep=0pt, topsep=0pt, parsep=0pt]
  \small
  \item \textbf{Anthropic AI Courses} \href{https://verify.skilljar.com/c/ufc5sweipoht}{\textcolor{blue}{Certificate}} \hfill May 2026
  \item \textbf{Generative AI Using IBM Watsonx} -- IBM \href{https://courses.vit.skillsnetwork.site/certificates/cb164478ebbc423cb0f9f18a502d59f6}{\textcolor{blue}{Certificate}} \hfill Jun 2025
  \item \textbf{Supervised Machine Learning: Regression and Classification} -- DeepLearning.AI \href{https://www.coursera.org/account/accomplishments/verify/TLP3MHO43N32}{\textcolor{blue}{Certificate}} \hfill Dec 2024
\end{itemize}

%-----------ACHIEVEMENTS-----------
\section{Achievements}
\begin{itemize}[leftmargin=0.15in, itemsep=0pt, topsep=0pt, parsep=0pt]
  \small
  \item \textbf{LeetCode:} Solved 300+ algorithmic problems across C++, Java, and Python; achieved a contest rating of 1,489. \href{https://leetcode.com/u/aki_09n/}{\textcolor{blue}{Link}}  \hfill Jul 2026
  \item \textbf{Gold Level -- WorldQuant BRAIN International Quant Championship 2026:} a quantitative research challenge. \hfill Jun 2026
  \item \textbf{SIH 2025 -- VARUNA:} Shortlisted from \textbf{864 teams} to top 150 nationally; ranked \textbf{51st} in second round. \hfill Sep 2025
  \item \textbf{National Semi-Finalist, Flipkart GRID 7.0} -- Techno-commercial hackathon by Flipkart Early Careers. \hfill Aug 2025
  \item \textbf{National Finalist, 3rd Runner-up -- DATASET '24:} Shipped an AI system in 36 hours; earned a \textbf{Nokia internship offer}. \hfill Dec 2024
\end{itemize}

\end{document}