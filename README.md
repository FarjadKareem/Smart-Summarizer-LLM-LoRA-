# 🤖 Autonomous AI Agent System

An AI-powered conversational agent that answers employee-related queries from a structured dataset and seamlessly falls back to **web search** when the dataset lacks information. Built with **LangChain**, **Google Gemini**, and **Tavily Search API**, this system supports **multi-turn, context-aware conversations** with memory.

---

## 🚀 Features

- 📊 Query structured employee dataset (salary, role counts, highest/lowest paid employees, etc.)
- 🌐 Web search fallback via **Tavily API**
- 🧠 Conversational memory with LangChain’s **ConversationBufferMemory**
- ⚡ Reasoning powered by **Google Gemini (Gemini-2.5-pro)**
- 🔌 Extensible tool-based architecture for adding new capabilities

---

## 🧠 How It Works

1. **Dataset Lookup:** Uses Pandas to query structured employee data  
2. **LLM Reasoning:** Google Gemini generates natural responses  
3. **Memory:** Conversation history maintained with LangChain memory  
4. **Web Search:** Tavily API provides real-time fallback information  
5. **Agent Orchestration:** LangChain coordinates tools + LLM for smooth interaction  

---

## ⚙️ Tech Stack

- 🧠 [LangChain](https://www.langchain.com/) – Agent orchestration  
- 🔮 [Google Gemini](https://deepmind.google/technologies/gemini/) – LLM reasoning  
- 🌐 [Tavily Search](https://tavily.com/) – Web search integration  
- 🐼 [Pandas](https://pandas.pydata.org/) – Dataset queries  
- 🐍 Python  

---
## Example Queries

How many Data Scientists do we have?

What is the average salary of a Software Engineer?

Who is the highest paid employee?

What is the lowest salary in the company?

Give me today’s latest AI news.

👉 Type exit to quit the program.

## 🙌 Acknowledgements

LangChain

Google Gemini

Tavily Search

Pandas
