# 🚀 Complete Deployment Guide - SciRAG

Deploy your SciRAG system to production in 3 steps!

**Deployment Stack:**
- Frontend → Vercel (Free)
- Backend → Railway (Free $5 credit/month)

**Total Time:** 30-45 minutes

---

## 📋 Prerequisites

Before starting, make sure you have:

- ✅ GitHub account (free)
- ✅ Vercel account (free - sign up at vercel.com)
- ✅ Railway account (free - sign up at railway.app)
- ✅ Your Anthropic API key
- ✅ Git installed on your computer
- ✅ All project files downloaded and working locally

---

## 🎯 Deployment Overview

```
Step 1: Push Code to GitHub
    ↓
Step 2: Deploy Backend to Railway
    ↓
Step 3: Deploy Frontend to Vercel
    ↓
Step 4: Connect & Test
```

---

## 📦 STEP 1: Prepare & Push to GitHub

### 1.1 Initialize Git Repository

Open PowerShell in your project root:

```powershell
cd C:\Users\Administrator\Documents\scirag

# Initialize git
git init

# Create .gitignore in root
New-Item -ItemType File .gitignore
```

### 1.2 Create Root .gitignore

Add this content to `scirag/.gitignore`:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual Environment
backend/venv/
backend/ENV/
backend/env/

# Environment Variables
backend/.env
frontend/.env
frontend/.env.local

# Data & Cache
backend/papers/
backend/chroma_db/

# Node
frontend/node_modules/
frontend/dist/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### 1.3 Create GitHub Repository

1. Go to **https://github.com/new**
2. Repository name: `scirag`
3. Description: "Scientific Research Assistant with RAG"
4. **Keep it Private** (or Public if you want)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click **"Create repository"**

### 1.4 Push Code to GitHub

```powershell
# Add all files
git add .

# Commit
git commit -m "Initial commit - SciRAG full-stack app"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/scirag.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**✅ Checkpoint:** Your code is now on GitHub!

---

## 🚂 STEP 2: Deploy Backend to Railway

### 2.1 Create Railway Account

1. Go to **https://railway.app**
2. Click **"Start a New Project"**
3. Sign up with GitHub (easiest)
4. Verify your account

### 2.2 Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Click **"Configure GitHub App"**
4. Give Railway access to your `scirag` repository
5. Select your **`scirag`** repository

### 2.3 Configure Backend Service

Railway will detect it's a Python app automatically.

1. Click on your service (it will auto-deploy)
2. Go to **"Settings"** tab
3. **Root Directory:** Set to `backend`
4. **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2.4 Add Environment Variables

1. Click **"Variables"** tab
2. Click **"+ New Variable"**
3. Add these variables:

```
ANTHROPIC_API_KEY=sk-ant-api03-YOUR-KEY-HERE
MAX_PAPERS=5
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=all-MiniLM-L6-v2
CLAUDE_MODEL=claude-sonnet-4-20250514
MAX_TOKENS=2000
```

**⚠️ CRITICAL:** Add your actual Anthropic API key!

### 2.5 Deploy Backend

1. Railway will automatically deploy
2. Wait 2-3 minutes for build to complete
3. You'll see: ✅ "Deployed successfully"

### 2.6 Get Backend URL

1. Go to **"Settings"** tab
2. Scroll to **"Networking"** section
3. Click **"Generate Domain"**
4. Copy your backend URL (looks like: `https://scirag-production.up.railway.app`)

**✅ Checkpoint:** Backend is live!

### 2.7 Test Backend

Visit: `https://YOUR-BACKEND-URL.up.railway.app/health`

You should see:
```json
{"status": "healthy"}
```

Also check docs: `https://YOUR-BACKEND-URL.up.railway.app/docs`

---

## 🎨 STEP 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Account

1. Go to **https://vercel.com**
2. Click **"Sign Up"**
3. Sign up with GitHub (easiest)

### 3.2 Import Project

1. Click **"Add New..."** → **"Project"**
2. Click **"Import"** next to your `scirag` repository
3. If you don't see it, click **"Import Third-Party Git Repository"**

### 3.3 Configure Project

**Framework Preset:** Vite  
**Root Directory:** `frontend`  
**Build Command:** `npm run build`  
**Output Directory:** `dist`

### 3.4 Add Environment Variable

Before deploying, click **"Environment Variables"**:

1. **Key:** `VITE_API_BASE_URL`
2. **Value:** `https://YOUR-RAILWAY-URL.up.railway.app/api`
   
   (Replace with your Railway backend URL + `/api`)

3. Check **all** environments (Production, Preview, Development)

### 3.5 Deploy Frontend

1. Click **"Deploy"**
2. Wait 1-2 minutes
3. You'll see: ✅ "Deployment Ready"

### 3.6 Get Frontend URL

Vercel will give you a URL like:
`https://scirag.vercel.app`

**✅ Checkpoint:** Frontend is live!

---

## 🔗 STEP 4: Connect & Test

### 4.1 Update Backend CORS (if needed)

If you get CORS errors, update `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://scirag.vercel.app",  # Your Vercel URL
        "https://*.vercel.app",        # All Vercel preview URLs
        "http://localhost:3000",       # Local development
        "*"                            # Or allow all (less secure)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then push to GitHub:
```powershell
git add .
git commit -m "Update CORS for production"
git push
```

Railway will auto-redeploy.

### 4.2 Test Complete System

1. Go to your Vercel URL: `https://scirag.vercel.app`
2. Try searching: "neural networks"
3. Process papers
4. Ask a question: "What are neural networks?"
5. Verify everything works!

---

## 🎉 SUCCESS! Your App is Live!

### Your URLs

- **Frontend:** `https://scirag.vercel.app`
- **Backend:** `https://scirag-production.up.railway.app`
- **API Docs:** `https://YOUR-BACKEND-URL.up.railway.app/docs`

### Share Your App

You can now share your frontend URL with anyone!

---

## 💰 Cost Breakdown

**Vercel (Frontend):**
- Free tier: Unlimited
- Bandwidth: 100GB/month
- Cost: **$0** ✅

**Railway (Backend):**
- Free tier: $5 credit/month
- Enough for ~500 requests/month
- Cost: **$0** (stays in free tier) ✅

**Anthropic API:**
- Pay per token
- ~$0.003 per 1000 tokens
- Estimated: $1-5/month for normal use

**Total Cost:** ~$1-5/month (just Anthropic API)

---

## 🔧 Maintenance & Updates

### Update Backend

```powershell
# Make changes locally
# Test locally
# Push to GitHub
git add .
git commit -m "Update: description"
git push
```

Railway will auto-deploy in ~2 minutes.

### Update Frontend

```powershell
# Make changes locally
# Test locally: npm run dev
# Push to GitHub
git add .
git commit -m "Update: description"
git push
```

Vercel will auto-deploy in ~1 minute.

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** Backend fails to build
- Check Railway logs
- Verify `requirements.txt` is correct
- Check Python version (3.10)

**Problem:** Backend crashes
- Check environment variables are set
- Verify ANTHROPIC_API_KEY is correct
- Check Railway logs for errors

**Problem:** Papers not persisting
- Railway free tier has ephemeral storage
- Upgrade to Pro ($5/month) for persistent volumes
- Or use external storage (S3)

### Frontend Issues

**Problem:** Can't connect to backend
- Verify `VITE_API_BASE_URL` is correct
- Check backend CORS settings
- Verify backend is running (visit /health)

**Problem:** Environment variable not working
- Make sure it starts with `VITE_`
- Redeploy after adding variables
- Check Vercel environment settings

### CORS Errors

If you see CORS errors in browser console:

1. Update `backend/app/main.py` CORS settings
2. Add your Vercel URL to `allow_origins`
3. Push to GitHub
4. Wait for Railway to redeploy

---

## 📊 Monitoring

### Railway (Backend)

- **Metrics:** View CPU, Memory, Network usage
- **Logs:** Real-time logs of all requests
- **Deployments:** History of all deployments

### Vercel (Frontend)

- **Analytics:** Page views, performance
- **Deployment Logs:** Build and deploy logs
- **Preview URLs:** Each PR gets a preview URL

---

## 🚀 Next Steps

Now that you're deployed:

1. **Custom Domain** (Optional)
   - Buy domain (Namecheap, GoDaddy)
   - Connect to Vercel
   - Add SSL (automatic with Vercel)

2. **Add Authentication**
   - Clerk.com (easiest)
   - Auth0
   - Custom JWT

3. **Database** (for saving conversations)
   - Railway PostgreSQL
   - Supabase
   - MongoDB Atlas

4. **Monitoring**
   - Sentry (error tracking)
   - LogRocket (session replay)
   - PostHog (analytics)

---

## 📝 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] Backend deployed to Railway
- [ ] Environment variables added to Railway
- [ ] Backend health check works
- [ ] Backend API docs accessible
- [ ] Vercel project created
- [ ] Frontend deployed to Vercel
- [ ] Environment variable added to Vercel
- [ ] Frontend loads successfully
- [ ] Can search papers
- [ ] Can process papers
- [ ] Can ask questions
- [ ] Shared URL with someone

---

## 🎉 Congratulations!

You've successfully deployed a full-stack AI application to production!

**What you accomplished:**
- ✅ Backend API on Railway
- ✅ Frontend on Vercel
- ✅ Automatic deployments from GitHub
- ✅ Environment variables configured
- ✅ CORS properly set up
- ✅ Live, shareable URL
- ✅ Professional deployment pipeline

**Share your creation!** 🚀

---

## 📞 Need Help?

**Common Resources:**
- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- GitHub Docs: https://docs.github.com

**Check Status:**
- Railway Status: https://status.railway.app
- Vercel Status: https://www.vercel-status.com

---

**Deployment Guide v1.0**  
**Last Updated:** Phase 3 Complete