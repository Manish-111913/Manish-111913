# AI Intelligent Candidate Ranking System

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![Node.js](https://img.shields.io/badge/Node.js-20.x-339933?logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-1.5_Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/)

An AI-driven HR technology application that automates candidate resume parsing, semantic matching, and intelligent ranking based on customized job descriptions. Powered by Google Gemini and advanced LLM prompt engineering, this tool matches skills, experience, and certifications while avoiding the keyword-matching biases of traditional ATS.

---

## 🔗 System Architecture

```
+------------+     +-------------------+     +------------------+
|  Resume    | --> |  Document Parser  | --> | Structured Text  |
|  PDF/DOCX  |     |  (pdfjs / pdfplumber)   | (Skills, Exp, Ed)|
+------------+     +-------------------+     +------------------+
                                                      |
                                                      v
+------------+     +-------------------+     +------------------+
| Job        | --> |   Gemini 1.5      | <---| Semantic Scorer  |
| Desc       |     |   Evaluator       |     | & Alignment      |
+------------+     +---------+---------+     +------------------+
                             |
                             v
                   +---------+---------+
                   | MongoDB Stats     |
                   | & Rankings        |
                   +---------+---------+
                             |
                             v
                   +---------+---------+
                   | React Dashboard   |
                   | (Filter & View)   |
                   +-------------------+
```

---

## ⚡ Features

- **Multipage Resume Parsing**: High-fidelity text extraction from PDF and Word documents.
- **Dynamic Semantic Scoring**: Evaluates candidate fit across sub-categories: tech stack matches, domain experience, soft skills, and career progression.
- **Interactive Scoring Analytics**: Detailed AI breakdown showing the rationale behind each rating.
- **Batch Processing & Ranking**: Upload dozens of resumes simultaneously and receive a ranked leaderboard in seconds.
- **Advanced Filters**: Filter candidates by score ranges, core technologies, and years of experience.

---

## 💻 Tech Stack

- **Frontend**: Next.js 15, Tailwind CSS
- **Backend API**: Node.js, Express.js
- **AI Processing**: Google Gemini API (gemini-1.5-flash)
- **Database**: MongoDB
- **File Storage**: AWS S3 (for secure resume uploads)

---

## 🛠️ Installation & Setup

### Prerequisites
- Node.js 20+
- MongoDB instance (local or Atlas)
- Google Gemini API Key

### Step 1: Clone the Repository
```bash
git clone https://github.com/Manish-111913/AI-Candidate-Ranking.git
cd AI-Candidate-Ranking
```

### Step 2: Configure Backend Server
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a `.env` file:
   ```env
   PORT=5000
   MONGO_URI=mongodb://localhost:27017/candidate_ranking
   GEMINI_API_KEY=your_gemini_api_key
   AWS_ACCESS_KEY_ID=your_aws_s3_key
   AWS_SECRET_ACCESS_KEY=your_aws_s3_secret
   AWS_BUCKET_NAME=your_s3_bucket
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Start the server:
   ```bash
   npm run dev
   ```

### Step 3: Configure Frontend Dashboard
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Create a `.env.local` file:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:5000/api
   ```
3. Install dependencies and start:
   ```bash
   npm install
   npm run dev
   ```

---

## 📂 Folder Structure

```
AI-Candidate-Ranking/
├── backend/
│   ├── src/
│   │   ├── config/         # MongoDB & AWS SDK setups
│   │   ├── controllers/    # Resume parsing & Gemini API execution
│   │   ├── models/         # Resume and Job Description schemas
│   │   └── routes/         # Express endpoints
│   ├── package.json
│   └── server.js
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/     # Upload widgets, candidate tables, radar charts
│   │   └── app/            # Next.js pages
│   └── package.json
├── README.md
└── architecture.png
```

---

## 🚀 Future Scope

- Add automated resume anonymization to eliminate unconscious gender, race, or age bias.
- Integrate with external job boards (LinkedIn, Indeed APIs) for direct candidate importing.
- Multi-agent HR framework: spawn AI agents to conduct asynchronous pre-screening chatbot interviews.

---

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.
