 LexAI — AI Legislative Analyzer

Intelligent Semantic Search over India's Information Technology Act, 2000

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![NLP](https://img.shields.io/badge/NLP-spaCy-green)
![AI](https://img.shields.io/badge/AI-Transformers-orange)
![Status](https://img.shields.io/badge/Status-Local%20Deployment-yellow)


 Project Overview

LexAI is an AI-powered legal research assistant that allows users to query the Information Technology Act, 2000 using natural language.

Instead of manually reading long legal documents, users can ask questions like:
"What is the punishment for hacking?"
"What are my rights under IT Act?"

and receive structured, simplified answers instantly.


 Key Features

* Natural language query support
* Semantic search using transformer embeddings
* Automatic legal text summarization
* Extraction of penalties, rights, and obligations
* Clean dark-themed user interface
* REST API support

 How It Works

1. PDF Processing
   Extracts text from the IT Act 2000 using pdfplumber

2. Chunking
   Splits content into section-wise segments

3. Embeddings
   Uses sentence-transformers (MiniLM) to convert text into vectors

4. Semantic Search
   Matches user query with legal sections using cosine similarity

5. NLP Processing
   Uses spaCy for keyword extraction, sentence filtering, and classification

6. Summarization
   Generates concise legal explanations


 Tech Stack

| Layer       | Technology            | Purpose            |
| ----------- | --------------------- | ------------------ |
| Backend     | Flask                 | API and routing    |
| Frontend    | HTML, CSS, JavaScript | User interface     |
| NLP         | spaCy                 | Text processing    |
| Embeddings  | sentence-transformers | Semantic search    |
| PDF Parsing | pdfplumber            | Extract legal text |


 Project Structure


AI-legislative-analyzer/
│── app.py
│── search_engine.py
│── nlp_utils.py
│── summarizer.py
│── requirements.txt
│
├── documents/
│   └── it_act_2000.pdf
│
└── static/
    ├── index.html
    ├── style.css
    └── script.js

 Setup and Run Locally

 1. Clone Repository

git clone https://github.com/your-username/AI-legislative-analyzer.git
cd AI-legislative-analyzer

 2. Create Virtual Environment

python -m venv venv
venv\Scripts\activate

 3. Install Dependencies

pip install -r requirements.txt

 4. Download spaCy Model

python -m spacy download en_core_web_sm

 5. Add IT Act PDF

Place the file in:

documents/it_act_2000.pdf

 6. Run Application

python app.py

 7. Open in Browser

http://localhost:5000

 API Example

POST /api/search

```json
{
  "query": "hacking punishment"
}
```



 Backend Deployment Status

The backend is currently not deployed online due to memory limitations on free-tier platforms such as Render.

The application requires:

* Transformer model (~90MB)
* NLP processing (spaCy)

These exceed free-tier memory limits.
 Current Status

* Works correctly in local environment
* Not deployed online yet



Deployment is planned on a platform with higher memory support such as Railway or a cloud virtual machine.


 Future Improvements

* Deployment on scalable cloud infrastructure
* Support for additional legal documents
* Improved summarization using advanced models
* Voice-based query support





