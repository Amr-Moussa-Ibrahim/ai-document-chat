# 🤖 AI Document Chat — Chat With Your PDFs & Notes (100% Free)

An **advanced AI project** you can run on your own laptop and upload to GitHub.
Upload a PDF or text file, then ask questions about it in plain English — and get
answers written by a real AI model, with the exact passages it used as proof.

> **Everything is 100% free and open-source. No API keys. No paid accounts. No
> internet needed after the first run.** It works on a normal CPU (no GPU
> required).

This project uses the same technique (**RAG — Retrieval-Augmented Generation**)
that powers modern tools like ChatGPT's "chat with your files", enterprise
search assistants, and customer-support bots. It's a fantastic portfolio piece.

---

## 📸 What it looks like

A clean web page where you:
1. Upload a document in the sidebar.
2. Type a question in the chat box.
3. Get an AI answer **plus** the source passages it based the answer on.

---

## 🧠 What is RAG? (explained super simply)

Imagine an open-book exam. Instead of memorizing an entire textbook, you:
1. **Find** the right page for the question (this is *Retrieval*).
2. **Read** that page and **write** an answer in your own words (this is
   *Generation*).

That's exactly what this app does:

| Step | What happens | File that does it |
|------|--------------|-------------------|
| 1️⃣ **Split** | Your document is cut into small chunks | `src/document_loader.py` |
| 2️⃣ **Embed** | Each chunk becomes numbers that capture its *meaning* | `src/embeddings.py` |
| 3️⃣ **Store & Search** | Chunks are stored so we can find the most relevant ones fast | `src/vector_store.py` |
| 4️⃣ **Answer** | The AI reads the top chunks and writes an answer | `src/chatbot.py` |
| 🖥️ **UI** | The web page you click on | `app.py` |

Because the AI only answers from *your* document, it rarely makes things up.

---

## 🛠️ The free tools used (and why)

| Tool | What it does | Cost |
|------|--------------|------|
| **sentence-transformers** (`all-MiniLM-L6-v2`) | Understands the *meaning* of text | Free |
| **FAISS** | Lightning-fast search over meanings | Free |
| **Transformers** (`google/flan-t5-base`) | Writes the answers | Free |
| **Streamlit** | Turns Python into a web app | Free |
| **pypdf** | Reads text out of PDFs | Free |

The AI models download automatically the first time you run the app (a few
hundred MB total) and are then cached, so future runs work fully offline.

---

## 🚀 Get started in 5 minutes

You need **Python 3.9 or newer** installed. Then:

```bash
# 1. Get the code
git clone https://github.com/YOUR-USERNAME/ai-document-chat.git
cd ai-document-chat

# 2. (Recommended) create a clean virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install the free dependencies
pip install -r requirements.txt

# 4. Run the web app!
streamlit run app.py
```

Your browser opens automatically at `http://localhost:8501`.
Upload the included `sample_data/sample.txt`, click **Add to knowledge base**,
then ask things like *"Which planet is the hottest and why?"*

### Prefer the terminal instead of a web page?

```bash
python cli_demo.py sample_data/sample.txt
```

---

## 📂 Project structure

```
ai-document-chat/
├── app.py                 # The Streamlit web interface
├── cli_demo.py            # A simple command-line version
├── requirements.txt       # The free libraries to install
├── README.md              # This file
├── LICENSE                # MIT license (free to use)
├── .gitignore             # Files Git should ignore
├── sample_data/
│   └── sample.txt         # A demo document about the Solar System
└── src/                   # The "brain" of the app
    ├── __init__.py
    ├── document_loader.py # Step 1: read & chunk documents
    ├── embeddings.py      # Step 2: text -> meaning (embeddings)
    ├── vector_store.py    # Step 3: store & search meanings (FAISS)
    └── chatbot.py         # Step 4: RAG — tie it all together
```

Every file is heavily commented in plain English, so you can read it top to
bottom and understand exactly what each line does.

---

## ☁️ Upload it to GitHub (step by step)

1. Create a free account at [github.com](https://github.com).
2. Click **New repository**, name it `ai-document-chat`, keep it **Public**,
   and click **Create repository**.
3. In your terminal, inside the project folder, run:

```bash
git init
git add .
git commit -m "Initial commit: AI Document Chat (free RAG app)"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ai-document-chat.git
git push -u origin main
```

Done — your advanced AI project is now on GitHub! 🎉

> Tip: the `.gitignore` file already stops big model files and your virtual
> environment from being uploaded, keeping your repo clean and small.

---

## 🌐 Put it online for free (optional)

Want a public link anyone can try? Deploy free on **Streamlit Community Cloud**:
1. Push the project to GitHub (see above).
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Click **New app**, pick your repo, set the main file to `app.py`, and deploy.

You'll get a shareable `https://...streamlit.app` URL — still 100% free.

---

## 💡 Ideas to make it your own (great for standing out)

- 🌍 Add support for more file types (Word `.docx`, web pages, CSVs).
- 🗣️ Add a "sources highlighting" view or voice input.
- 🧩 Swap in a bigger model like `google/flan-t5-large` for smarter answers.
- 💾 Save the vector store to disk so documents stay indexed between runs.
- 🎨 Customize the colors and title in `app.py`.

---

## ❓ Troubleshooting

- **First run is slow / seems stuck:** it's downloading the AI models once. Give
  it a couple of minutes. After that it's fast and offline.
- **`pip install` fails on `faiss-cpu`:** make sure you're on Python 3.9–3.12
  and have an up-to-date `pip` (`python -m pip install --upgrade pip`).
- **Out of memory on a small machine:** use a smaller model by changing
  `google/flan-t5-base` to `google/flan-t5-small` in `src/chatbot.py`.

---

## 📜 License

MIT — free to use, modify, and share. See the [LICENSE](LICENSE) file.

Made with ❤️ and open-source AI.
