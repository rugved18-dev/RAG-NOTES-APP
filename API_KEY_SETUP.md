# 🔑 API Key Configuration Guide

## Quick Setup (2 minutes)

### Option 1: Add API Key in the App (Easiest)
1. Run the app: `streamlit run app/app.py`
2. In the sidebar under "🔑 API Configuration", paste your API key
3. Click Enter - it will validate instantly
4. Start uploading documents!

### Option 2: Add API Key to `.env` File
1. Open `.env` file in your project root
2. Replace the empty line with your key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
3. Save the file
4. Restart the app

---

## How to Get an OpenAI API Key

### Step-by-Step:
1. Go to https://platform.openai.com/api-keys
2. Sign in with your OpenAI account (create one if needed)
3. Click **"Create new secret key"**
4. Copy the key immediately (you can't see it again!)
5. Paste it into the app sidebar or `.env` file

### What You'll See:
```
sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Important Security Notes

🔒 **NEVER:**
- Share your API key publicly
- Commit it to GitHub (we have `.gitignore` to prevent this)
- Paste it in messages or forums
- Use it in client-side code

✅ **DO:**
- Keep it in `.env` file (which is in `.gitignore`)
- Or use the app sidebar input (not stored anywhere)
- Rotate it regularly
- Use API key restrictions (tier 3 limited access)

---

## Troubleshooting

### ❌ "Invalid API Key"
- Check you copied the full key from OpenAI dashboard
- No extra spaces before/after
- Make sure it starts with `sk-`

### ❌ "API Key not found"
- If using `.env`: Make sure `OPENAI_API_KEY=sk-...` (with your actual key)
- If using app sidebar: Paste the key and it should show ✅ confirmation
- Restart the app after editing `.env`

### ❌ "Quota exceeded"
- You've used all your free trial credits
- Upgrade to a paid account at https://platform.openai.com/account/billing

### ❌ "Rate limit exceeded"
- Wait a moment and try again
- Reduce the number of simultaneous requests
- Consider upgrading your OpenAI plan

---

## Cost Information

### Typical Usage Costs:
- **Embeddings**: ~$0.0001 per 1,000 tokens
- **Chat (GPT-3.5-Turbo)**: ~$0.0005 per 1,000 tokens
- **Estimate**: ~$0.01 per conversation turn

### Examples:
- 100 conversations/day = ~$1/month
- 1,000 conversations/day = ~$10/month

Check your usage at: https://platform.openai.com/account/usage

---

## Alternative: Use Ollama (Free, Local AI)

If you don't want to pay for OpenAI:

1. Install Ollama from https://ollama.ai
2. Run `ollama serve` in another terminal
3. The app will auto-detect it
4. No API key needed!
5. Runs completely offline

---

## Support

- OpenAI API Docs: https://platform.openai.com/docs
- Troubleshoot API: https://help.openai.com
- Status Page: https://status.openai.com
