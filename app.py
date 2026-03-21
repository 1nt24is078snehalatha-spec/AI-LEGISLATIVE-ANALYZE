from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import pdfplumber
import re
import os

from search_engine import create_embeddings, search
from nlp_utils import compress_text, extract_keywords,extract_insights
from summarizer import generate_summary

app = Flask(__name__)
CORS(app)

# -------------------------------
# LOAD PDF
# -------------------------------
print("Loading PDF...")

text = ""
with pdfplumber.open("documents/it_act_2000.pdf") as pdf:
    for page in pdf.pages:
        t = page.extract_text()
        if t:
            text += t.lower()

print("PDF Loaded ✅")

# -------------------------------
# SMART CHUNKING (SECTION BASED)
# -------------------------------
sections = re.split(r'(section\s+\d+)', text)

chunks = []
for i in range(1, len(sections), 2):
    chunk = sections[i] + sections[i+1]
    chunks.append(chunk)

print("Total chunks:", len(chunks))

# -------------------------------
# CREATE EMBEDDINGS (AI)
# -------------------------------
print("Creating embeddings...")
embeddings = create_embeddings(chunks)
print("Embeddings ready ✅")

# -------------------------------
# COMMON PROCESS FUNCTION (DRY)
# -------------------------------
def process_query(query):
    matched_chunks = search(query, chunks, embeddings)
    results = []

    for chunk in matched_chunks:
        compressed = compress_text(chunk)
        summary = generate_summary(compressed, query)
        keywords = extract_keywords(compressed)

        penalty, info, rights = extract_insights(compressed)
        section = extract_section(chunk)

        # ✅ FILTER BAD RESULTS
        if len(summary["summary"]) > 30:
            results.append({
                "summary": "📌 " + summary["summary"],
                "section": section,
                "keywords": ", ".join(keywords),
                "penalty": penalty,
                "info": info,
                "rights": rights
            })

    return results
def extract_section(chunk):
    import re
    match = re.search(r'section\s+\d+[a-zA-Z]*', chunk)
    if match:
        return match.group().upper()
    return "Unknown Section"

# -------------------------------
# API ROUTE
# -------------------------------
@app.route('/api/search', methods=['POST'])
def analyze():

    if request.is_json:
        data = request.get_json()
        query = data.get("query", "").lower()
    else:
        query = request.form.get("query", "").lower()

    results = process_query(query)

    return jsonify({"results": results})


# -------------------------------
# UI (DASHBOARD)
# -------------------------------
HTML = """
<h1 style="text-align:center;">⚖️ AI Legislative Analyzer</h1>

<form method="post" style="text-align:center;">
    <input name="query" placeholder="Enter your legal query" required style="width:300px; padding:8px;">
    <button type="submit">Search</button>
</form>

<hr>

{% for r in results %}
<div style="border:1px solid #ccc; padding:15px; margin:10px; border-radius:10px;">
    <h3 style="color:black;">📚 {{ r.section }}</h3>

    <h3 style="color:blue;">🧠 Summary</h3>
    <p>{{ r.summary }}</p>

    {% if r.penalty %}
    <h4 style="color:red;">🟥 Penalty</h4>
    <p>{{ r.penalty }}</p>
    {% endif %}

    {% if r.info %}
    <h4 style="color:green;">🟩 What you should know</h4>
    <p>{{ r.info }}</p>
    {% endif %}

    {% if r.rights %}
    <h4 style="color:orange;">🟧 Rights</h4>
    <p>{{ r.rights }}</p>
    {% endif %}

    <h4 style="color:purple;">🟦 Keywords</h4>
    <p>{{ r.keywords }}</p>

</div>
{% endfor %}
"""


@app.route('/ui', methods=["GET", "POST"])
def ui():
    results = []

    if request.method == "POST":
        query = request.form.get("query", "").lower()
        results = process_query(query)

    return render_template_string(HTML, results=results)


# -------------------------------
# HOME ROUTE
# -------------------------------
@app.route('/')
def home():
    return "AI Legislative Analyzer Backend Running 🚀"


# -------------------------------
# RUN SERVER (DEPLOYMENT READY)
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))   # 🔥 for Railway
    app.run(host="0.0.0.0", port=port, debug=False)