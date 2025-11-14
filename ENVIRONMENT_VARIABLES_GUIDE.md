# 🔧 Environment Variables Configuration Guide

This guide explains where and how to set environment variables for SciRAG in different environments.

---

## 📍 Where to Set Environment Variables

### 1. **Local Development** (Your Computer)

**File**: `backend/.env`

**How to set up**:
```bash
# Navigate to backend directory
cd backend

# Copy the example file
cp .env.example .env

# Edit .env with your values
nano .env  # or use your favorite editor
```

**Example `backend/.env`**:
```bash
# For local development - frontend runs on localhost:3000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Optional: Add your API key if you want to test with it
# ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# Other settings use defaults (see .env.example for all options)
```

**Important**:
- ✅ `.env` stays on your computer (in `.gitignore`)
- ❌ Never commit `.env` to GitHub
- ✅ Always commit `.env.example` (template for others)

---

### 2. **Production - Railway** (Backend Deployment)

Railway doesn't use `.env` files. You set variables through their dashboard.

#### **Step-by-Step**:

1. **Go to Railway Dashboard**
   - Visit: https://railway.app/dashboard
   - Click on your SciRAG backend project

2. **Open Variables Tab**
   - Click **"Variables"** in the left sidebar
   - You'll see a list of environment variables

3. **Add ALLOWED_ORIGINS**
   - Click **"+ New Variable"** button
   - **Variable Name**: `ALLOWED_ORIGINS`
   - **Value**: Your Vercel frontend URL

   **Example**:
   ```
   https://scirag.vercel.app
   ```

   **For multiple domains** (production + staging):
   ```
   https://scirag.vercel.app,https://scirag-staging.vercel.app
   ```

4. **Click "Add"**
   - Railway will automatically restart your app with the new variable

5. **Verify It Works**
   - Check deployment logs for errors
   - Test your frontend can access the API

#### **All Variables for Railway**:

Here are the variables you might want to set on Railway:

```bash
# REQUIRED
ALLOWED_ORIGINS=https://your-frontend.vercel.app

# OPTIONAL (users can provide via UI instead)
ANTHROPIC_API_KEY=sk-ant-api03-...

# OPTIONAL (defaults work fine)
MAX_PAPERS=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=all-MiniLM-L6-v2
CLAUDE_MODEL=claude-sonnet-4-20250514
MAX_TOKENS=2000
LOG_LEVEL=INFO
```

#### **Railway Screenshot Guide**:

```
┌─────────────────────────────────────────┐
│  Railway Dashboard                       │
├─────────────────────────────────────────┤
│  > Your Project Name                     │
│    ├─ Settings                          │
│    ├─ Deployments                       │
│    ├─ Metrics                           │
│    └─ Variables  <-- Click here         │
│                                          │
│  Variables                               │
│  ┌─────────────────────────────────┐   │
│  │ + New Variable                   │   │
│  └─────────────────────────────────┘   │
│                                          │
│  Existing Variables:                    │
│  PORT=8000 (Railway sets this)          │
│                                          │
│  Add new:                                │
│  Name:  ALLOWED_ORIGINS                 │
│  Value: https://yourapp.vercel.app      │
│  [ Add ]                                 │
└─────────────────────────────────────────┘
```

---

### 3. **Production - Vercel** (Frontend Deployment)

Your frontend also needs to know the backend URL.

#### **Step-by-Step**:

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Select your SciRAG frontend project

2. **Open Settings**
   - Click **"Settings"** tab
   - Click **"Environment Variables"** in left menu

3. **Add Backend URL**
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: Your Railway backend URL
   - **Environments**: Production, Preview, Development (select all)

   **Example**:
   ```
   https://scirag-backend.railway.app/api
   ```

4. **Redeploy**
   - After adding, trigger a new deployment
   - Go to "Deployments" tab
   - Click "..." → "Redeploy"

---

## 🔍 How to Find Your URLs

### Find Your Vercel Frontend URL:
1. Go to Vercel dashboard
2. Click on your project
3. Look for **"Visit"** button - that's your URL
4. Example: `https://scirag-abc123.vercel.app`

### Find Your Railway Backend URL:
1. Go to Railway dashboard
2. Click on your backend service
3. Click **"Settings"**
4. Scroll to **"Domains"** section
5. You'll see something like: `scirag-backend-production.up.railway.app`
6. Your full API URL: `https://scirag-backend-production.up.railway.app/api`

---

## ✅ Quick Setup Checklist

### For Local Development:
- [ ] Copy `backend/.env.example` to `backend/.env`
- [ ] Set `ALLOWED_ORIGINS=http://localhost:3000`
- [ ] (Optional) Add your `ANTHROPIC_API_KEY`
- [ ] Run `cd backend && uvicorn app.main:app --reload`
- [ ] Run `cd frontend && npm run dev`
- [ ] Test: Frontend at http://localhost:3000 should access backend at http://localhost:8000

### For Production (Railway):
- [ ] Get your Vercel frontend URL
- [ ] Go to Railway Variables settings
- [ ] Add `ALLOWED_ORIGINS=https://your-frontend.vercel.app`
- [ ] (Optional) Add `ANTHROPIC_API_KEY` if providing server key
- [ ] Wait for Railway to redeploy
- [ ] Test: Visit your frontend, try searching papers

### For Production (Vercel):
- [ ] Get your Railway backend URL (with `/api` at the end)
- [ ] Go to Vercel Environment Variables
- [ ] Add `VITE_API_BASE_URL=https://your-backend.railway.app/api`
- [ ] Redeploy from Vercel dashboard
- [ ] Test: Visit your frontend, check browser console for API calls

---

## 🐛 Troubleshooting

### Problem: "CORS error" in browser console

**Symptoms**:
```
Access to fetch at 'https://backend.railway.app/api/search'
from origin 'https://frontend.vercel.app' has been blocked by CORS policy
```

**Solutions**:

1. **Check Railway Variables**
   - Go to Railway → Variables
   - Verify `ALLOWED_ORIGINS` is set correctly
   - Make sure it matches your frontend URL **exactly**
   - ❌ Wrong: `https://frontend.vercel.app/`  (trailing slash)
   - ✅ Right: `https://frontend.vercel.app`

2. **Check for typos**
   - Frontend URL must match exactly
   - Case-sensitive
   - Include `https://` not `http://`

3. **Check Railway logs**
   - Go to Railway → Deployments → View Logs
   - Look for startup message about CORS
   - Should see: `ALLOWED_ORIGINS: ['https://your-frontend.vercel.app']`

### Problem: Frontend can't connect to backend

**Check**:
1. Is `VITE_API_BASE_URL` set in Vercel?
2. Did you redeploy after adding the variable?
3. Check browser console → Network tab
4. Are requests going to the right URL?

### Problem: Railway deployment failed after adding ALLOWED_ORIGINS

**Likely causes**:
1. Syntax error in the value (extra quotes, spaces)
2. Use comma to separate multiple URLs, no spaces:
   - ❌ Wrong: `https://site1.com, https://site2.com`
   - ✅ Right: `https://site1.com,https://site2.com`

---

## 🔐 Security Best Practices

### DO:
✅ Set `ALLOWED_ORIGINS` to specific domains
✅ Use environment variables for all secrets
✅ Different values for dev/staging/production
✅ Keep `.env` files out of version control

### DON'T:
❌ Use `ALLOWED_ORIGINS=*` in production
❌ Commit API keys to GitHub
❌ Share `.env` files publicly
❌ Use production API keys in development

---

## 📚 Reference: All Available Environment Variables

| Variable | Required? | Default | Description |
|----------|-----------|---------|-------------|
| `ALLOWED_ORIGINS` | **YES** (prod) | `http://localhost:3000` | Comma-separated frontend URLs |
| `ANTHROPIC_API_KEY` | No | None | Server-side API key (optional) |
| `MAX_PAPERS` | No | `5` | Max papers per search |
| `CHUNK_SIZE` | No | `1000` | Words per text chunk |
| `CHUNK_OVERLAP` | No | `200` | Overlap between chunks |
| `DOWNLOAD_DIR` | No | `./papers` | PDF storage location |
| `EMBEDDING_MODEL` | No | `all-MiniLM-L6-v2` | Sentence transformer model |
| `CHROMA_PERSIST_DIR` | No | `./chroma_db` | Vector DB location |
| `CLAUDE_MODEL` | No | `claude-sonnet-4-20250514` | Default Claude model |
| `MAX_TOKENS` | No | `2000` | Max tokens for LLM |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity |
| `DEBUG` | No | `false` | Debug mode toggle |

---

## 🆘 Still Having Issues?

1. Check the `SECURITY_AUDIT_SUMMARY.md` for common security issues
2. Review Railway deployment logs
3. Check browser console for errors
4. Verify all URLs are correct (no typos, correct protocols)
5. Make sure you redeployed after adding variables

**Common mistake**: Forgetting to redeploy after adding environment variables!
