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

\geometry{top=0.3in, bottom=0.3in, left=0.45in, right=0.45in}

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
  \vspace{-6pt}\bfseries\raggedright\normalsize\uppercase
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
  \vspace{0pt}\item
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
  {\LARGE\textbf{Aakarshak Swaraj}} \\[2pt]
  \small
  +91-81416 23953 \;$|$\;
  \href{mailto:aakarshak.work@gmail.com}{aakarshak.work@gmail.com} \;$|$\;
  \href{https://www.linkedin.com/in/aakarshak-swaraj-a3ba21290}{LinkedIn} \;$|$\;
  \href{https://akiportfolio.vercel.app/}{Portfolio} \;$|$\;
  \href{https://github.com/Krishna-Kilrofkansa}{GitHub} \;$|$\;
  Bengaluru, India
\end{center}
\vspace{-4pt}

%-----------SUMMARY-----------
\section{Summary}
\small{Full-stack Engineer specializing in AI-powered applications, with internship experience building scalable web platforms, backend systems, NLP pipelines, and mobile applications. Experienced with TypeScript, React, Next.js, Spring Boot, Python, Kotlin, AWS, and applied ML. Proven results: \textbf{93.4\% cancer detection accuracy}, \textbf{AUC 0.81} IPL prediction, \textbf{95\% NLP precision} in civic monitoring, and a nationally ranked disaster platform (top 150 of 864 teams, SIH 2025). Proficient in Python, TypeScript, Kotlin, C++, PyTorch, Next.js, React, and AWS.}
\vspace{-2pt}

%-----------EDUCATION-----------
\section{Education}
\resumeSubHeadingListStart
  \resumeSubheading
    {Vellore Institute of Technology}{August 2023 -- August 2027 (Expected)}
    {B.Tech in Computer Science, Specialization in AIML; GPA: 8.62/10.0}{Chennai, India}
\resumeSubHeadingListEnd

%-----------EXPERIENCE-----------
\section{Experience}
\resumeSubHeadingListStart

  \resumeSubheading
    {SDE Intern $|$ Taslasoft $|$ Hyderabad, India}{February 2026 -- April 2026}
    {}{}
    \vspace{-12pt}
    \resumeItemListStart
      \resumeItem{Developed a real-time Reddit social intelligence pipeline monitoring \textbf{15+ targeted subreddits}, building a geo-temporal aggregation system that mapped incident activity to geographic clusters with near-real-time latency.}
      \resumeItem{Achieved \textbf{95\% system precision} via a 3-stage NLP detection pipeline (keyword rules $\rightarrow$ sentiment analysis $\rightarrow$ transformer classification) with human-in-the-loop validation; operationalized in a civic monitoring deployment identifying \textbf{200+ harmful posts} in its pilot phase.}
    \resumeItemListEnd

  \resumeSubheading
    {SDE Intern $|$ Qcecuring Technologies $|$ Delhi, India}{October 2025 -- December 2025}
    {}{}
    \vspace{-12pt}
    \resumeItemListStart
      \resumeItem{Architected a self-service code-signing platform with client-side hashing, eliminating private key exposure and enabling on-demand artifact signing without uploading sensitive build files to remote servers.}
      \resumeItem{Delivered a \textbf{PKI-as-a-Service} module with quorum-based multi-approver workflows, automated certificate lifecycle management, and tamper-proof audit logging for enterprise-grade non-repudiation and compliance.}
    \resumeItemListEnd

\resumeSubHeadingListEnd

%-----------PROJECTS-----------
\section{Projects}
\resumeSubHeadingListStart


  % ── UPDATED: VARUNA ──────────────────────────────────────────────────────────
  \resumeProjectHeading
    {\href{https://varuna001.vercel.app/}{\textbf{VARUNA -- Citizen Disaster Reporting Platform (SIH 2025)}} \href{https://github.com/Krishna-Kilrofkansa/VARUNA}{\textcolor{blue}{GitHub}} $|$ \textit{Next.js 14, TypeScript, Tailwind CSS, Leaflet, Recharts}}{}
    \resumeItemListStart
      \resumeItem{Led a \textbf{5-person team} to build VARUNA, a \textbf{TypeScript/Next.js 14} citizen disaster-reporting platform processing \textbf{5,000+ monthly reports} with a multi-stage CV+NLP validation pipeline that reduced false submissions by $\sim$\textbf{35\%} --- shortlisted from \textbf{864 teams} nationally and ranked \textbf{51st} at Smart India Hackathon 2025.}
    \resumeItemListEnd

  % ── UPDATED: ehub (formerly EntertainmentHub, new live link) ──────────────────
  \resumeProjectHeading
    {\textbf{\href{https://ehubdelta.vercel.app/}{EHub}} \href{https://github.com/Krishna-Kilrofkansa/ehub}{\textcolor{blue}{GitHub}} $|$ \textit{Spring Boot, ReactJS, MongoDB}}{}
    \resumeItemListStart
      \resumeItem{Created a full-stack content discovery platform with a \textbf{Spring Boot} backend and \textbf{React} frontend, integrating \textbf{5 third-party REST APIs} across 4 content domains (movies, anime, manhwa, books) with JWT authentication and optimized MongoDB retrieval.}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{\href{https://team-dromos-website.vercel.app/}{Team Dromos -- Official Website}}
    \href{https://github.com/Krishna-Kilrofkansa/team-dromos-website}{\textcolor{blue}{GitHub}}$|$ \textit{Next.js, GSAP, React, TypeScript}}{}
    \resumeItemListStart
      \resumeItem{Crafted the official website for Team Dromos in Next.js and GSAP, delivering \textbf{99/100 Lighthouse performance} on desktop (0.7s LCP, 0ms TBT, 100/100 Best Practices \& SEO) while strengthening recruitment, outreach, and sponsor visibility for the team's Global Hyperloop Competition 2025 campaign.}
    \resumeItemListEnd
    
  % ── NEW: TSlate ───────────────────────────────────────────────────────────────
  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/tslate}{TSlate -- Offline Voice Translator}} \href{https://github.com/Krishna-Kilrofkansa/tslate}{\textcolor{blue}{GitHub}} $|$ \textit{C++, Kotlin, Whisper.cpp, NLLB-200, CTranslate2, JNI/NDK, Android}}{}
    \resumeItemListStart
      \resumeItem{Engineered a fully offline Android voice translator (Hindi/Hinglish $\rightarrow$ Kannada) targeting \textbf{$<$15s} end-to-end latency by integrating Whisper.cpp (ggml-tiny) for STT and NLLB-200 600M INT8 for translation via \textbf{custom C++ JNI/NDK bindings} (CTranslate2); implemented Unicode-based Devanagari/Latin routing and a Kotlin normalization layer for Hinglish text handling.}
    \resumeItemListEnd

  % ── NEW: BhashaBridge ─────────────────────────────────────────────────────────
  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/BhashaBridge}{BhashaBridge -- Indian Language Translator}} \href{https://github.com/Krishna-Kilrofkansa/BhashaBridge}{\textcolor{blue}{GitHub}} $|$ \textit{Kotlin, Jetpack Compose, MVVM, Room, Gemini API, Android}}{}
    \resumeItemListStart
      \resumeItem{Built a Hindi $\leftrightarrow$ Dravidian language translator for Android (Kotlin + \textbf{MVVM} + Jetpack Compose) integrating \textbf{Gemini API} for neural translation with \textbf{Room SQLite} reactive persistence, a sealed-class \texttt{StateFlow} UI architecture, and BCP47-localized STT/TTS across Tamil, Telugu, Kannada, and Malayalam.}
    \resumeItemListEnd

  % ── NEW: Legal Sentiment Analyzer ─────────────────────────────────────────────
  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/legal-sentiment-analyzer}{AI Legal Sentiment Analyzer}} \href{https://github.com/Krishna-Kilrofkansa/legal-sentiment-analyzer}{\textcolor{blue}{GitHub}} $|$ \textit{Python, IBM watsonx.ai, FLAN-T5, Watson ML, Jupyter}}{}
    \resumeItemListStart
      \resumeItem{Developed a few-shot legal document sentiment classifier on \textbf{IBM watsonx.ai} using FLAN-T5 via Watson Machine Learning, automating positive/negative/neutral tagging of case summaries and contracts with prompt-engineered templates to accelerate compliance review workflows for law firms.}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{\href{https://akiportfolio.vercel.app/circles.apk}{Circles -- Cross-Platform Focus \& Productivity App}}
    \href{https://github.com/krishna-kilrofkansa/circle}{\textcolor{blue}{GitHub}} $|$ \textit{Flutter, Firebase, Dart}}{}
    \resumeItemListStart
      \resumeItem{Shipped a cross-platform productivity app in Flutter/Dart with \textbf{Firebase-backed} persistent state, real-time session tracking, and goal-setting workflows and deployed as an Android APK.}
    \resumeItemListEnd
    
  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/ipl-prediction}{IPL Match Prediction \& Decision Support System}}
    \href{https://github.com/Krishna-Kilrofkansa/ipl-prediction}{\textcolor{blue}{GitHub}}$|$ \textit{Python, Scikit-learn, SQLite, Pandas, NumPy, SciPy}}{}
    \resumeItemListStart
      \resumeItem{Designed an IPL outcome predictor achieving \textbf{AUC 0.81} across 1,169 matches (2008--2026) using a calibrated soft-voting ensemble with 20+ engineered features and an SQLite-backed incremental retraining pipeline; implemented a constrained \textbf{Playing XI optimizer} enforcing role composition and overseas limits.}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{Breast Cancer Detection} $|$ \textit{Python, PyTorch, CNN, ResNet50, SimCLR, Deep Learning}}{}
    \resumeItemListStart
      \resumeItem{Fine-tuned \textbf{ResNet50} with SimCLR contrastive pretraining on \textbf{7,909 BreakHis} histopathology images, achieving \textbf{93.4\% accuracy} and \textbf{0.92 F1-score} --- a $\sim$7\% improvement over the CNN baseline --- using PyTorch with augmentation-heavy preprocessing.}
    \resumeItemListEnd

  \resumeProjectHeading
    {\textbf{\href{https://github.com/Krishna-Kilrofkansa/EYERIS}{EYERIS -- Privacy-Preserving Autonomous Robot}}
    \href{https://github.com/Krishna-Kilrofkansa/EYERIS}{\textcolor{blue}{GitHub}}$|$ \textit{Python, OpenCV, MediaPipe, Arduino, Embedded Systems}}{}
    \resumeItemListStart
      \resumeItem{Deployed a privacy-preserving robot achieving \textbf{$<$50ms} real-time human detection latency via MediaPipe pose estimation and OpenCV, with a dual-sensor stack (ultrasonic + servo) enforcing a \textbf{$\sim$30cm avoidance threshold} across multiple lab environments.}
    \resumeItemListEnd


\resumeSubHeadingListEnd

%-----------SKILLS-----------
\section{Skills}
\begin{itemize}[leftmargin=0in, label={}, itemsep=1pt, topsep=0pt, parsep=0pt]
\small\item{
\textbf{Languages:} Python, C++, TypeScript, Kotlin, JavaScript, Dart \quad
\textbf{Frontend:} React.js, Next.js, Jetpack Compose \\
\textbf{Backend \& Systems:} Node.js, Spring Boot, FastAPI, REST APIs, Distributed Systems \\
\textbf{ML \& AI:} NLP, Computer Vision, LLMs, RAG, PyTorch, OpenCV, Hugging Face Transformers, fine-tuning \\
\textbf{Mobile:} Android (Kotlin, MVVM, Room), Flutter/Dart \quad
\textbf{Databases:} PostgreSQL, MySQL, MongoDB, SQLite \\
\textbf{Cloud \& DevOps:} AWS (EC2, S3, Lambda), Docker, CI/CD \quad
\textbf{Tools:} Git, Linux, Gradle, Maven, MLflow
}
\end{itemize}
\vspace{-4pt}

%-----------CERTIFICATIONS-----------
\section{Certifications}
\begin{itemize}[leftmargin=0.15in, itemsep=1pt, topsep=0pt, parsep=0pt]
  \small
    \item \textbf{Anthropic AI courses} \href{https://verify.skilljar.com/c/ufc5sweipoht}{\textcolor{blue}{Certificate}} \hfill May 2026
  
  \item \textbf{Generative AI Using IBM Watsonx} -- IBM \href{https://courses.vit.skillsnetwork.site/certificates/cb164478ebbc423cb0f9f18a502d59f6}{\textcolor{blue}{Certificate}} \hfill Jun 2025
  \item \textbf{Supervised Machine Learning: Regression and Classification} -- DeepLearning.AI \href{https://www.coursera.org/account/accomplishments/verify/TLP3MHO43N32}{\textcolor{blue}{Certificate}} \hfill Dec 2024
\end{itemize}

%-----------ACHIEVEMENTS-----------
\section{Achievements}
\begin{itemize}[leftmargin=0.15in, itemsep=1pt, topsep=0pt, parsep=0pt]
  \small
  \item \textbf{Gold Level -- WorldQuant BRAIN International Quant Championship 2026:} Advanced to Stage 2 (National Level); ranked among the \textbf{top 20\% of teams globally} in a quantitative research challenge. \hfill Jun 2026
  \item \textbf{SIH 2025 -- VARUNA:} Shortlisted from \textbf{864 teams} to top 150 nationally; ranked \textbf{51st} in the internal second round. \hfill Sep 2025
  \item \textbf{National Semi-Finalist, Flipkart GRID 7.0} -- Techno-commercial hackathon by Flipkart Early Careers. \hfill Aug 2025
  \item \textbf{National Finalist, 3rd Runner-up -- DATASET '24:} Prototyped and shipped an AI system in under 36 hours; earned a \textbf{Nokia internship offer}. \hfill Dec 2024
\end{itemize}

\end{document}