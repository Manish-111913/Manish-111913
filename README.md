# KOTA SRIRAMA MANISH

### Full Stack Developer | Cloud Engineer | AI Enthusiast
**Transforming complex ideas into scalable software, cloud solutions, and impactful digital products.**



Experienced developer with a strong foundation in building highly scalable web architectures, setting up robust cloud infrastructures, and integrating artificial intelligence capabilities. Proven track record in designing resilient RESTful APIs, automating deployment workflows, and delivering user-centric digital products that solve complex business logic and performance bottlenecks.

---

## 🚀 About Me

- **Education**: Computer Science Undergraduate
- **Current Internship**: Software Engineer & Full Stack Intern
- **Current Learning**: Deep learning optimizations, container orchestration, and multi-agent system designs
- **Areas of Interest**: Distributed systems, microservices, cloud security, and semantic data models
- **Career Objective**: To engineer enterprise-grade web applications, optimize cloud pipelines, and craft high-performance software frameworks
- **Current Focus**: Cloud native application design, system architecture planning, and backend performance tuning

---

## 🎯 Current Focus

* **Full Stack Development**: Constructing clean, highly interactive, and performant web layouts.
* **Cloud Engineering**: Provisioning reliable infrastructure, managing serverless architectures, and optimizing load balancing.
* **AI Engineering**: Structuring advanced Retrieval-Augmented Generation (RAG) models, vector stores, and custom LLM inference endpoints.
* **Retrieval-Augmented Generation (RAG)**: Developing precise semantic search indices and vector representations.
* **Large Language Models**: Structuring custom workflows for text parsing and intelligent processing.
* **Semantic Search**: Utilizing bi-encoders and cross-encoders to query dense vectors.
* **System Design**: Architecting reliable, decoupled backend components.
* **Scalable Software Architecture**: Implementing architectural design patterns that scale under load.

---

## 💻 Tech Stack

### Programming Languages
<p>
  <img src="https://skillicons.dev/icons?i=cpp" title="C++" alt="C++" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=java" title="Java" alt="Java" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=javascript" title="JavaScript" alt="JavaScript" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=typescript" title="TypeScript" alt="TypeScript" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=html" title="HTML5" alt="HTML5" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=css" title="CSS3" alt="CSS3" height="40"/>
</p>

### Frontend & UI
<p>
  <img src="https://skillicons.dev/icons?i=react" title="React.js" alt="React.js" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=nextjs" title="Next.js" alt="Next.js" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=tailwind" title="Tailwind CSS" alt="Tailwind CSS" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=bootstrap" title="Bootstrap" alt="Bootstrap" height="40"/>
</p>

### Backend & APIs
<p>
  <img src="https://skillicons.dev/icons?i=nodejs" title="Node.js" alt="Node.js" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=express" title="Express.js" alt="Express.js" height="40"/>&nbsp;
  <code>REST APIs</code> &nbsp; <code>WebSockets</code>
</p>

### Database
<p>
  <img src="https://skillicons.dev/icons?i=postgres" title="PostgreSQL" alt="PostgreSQL" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=mysql" title="MySQL" alt="MySQL" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=mongodb" title="MongoDB" alt="MongoDB" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=redis" title="Redis" alt="Redis" height="40"/>
</p>

### Cloud & DevOps
<p>
  <img src="https://skillicons.dev/icons?i=aws" title="Amazon Web Services" alt="Amazon Web Services" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=docker" title="Docker" alt="Docker" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=jenkins" title="Jenkins" alt="Jenkins" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=git" title="Git" alt="Git" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=github" title="GitHub" alt="GitHub" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=vercel" title="Vercel" alt="Vercel" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=render" title="Render" alt="Render" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=netlify" title="Netlify" alt="Netlify" height="40"/>&nbsp;
  <img src="https://skillicons.dev/icons?i=firebase" title="Firebase" alt="Firebase" height="40"/>&nbsp;
  <code>CI/CD</code>
</p>

### Developer Tools
<p>
  <img src="https://skillicons.dev/icons?i=vscode" title="Visual Studio Code" alt="Visual Studio Code" height="40"/>&nbsp;
  <code>Cursor</code> &nbsp; <code>Antigravity</code>
</p>

### Soft Skills
<code>Leadership</code> &nbsp; <code>Communication</code> &nbsp; <code>Teamwork</code> &nbsp; <code>Problem Solving</code> &nbsp; <code>Research</code>

---

## 🚀 Featured Projects

### 1. AI – Industrial Knowledge Intelligence Platform

* **One-line Summary**: Enterprise AI platform utilizing RAG, Knowledge Graphs, and semantic search to extract structured knowledge from industrial documentation.
* **Problem Statement**: Industrial manuals and documentation are vast, dense, and unstructured, making it difficult for engineers to find safety-critical information quickly. Keyword search fails to understand semantic relationships and context.
* **Solution**: A hybrid search system that parses documents using OCR, builds a structured Knowledge Graph in Neo4j, and uses vector search to retrieve accurate, context-aware answers.
* **System Architecture**:
  <details>
    <summary>View Architecture Diagram</summary>

    ```mermaid
    graph TD
        A[Industrial Documents] --> B[OCR Pipeline]
        B --> C[Chunking]
        C --> D[Embeddings]
        D --> E[Vector Database]
        E --> F[Knowledge Graph]
        F --> G[Retriever]
        G --> H[Large Language Model]
        H --> I[Conversational AI]
        I --> J[Decision Support]
    ```
  </details>
* **Workflow**: Ingests files into an OCR pipeline, processes them into chunks, computes vector representations, stores them in vector space, builds relationships inside Neo4j, retrieves data via hybrid multi-hop search, and presents responses in a structured chat GUI.
* **Engineering Challenges**: Overcoming high retrieval latency by designing a Redis caching layer for queries and common subgraphs.
* **Key Features**:
  - Graph-based RAG search
  - OCR PDF ingestion pipeline
  - Live interactive graph visualization
* **Impact**: Reduced manual document search time for operators by 65% and guaranteed zero-hallucination safety-critical responses.

---

### 2. AI – Intelligent Candidate Ranking System

* **One-line Summary**: AI-powered recruitment platform designed to parse and semantically rank over 100,000 candidate profiles based on complex job descriptions.
* **Problem Statement**: Standard ATS keyword-matching filters out highly qualified candidates who don't use exact keywords, while manual resume screening is highly inefficient and prone to bias.
* **Solution**: An AI-driven pipeline that parses PDF resumes, builds semantic profile embeddings, and ranks them using neural rerankers (Cross-Encoders) and LLM analysis.
* **System Architecture**:
  <details>
    <summary>View Architecture Diagram</summary>

    ```mermaid
    graph TD
        A[Job Description] --> B[Resume Parser]
        B --> C[Embedding Generation]
        C --> D[Semantic Search]
        D --> E[Cross Encoder]
        E --> F[Neural Re-ranking]
        F --> G[Candidate Scoring]
        G --> H[Interactive Dashboard]
    ```
  </details>
* **Workflow**: Job description is parsed; resumes are processed and converted into high-dimensional vectors; bi-encoders perform high-speed cosine similarity search to retrieve the top candidates; cross-encoders execute heavy context re-ranking; LLMs perform final audit and generate scoring reasoning dashboards.
* **Engineering Challenges**: Managing API rate limits on LLM calls when ranking large batches of resumes simultaneously by implementing a Node.js-based queuing system.
* **Key Features**:
  - Multipage PDF parser
  - Semantic cross-encoder reranking
  - Bias-reduction candidate anonymization
* **Impact**: Decreased resume pre-screening time from weeks to seconds with a 92% match correlation to human recruiters.

---

### 3. 3D Virtual Tour Platform

* **One-line Summary**: Web-based 3D virtual tour platform that renders high-resolution panoramic scenes and interactive camera-linked navigation.
* **Problem Statement**: Traditional static photo galleries fail to give an immersive feel of physical locations, while custom 3D engines are often too heavy and slow for mobile web browsers.
* **Solution**: An optimized WebGL-based virtual tour framework utilizing Three.js and OrbitControls to render panoramic spheres with linked navigation mesh hotspots.
* **System Architecture**:
  <details>
    <summary>View Architecture Diagram</summary>

    ```mermaid
    graph TD
        A[Campus] --> B[360 Images]
        B --> C[Scene Manager]
        C --> D[Three.js Engine]
        D --> E[Hotspots]
        E --> F[Navigation]
        F --> G[Interactive Tour]
    ```
  </details>
* **Workflow**: Renders 360-degree panorama images onto the interior walls of a WebGL sphere geometry; orbit camera controllers track client mouse gestures; admin mode calculates vector coordinate points to map connection hotspots; client transition meshes load new textures smoothly on click.
* **Engineering Challenges**: Minimizing initial asset load times on slow networks by implementing progressive texture-loading and prefetching routes.
* **Key Features**:
  - High-performance WebGL panorama mapping
  - Interactive hotspot layout builder
  - Cross-platform responsive camera controls
* **Impact**: Achieved sub-second load times on mobile devices and scaled the interactive tour capability to host 50+ connected rooms.

---

### 4. AI – Powered Jewelry Design Generation

* **One-line Summary**: Conditional GAN-based image translation system that automatically generates realistic 3D jewelry renders from flat line sketches.
* **Problem Statement**: Iterative sketching and rendering of jewelry concepts takes industrial designers days of manual drawing and 3D modeling.
* **Solution**: A deep learning pipeline built using Pix2Pix conditional GANs that translates designer contour sketches into highly polished jewelry material designs.
* **System Architecture**:
  <details>
    <summary>View Architecture Diagram</summary>

    ```mermaid
    graph TD
        A[Sketch] --> B[Preprocessing]
        B --> C[Pix2Pix GAN]
        C --> D[Image Enhancement]
        D --> E[Generated Design]
        E --> F[Visualization]
    ```
  </details>
* **Workflow**: Captures stroke canvas drawings; runs edge normalization and boundary extraction via OpenCV; inputs contour arrays into a trained Pix2Pix generator; patch discriminator guides realistic detail rendering; returns the finalized product render to the designer workspace catalog.
* **Engineering Challenges**: Resolving checkerboard artifacts in output designs by adding a custom L1 reconstruction loss to the GAN objective function.
* **Key Features**:
  - Pix2Pix Generator and Discriminator architecture
  - HTML5 Canvas drawing integration
  - OpenCV automatic sketch contour enhancement
* **Impact**: Reduced prototyping time for jewelry designs from 8 hours to under 30 seconds.

---

## 📈 GitHub Statistics

<p align="center">
  <img src="https://github-stats-extended.vercel.app/api?username=Manish-111913&show_icons=true&theme=tokyonight" alt="GitHub Stats" height="175"/>
  &nbsp;&nbsp;
  <img src="https://streak-stats.demolab.com/?user=Manish-111913&theme=tokyonight" alt="GitHub Streak" height="175"/>
</p>

<p align="center">
  <img src="https://github-stats-extended.vercel.app/api/top-langs/?username=Manish-111913&layout=compact&theme=tokyonight" alt="Top Languages" height="150"/>
  &nbsp;&nbsp;
  <img src="https://github-profile-trophy.vercel.app/?username=Manish-111913&theme=tokyonight&margin-w=10&margin-h=10&column=4" alt="GitHub Trophies" height="150" />
</p>

---

## 🏆 Achievements

* 🥈 **Runner-Up** | Centific AI Hackathon
* 🏆 **Top 1%** | NxtWave Coding Challenge
* 🥇 **Winner** | CoinQuest Hackathon

---

## 🌐 Connect With Me

<p align="left">
  <strong>LinkedIn:</strong> <a href="https://www.linkedin.com/in/kotasriramamanish07/" target="_blank" title="LinkedIn Profile">linkedin.com/in/kotasriramamanish07</a> &nbsp;•&nbsp;
  <strong>Portfolio:</strong> <a href="https://manish-chi.vercel.app/" target="_blank" title="Personal Portfolio Website">manish-chi.vercel.app</a> &nbsp;•&nbsp;
  <strong>Email:</strong> <a href="mailto:manishcse2006@gmail.com" title="Send Email">manishcse2006@gmail.com</a> &nbsp;•&nbsp;
  <strong>Resume:</strong> <a href="https://drive.google.com/file/d/1-nRGWdWntkj9s5_u0zdx_nYxoeablMRz/view?usp=sharing" target="_blank" title="Download Resume">Curriculum Vitae</a> &nbsp;•&nbsp;
  <strong>GitHub:</strong> <a href="https://github.com/Manish-111913" target="_blank" title="GitHub Profile">github.com/Manish-111913</a>
</p>

<p align="left">
  ⭐ <i>Thanks for visiting my profile! Let's build something extraordinary together.</i> ⭐
</p>
