# Quick Start Guide - Chat with Your Notes

## ⚡ 5-Minute Setup

### Windows Users

1. **Double-click `setup.bat`**
   ```
   This will:
   - Create virtual environment
   - Install all dependencies
   - Create uploads folder
   - Create .env file
   ```

2. **Edit `.env` file**
   ```
   OPENAI_API_KEY=sk-...your-key-here...
   ```

3. **Run the app**
   ```
   streamlit run app/app.py
   ```

4. **Access in browser**
   ```
   http://localhost:8501
   ```

---

## 🍎 macOS/Linux Users

```bash
# 1. Navigate to project
cd rag-notes-app

# 2. Run setup
python setup.py

# 3. Activate environment
source venv/bin/activate

# 4. Edit .env with your API key
nano .env

# 5. Run app
streamlit run app/app.py
```

---

## 🚀 First Run Checklist

- [ ] Created virtual environment
- [ ] Installed requirements.txt
- [ ] Added OpenAI API key to .env
- [ ] Created uploads folder
- [ ] Can run `streamlit run app/app.py` without errors
- [ ] Browser opens to http://localhost:8501

---

## 📚 First Usage

1. **Enter API Key** (or it's already in .env)
2. **Upload a PDF** - Try with a textbook or notes
3. **Wait for processing** - See "Reading PDF..." indicator
4. **Ask a question** - Try: "Summarize the introduction"
5. **See citations** - Click "Sources" to verify answers

---

## ❓ Troubleshooting Quick Answers

**"Python not found"**
→ Install Python 3.8+ from https://www.python.org/

**"Invalid API key"**
→ Check key is correct at https://platform.openai.com/api-keys

**"PDF won't upload"**
→ Ensure it's a text-based PDF (not scanned images)

**"Slow first query"**
→ Normal! ChromaDB initialization takes time

**"ModuleNotFoundError"**
→ Run `pip install -r requirements.txt` again

---

## 💡 Pro Tips

- Use the temperature slider (0.3 = precise, 0.8 = creative)
- Upload multiple PDFs and ask cross-file questions
- Clear chat without clearing documents
- Copy-paste answers for citations
- Works best with 5-50 page documents

---

## 📖 Need More Help?

- **Setup Issues**: See README.md
- **Development**: See DEVELOPMENT.md
- **Architecture**: See DEVELOPMENT.md#Architecture
- **API Questions**: https://platform.openai.com/docs

---

**Ready? Let's go! 🚀**
