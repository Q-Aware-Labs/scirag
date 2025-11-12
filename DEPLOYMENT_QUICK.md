# ⚡ Quick Deployment Commands

## 🔥 Fast Deploy (Already configured? Use this!)

### Push to GitHub
```powershell
git add .
git commit -m "Deploy to production"
git push
```

**That's it!** Railway and Vercel auto-deploy from GitHub.

---

## 🆕 First Time Setup

### 1. GitHub Setup
```powershell
cd C:\Users\Administrator\Documents\scirag
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/scirag.git
git branch -M main
git push -u origin main
```

### 2. Railway Backend
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select `scirag` repo
4. Settings → Root Directory: `backend`
5. Variables → Add:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```
6. Settings → Generate Domain
7. Copy URL: `https://YOUR-APP.up.railway.app`

### 3. Vercel Frontend
1. Go to https://vercel.com
2. Import Project → Select `scirag`
3. Framework: Vite
4. Root Directory: `frontend`
5. Environment Variables:
   ```
   VITE_API_BASE_URL=https://YOUR-RAILWAY-URL.up.railway.app/api
   ```
6. Deploy!

---

## 🔄 Update Deployment

### Backend Changes
```powershell
cd backend
# Make changes
git add .
git commit -m "Update backend"
git push
# Railway auto-deploys in ~2 minutes
```

### Frontend Changes
```powershell
cd frontend
# Make changes
git add .
git commit -m "Update frontend"
git push
# Vercel auto-deploys in ~1 minute
```

---

## 🧪 Test Deployments

### Backend
```powershell
# Health check
curl https://YOUR-APP.up.railway.app/health

# API docs
# Visit: https://YOUR-APP.up.railway.app/docs
```

### Frontend
```
# Visit: https://YOUR-APP.vercel.app
```

---

## 🐛 Quick Fixes

### CORS Error
Update `backend/app/main.py`:
```python
allow_origins=["https://YOUR-APP.vercel.app", "*"]
```
Then: `git push`

### Environment Variable
**Railway:** Variables tab → Add/Edit → Redeploy
**Vercel:** Settings → Environment Variables → Add → Redeploy

### Force Redeploy
**Railway:** Deployments → ⋯ → Redeploy
**Vercel:** Deployments → ⋯ → Redeploy

---

## 📊 Check Status

### Logs
**Railway:** Deployments tab → View Logs
**Vercel:** Deployments tab → View Function Logs

### Metrics
**Railway:** Metrics tab
**Vercel:** Analytics tab

---

## 💰 Cost

- **Vercel:** Free ✅
- **Railway:** $5 credit/month (free) ✅
- **Total:** $0/month ✅

---

## 🎯 Your URLs

Frontend: `https://YOUR-APP.vercel.app`
Backend: `https://YOUR-APP.up.railway.app`
API Docs: `https://YOUR-APP.up.railway.app/docs`

**Save these!** 🔖