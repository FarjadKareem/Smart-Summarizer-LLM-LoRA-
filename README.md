# 📚 Smart Summarizer (LLM + LoRA + LangGraph)

A smart academic summarization system that fine-tunes Large Language Models (LLMs) using **LoRA** and automates literature review through **LangGraph**-based multi-agent orchestration.

---

## 🚀 Features

- 🔍 Summarizes research papers from the **arXiv dataset** using LoRA-tuned **LLaMA/Mistral** models  
- 🤖 Includes a multi-agent system using **LangGraph**:  
  - `KeywordAgent`  
  - `SearchAgent`  
  - `RankAgent`  
  - `SummaryAgent`  
  - `CompareAgent`  
- ⚖️ Evaluated with **ROUGE, BLEU, BERTScore**, and LLM-as-a-Judge (fluency, factuality, coverage)  
- 🧪 Compare summaries from base and fine-tuned models  
- 🧠 Upload paper + auto-score via **Together.ai API**  
- 📊 Interactive frontend via **Streamlit/Gradio**  

---

## 🔧 How It Works

1. **Data Preprocessing** → Extracts articles and abstracts from **arXiv** dataset  
2. **LoRA Fine-Tuning** → Uses Hugging Face PEFT to fine-tune attention layers  
3. **Summary Generation** → Generates summaries from base and tuned models  
4. **Evaluation** → Quantitative and qualitative evaluation with LLM-as-a-Judge  
5. **Multi-Agent System** → Uses **LangGraph agents** to simulate automated literature review  
6. **Web App** → Upload a paper, generate and compare summaries, auto-score  

---

## 📊 Results

### 📈 Quantitative Evaluation (10 samples)

| Metric         | Fine-Tuned Model | Base Model |
|----------------|------------------|------------|
| ROUGE-1        | 0.2732           | 0.2744     |
| ROUGE-L        | 0.1403           | 0.1417     |
| BLEU           | 0.0264           | 0.0264     |
| BERTScore (F1) | 0.8303           | 0.8303     |

⚠️ **Note:** Both models returned nearly identical outputs due to a generation issue. Improvements are expected after fixing LoRA inference or decoding parameters.

---

### 🧑‍⚖️ Qualitative Evaluation (LLM-as-a-Judge, 10 samples, DeepSeek-V3 via Together.ai)

| Criterion   | Avg. Score (out of 5) | Observations |
|-------------|------------------------|--------------|
| Fluency     | 3.9 | Mostly accurate with minor hallucinations |
| Coverage    | 3.6 | Good topical breadth, but often missed fine points |
| Readability | 3.1 | Some summaries well-structured, others awkward |
| Factuality  | 3.6 | Some samples demonstrated excellent accuracy; others showed repetition or placeholders |

---

## 🎨 Visual Evaluation

- Gradio dashboard was used to visualize **ROUGE/ BLEU/ BERTScore** comparisons.  
- Interactive interface allows uploading academic PDFs and scoring summaries via **Together.ai**.  

---

## 🛠 Tech Stack

- 🦙 **LLaMA 3 / Mistral 7B**  
- 🌿 **LoRA (PEFT)**  
- 🔗 **LangGraph & LangChain**  
- ☁️ **Together.ai API**  
- 🐍 Python, Hugging Face, Streamlit  

---

## 📥 Installation

```bash
git clone https://github.com/Farjadkareem/smart-summarizer-LLM-LoRA
cd smart-summarizer
pip install -r requirements.txt

---
## 📌 Future Improvements

✅ Add RAG for improved contextual summaries

✅ Add PDF/Docx input pipeline

✅ Enable exportable structured research reports

✅ Add user feedback loop for continual tuning

---
## 👏 Acknowledgements

Hugging Face

LoRA PEFT

LangGraph

Together.ai

---
## 📜 License

MIT License © Farjad Kareem
