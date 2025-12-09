# Deploying Tangled to a Custom .es Domain

## Option 1: Streamlit Cloud + Custom Domain (Easiest)

**Cost:** ~€10-15/year for .es domain  
**Time:** 1-2 hours

### Steps:

1. **Buy a .es domain**
   - Go to Spanish registrar: https://www.arsys.es/ or https://www.nominalia.com/
   - Search for your desired name (e.g., `tangled.es`, `crochetplanner.es`)
   - Purchase domain (~€10-15/year)

2. **Keep Streamlit Cloud hosting** (free)
   - Your app is already on: `https://annaarrodriguez44-tangled.streamlit.app`

3. **Point domain to Streamlit**
   - In your domain registrar DNS settings:
   - Add CNAME record: `www` → `annaarrodriguez44-tangled.streamlit.app`
   - Add URL redirect: `tangled.es` → `www.tangled.es`

4. **Configure in Streamlit Cloud**
   - Go to app settings → Custom domains
   - Add your domain: `www.tangled.es`
   - Follow verification steps

**Result:** Your app accessible at `www.tangled.es`

---

## Option 2: Full Custom Hosting (More Control)

**Cost:** €5-20/month  
**Time:** 3-5 hours

### A. Heroku + Custom Domain

1. **Deploy to Heroku**
   ```bash
   # Install Heroku CLI
   # Login
   heroku login
   
   # Create app
   heroku create tangled-crochet
   
   # Add buildpack for Python
   heroku buildpacks:set heroku/python
   
   # Deploy
   git push heroku main
   ```

2. **Add custom domain**
   ```bash
   heroku domains:add www.tangled.es
   ```

3. **Configure DNS** (in domain registrar)
   - CNAME: `www` → `[heroku-dns-target]`

**Cost:** Free tier available, ~€7/month for hobby

### B. DigitalOcean App Platform

1. **Create DigitalOcean account**: https://www.digitalocean.com
2. **Connect GitHub repo**
3. **Configure app:**
   - Runtime: Python
   - Run command: `streamlit run Home.py --server.port=8080`
4. **Add domain** in settings
5. **Update DNS** in registrar

**Cost:** $5/month (~€4.50)

### C. Railway.app

1. **Go to**: https://railway.app
2. **Deploy from GitHub**
3. **Add domain** in project settings
4. **Configure DNS**

**Cost:** $5/month with free credits

### D. Render.com

1. **Sign up**: https://render.com
2. **New Web Service** from GitHub
3. **Set start command:** `streamlit run Home.py --server.port=$PORT`
4. **Add custom domain**

**Cost:** Free tier available, paid from $7/month

---

## Option 3: Professional Setup (Best Performance)

**Cost:** €10-30/month  
**Time:** 1 day

### Use Google Cloud Run + Cloud CDN

1. **Containerize app** (Dockerfile)
2. **Deploy to Cloud Run**
3. **Add Cloud CDN** for Spain
4. **Configure domain**

---

## Recommended Approach for You

### **Best: Streamlit Cloud + .es Domain**

**Why:**
- Already deployed on Streamlit Cloud
- Free hosting
- Automatic updates from GitHub
- Just need to buy domain and configure DNS
- No code changes needed

**Steps:**

1. **Buy domain** (~15 min)
   - Go to https://www.arsys.es
   - Search for name: `tangled.es`, `mispatrones.es`, `crochetplanner.es`
   - Purchase

2. **Configure DNS** (~5 min)
   - In Arsys DNS panel:
   - Type: CNAME
   - Name: `www`
   - Value: `annaarrodriguez44-tangled.streamlit.app`
   - TTL: 3600

3. **Add to Streamlit** (~10 min)
   - Go to https://share.streamlit.io
   - Open your Tangled app
   - Settings → Custom domains
   - Add: `www.tangled.es`
   - Verify ownership (add TXT record if needed)

4. **Wait for propagation** (1-48 hours)
   - DNS changes take time
   - Check status: https://dnschecker.org

---

## Domain Name Ideas

### Available to check:
- `tangled.es`
- `mispatrones.es` (my patterns)
- `crochetplanner.es`
- `patronesganchillo.es` (crochet patterns)
- `lanaypunto.es` (yarn and stitch)
- `tejidocroche.es`
- `hilosypatrones.es` (threads and patterns)

---

## Files Needed for Custom Hosting

If you choose Heroku/Railway/Render, you'll need:

### `Procfile` (for Heroku)
```
web: streamlit run Home.py --server.port=$PORT --server.address=0.0.0.0
```

### `runtime.txt` (specify Python version)
```
python-3.11.0
```

### `requirements.txt` (already have this)

---

## Next Steps

1. **Decide on domain name** - Check availability at arsys.es
2. **Choose hosting option** - Recommend staying with Streamlit Cloud
3. **Purchase domain** 
4. **I'll help configure DNS** once you have the domain

**Ready to buy a domain?** Let me know which name you like!
