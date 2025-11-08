# Hugging Face Spaces Deployment Guide

Complete guide for deploying the Adzuna MCP Job Assistant to Hugging Face Spaces with free hosting, automatic HTTPS, and no server management required.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Create Your Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Choose a Space name (e.g., `adzuna-job-assistant`)
3. Select **Gradio** as the SDK
4. Choose **Free CPU** hardware (sufficient for this app)
5. Click **Create Space**

### Step 2: Upload Files

Upload these 3 files via **Files** → **Add file** → **Upload files**:

- ✅ `run_adzuna_agent.py`
- ✅ `requirements.txt`
- ✅ `README.md` (use `README_HF_SPACES.md` as template)

### Step 3: Configure Secret

1. Go to **Settings** → **Repository secrets**
2. Add secret: `GOOGLE_API_KEY` = your Google API key
3. Get your key at [Google AI Studio](https://makersuite.google.com/app/apikey)

### Step 4: Deploy

- Watch the **Logs** tab for build progress
- Your app goes live automatically at `https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME`

---

## 📋 Detailed Instructions

### Prerequisites

- Hugging Face account ([sign up here](https://huggingface.co/join))
- Google Generative AI API key ([get one here](https://makersuite.google.com/app/apikey))
- Git installed locally (optional, for Git-based deployment)

---

## 📦 Deployment Methods

### Method 1: Web Upload (Easiest)

Perfect for first-time deployment:

1. **Create Space**: Go to [huggingface.co/new-space](https://huggingface.co/new-space)

   - Name: `adzuna-job-assistant`
   - SDK: **Gradio**
   - Hardware: **Free CPU**
   - Visibility: Public or Private

2. **Upload Files**: Click **Files** → **Add file** → **Upload files**

   - `run_adzuna_agent.py`
   - `requirements.txt`
   - `README.md` (rename from `README_HF_SPACES.md`)

3. **Add Secret**: **Settings** → **Repository secrets** → **New secret**

   - Name: `GOOGLE_API_KEY`
   - Value: Your Google API key

4. **Deploy**: Watch **Logs** tab, app goes live automatically

### Method 2: Git Push (Best for Updates)

Better for version control and ongoing updates:

1. **Create Space** on Hugging Face (same as Method 1)

2. **Clone Space Repository**

   ```powershell
   git clone https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
   cd SPACE_NAME
   ```

3. **Copy Files**

   ```powershell
   Copy-Item ..\adzuna_gradio\run_adzuna_agent.py .
   Copy-Item ..\adzuna_gradio\requirements.txt .
   Copy-Item ..\adzuna_gradio\README_HF_SPACES.md README.md
   ```

4. **Commit and Push**

   ```powershell
   git add .
   git commit -m "Initial deployment"
   git push
   ```

5. **Add Secret**: Via web interface (Settings → Repository secrets)

---

## ⚙️ Configuration

### Required Environment Variable

| Variable         | Description                             | How to Get                                              |
| ---------------- | --------------------------------------- | ------------------------------------------------------- |
| `GOOGLE_API_KEY` | Google Generative AI API key for Gemini | [Get API Key](https://makersuite.google.com/app/apikey) |

### Optional Environment Variable

| Variable                | Description                | Default                                                          |
| ----------------------- | -------------------------- | ---------------------------------------------------------------- |
| `ADZUNA_MCP_SERVER_URL` | Custom Adzuna MCP endpoint | `https://adzuna-mcp-server-236255620233.us-central1.run.app/mcp` |

### Files Required

```
your-space/
├── run_adzuna_agent.py    # Main application
├── requirements.txt        # Python dependencies
└── README.md              # Space documentation
```

---

## 🧪 Testing Your Deployment

Once deployed, test with these queries:

- "Find data analyst jobs in Singapore"
- "Show me software engineer positions"
- "What companies are hiring in Singapore?"
- "Search for marketing executive roles"

---

## 🔧 Troubleshooting

### Build Fails

- Check **Logs** tab for error messages
- Verify `requirements.txt` has valid package versions
- Ensure all files are uploaded correctly

### App Doesn't Start

- Confirm `GOOGLE_API_KEY` is set in Repository secrets
- Check logs for runtime errors
- Verify `run_adzuna_agent.py` calls `launch_app()`

### Slow Performance

- Free CPU tier may be slower for complex queries
- Consider upgrading hardware tier if needed
- API latency depends on Gemini response time

### MCP Connection Issues

- Verify MCP server URL is accessible
- Check if custom `ADZUNA_MCP_SERVER_URL` is correct
- Default endpoint should work out of the box

---

## 🔄 Updating Your Space

### Via Web Interface

Upload new files through **Files** → **Add file** → **Upload files**

### Via Git

```powershell
cd path\to\your-space
git pull
# Make your changes
git add .
git commit -m "Update: description"
git push
```

Hugging Face automatically rebuilds and redeploys on push.

---

## 💰 Hardware Options

| Tier            | Cost | Best For                       |
| --------------- | ---- | ------------------------------ |
| **Free CPU**    | Free | Demos, prototypes, light usage |
| **CPU Upgrade** | Paid | Production, moderate traffic   |
| **GPU**         | Paid | Not needed for this app        |

---

## 📚 Deployment Checklist

### Pre-Deployment

- [ ] Create Hugging Face account
- [ ] Obtain Google API key
- [ ] Test app locally
- [ ] Review `requirements.txt`

### Deployment

- [ ] Create Space on Hugging Face
- [ ] Upload/push required files
- [ ] Configure `GOOGLE_API_KEY` secret
- [ ] Monitor build logs

### Post-Deployment

- [ ] Verify Space is live
- [ ] Test job search functionality
- [ ] Check job result links work
- [ ] Test conversation flow

---

## 📖 Additional Resources

- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Gradio Documentation](https://www.gradio.app/docs)
- [Managing Secrets in Spaces](https://huggingface.co/docs/hub/spaces-overview#managing-secrets)
- [Space README Template](./README_HF_SPACES.md)

---

**Ready to deploy? Start with the [Quick Start](#-quick-start-5-minutes) section above! 🚀**
