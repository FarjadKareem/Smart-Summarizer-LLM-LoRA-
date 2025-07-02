import os
import time
from together import Together  # Import the new Together client
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM

# --- AGENT 1: KeywordAgent ---
def expand_keywords(user_keywords):
    prompt = f"Expand and suggest related academic keywords for: {user_keywords}"
    
    # Initialize the Together client
    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))  
    
    # Request completion from the model
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=[{"role": "user", "content": prompt}]
    )
    result = completion.choices[0].message.content.split(',')
    time.sleep(1.1)
    return [kw.strip() for kw in result if kw.strip()]

# --- AGENT 2: SearchAgent ---
def search_papers(keywords):
    import requests
    results = []
    for kw in keywords:
        url = f"http://export.arxiv.org/api/query?search_query=all:{kw}&start=0&max_results=3"
        # For demonstration, we mock the data:
        results.append({
            "title": f"Sample Paper on {kw}",
            "authors": ["Author A", "Author B"],
            "abstract": f"This is an abstract about {kw}.",
            "year": 2023,
            "citations": 42,
            "id": f"arxiv_{kw}",
            "url": f"https://arxiv.org/abs/{kw.replace(' ', '_')}"
        })
    return results

# --- AGENT 3: RankAgent ---
def rank_papers(papers, keywords):
    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
    def relevance(paper):
        prompt = f"Given the keywords {keywords}, rate the relevance (0-1) of this paper: {paper['title']} - {paper['abstract']}"
        try:
            completion = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",
                messages=[{"role": "user", "content": prompt}]
            )
            score = float(completion.choices[0].message.content.strip())
        except:
            score = 0.5
        time.sleep(1.1)
        return score
    
    for p in papers:
        p['relevance'] = relevance(p)
    papers.sort(key=lambda x: (x['relevance'], x['citations'], x['year']), reverse=True)
    return papers[:3]

# --- AGENT 4: SummaryAgent ---
def summarize_paper(paper):
    tokenizer = AutoTokenizer.from_pretrained("./lora-llama3-3b-arxiv/final")
    model = AutoModelForCausalLM.from_pretrained("./lora-llama3-3b-arxiv/final")
    
    input_text = f"Title: {paper['title']}\nAbstract: {paper['abstract']}"
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
    
    outputs = model.generate(inputs["input_ids"], max_length=200)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return {
        "summary": summary,
        "methodology": "Methodology details (mocked).",
        "contributions": "Key contributions (mocked).",
        "limitations": "Limitations and gaps (mocked)."
    }

# --- AGENT 5: CompareAgent ---
def compare_summaries(summaries):
    client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
    prompt = (
        "Given the following paper summaries, identify:\n"
        "- Common findings\n- Contradictory insights\n- Research gaps\n\n"
        f"{summaries}\n"
        "Provide a structured comparative analysis."
    )
    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=[{"role": "user", "content": prompt}]
    )
    result = completion.choices[0].message.content
    time.sleep(1.1)
    return result

# --- LangGraph Pipeline ---
def run_graph(user_keywords):
    expanded_keywords = expand_keywords(user_keywords)
    papers = search_papers(expanded_keywords)
    top_papers = rank_papers(papers, expanded_keywords)
    summarized_papers = []
    for p in top_papers:
        s = summarize_paper(p)
        p.update(s)
        summarized_papers.append({
            "title": p["title"],
            "authors": p["authors"],
            "year": p["year"],
            "citations": p["citations"],
            "summary": p["summary"],
            "url": p["url"]
        })
    comparative_analysis = compare_summaries([p["summary"] for p in summarized_papers])
    report = {
        "topic_summary": f"Expanded keywords: {', '.join(expanded_keywords)}",
        "summarized_papers": summarized_papers,
        "comparative_analysis": comparative_analysis
    }
    return report

# --- PDF Export Stub ---
def export_to_pdf(result):
    from fpdf import FPDF
    import unicodedata

    def clean_text(text):
        # Normalize and replace common problematic characters
        text = unicodedata.normalize("NFKD", text)
        text = text.replace("’", "'").replace("“", '"').replace("”", '"')
        text = text.replace("–", "-").replace("—", "-")
        return text.encode('latin-1', 'replace').decode('latin-1')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Research Summary", ln=True, align='C')
    pdf.ln(10)

    pdf.multi_cell(0, 10, f"Topic Summary:\n{clean_text(result['topic_summary'])}\n")
    pdf.ln(5)

    for i, paper in enumerate(result["summarized_papers"], 1):
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(0, 10, f"Paper {i}: {clean_text(paper['title'])}", ln=True)
        pdf.set_font("Arial", size=12)
        authors = clean_text(', '.join(paper['authors']))
        summary = clean_text(paper['summary'])
        url = clean_text(paper['url'])
        pdf.multi_cell(0, 10, f"Authors: {authors}\nYear: {paper['year']} | Citations: {paper['citations']}\nSummary: {summary}\nURL: {url}\n")
        pdf.ln(2)

    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(0, 10, "Comparative Analysis", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, clean_text(result["comparative_analysis"]))

    pdf.output("resummary.pdf")
    return "resummary.pdf"


# --- Visualization Stub ---
def visualize_output(result):
    import pandas as pd
    import matplotlib.pyplot as plt
    import os
    from wordcloud import WordCloud

    papers = result["summarized_papers"]
    df = pd.DataFrame(papers)

    
    os.makedirs("visualizations", exist_ok=True)

    # Citations bar chart
    plt.figure(figsize=(8, 4))
    plt.bar(df["title"], df["citations"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Citations per Paper")
    plt.tight_layout()
    plt.savefig("visualizations/citations_bar.png")
    plt.close()

    # Years bar chart
    plt.figure(figsize=(8, 4))
    df["year"].value_counts().sort_index().plot(kind="bar")
    plt.title("Publication Years")
    plt.tight_layout()
    plt.savefig("visualizations/years_bar.png")
    plt.close()

    # Word cloud from comparative analysis
    wc = WordCloud(width=800, height=400, background_color="white").generate(result["comparative_analysis"])
    wc.to_file("visualizations/comparative_wordcloud.png")

    return df
