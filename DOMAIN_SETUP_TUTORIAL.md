# Complete Tutorial: Setting Up tangled.es Domain

## Step-by-Step Guide for Your Crochet Pattern App

---

## Part 1: Purchase the Domain (15 minutes)

### 1.1 Go to arsys.es
- Open browser: https://www.arsys.es/
- This is one of Spain's most popular domain registrars

### 1.2 Search for Your Domain
1. In the search box on homepage, type: **tangled.es**
2. Click "Buscar" (Search)
3. You'll see if it's available (should show green checkmark ✓)

### 1.3 Add to Cart
1. Click "Añadir al carrito" (Add to cart)
2. **Important**: Uncheck extra services you don't need:
   - Email hosting (you don't need this)
   - Website builder (you already have one!)
   - SSL certificate (Streamlit provides this free)
3. Keep only: **Domain registration for 1 year**

### 1.4 Complete Purchase
1. Click "Tramitar pedido" (Checkout)
2. Create account or log in
3. Fill in your details:
   - Name, email, address
   - Payment method (credit card)
4. **Expected cost: €10-15/year**
5. Complete payment

### 1.5 Verify Ownership
- Check your email for confirmation
- Click verification link if required
- Log into arsys.es panel: https://panel.arsys.es/

---

## Part 2: Configure DNS Records (20 minutes)

DNS = Domain Name System. It tells the internet where to find your website.

### 2.1 Access DNS Management
1. Log into https://panel.arsys.es/
2. Click on **"Mis dominios"** (My domains)
3. Find **tangled.es** in the list
4. Click on it → **"Gestionar DNS"** or **"Zona DNS"** (DNS Zone)

### 2.2 Add CNAME Record for www subdomain

**What is CNAME?** It's a redirect that says "www.tangled.es points to this other address"

**Steps:**
1. Click **"Añadir registro"** (Add record)
2. Fill in:
   - **Type**: CNAME
   - **Name/Host**: `www`
   - **Value/Target**: `annaarrodriguez44-tangled.streamlit.app`
   - **TTL**: 3600 (or leave default)
3. Click **"Guardar"** (Save)

**What this does:** When someone types `www.tangled.es`, it points to your Streamlit app

### 2.3 Handle Root Domain (tangled.es without www)

**Option A - CNAME for root (if allowed):**
1. Add another CNAME record:
   - **Name/Host**: `@` (this means root domain)
   - **Value**: `annaarrodriguez44-tangled.streamlit.app`
   - **TTL**: 3600

**Option B - URL Redirect (if CNAME not allowed for root):**
1. Look for **"Redirecciones"** or **"URL Redirect"**
2. Create redirect:
   - **From**: `tangled.es`
   - **To**: `www.tangled.es`
   - **Type**: 301 (permanent)

**What this does:** Ensures `tangled.es` and `www.tangled.es` both work

### 2.4 Verify DNS Records
After saving, check your records. You should see:
```
Type    Name    Value
CNAME   www     annaarrodriguez44-tangled.streamlit.app
CNAME   @       annaarrodriguez44-tangled.streamlit.app
```

**Important:** DNS changes take 1-48 hours to propagate worldwide (usually 1-4 hours)

---

## Part 3: Connect to Streamlit Cloud (15 minutes)

### 3.1 Access Your App Settings
1. Go to https://share.streamlit.io/
2. Sign in with GitHub (annaarrodriguez44)
3. Find your **Tangled** app
4. Click **⋮** (three dots) → **Settings**

### 3.2 Add Custom Domain
1. Look for **"Custom domains"** section (might be under "Advanced")
2. Click **"Add domain"**
3. Enter: `tangled.es`
4. Click **"Add"**
5. Repeat for: `www.tangled.es`

### 3.3 Verify Domain Ownership
Streamlit will ask you to verify you own the domain. Two methods:

**Method 1 - DNS TXT Record (most common):**
1. Streamlit shows you a TXT record like:
   ```
   _streamlit-verify.tangled.es  TXT  "abc123xyz456"
   ```
2. Go back to arsys.es DNS panel
3. Add new record:
   - **Type**: TXT
   - **Name**: `_streamlit-verify` (or full name shown)
   - **Value**: The code Streamlit gave you (with quotes)
4. Save
5. Wait 5-10 minutes
6. Go back to Streamlit, click **"Verify"**

**Method 2 - Upload HTML File (alternative):**
1. Streamlit might ask you to upload a file to your site
2. This doesn't apply to Streamlit Cloud, use Method 1

### 3.4 Wait for SSL Certificate
- Streamlit automatically generates SSL certificate (https://)
- This takes 5-15 minutes after verification
- You'll get email when ready

---

## Part 4: Test Your Domain (10 minutes)

### 4.1 Check DNS Propagation
1. Go to https://dnschecker.org/
2. Enter: `tangled.es`
3. Select record type: **CNAME**
4. Click **"Search"**
5. You should see your Streamlit URL appearing worldwide

**If some locations show old data:** This is normal, wait 1-2 hours

### 4.2 Test Your Website
Try these URLs in your browser:
- http://tangled.es → Should redirect to https://tangled.es
- https://tangled.es → Should load your app
- http://www.tangled.es → Should work
- https://www.tangled.es → Should work

**All should show your beautiful homepage with the 🧶 Tangled hero section!**

### 4.3 Mobile Test
- Open on your phone
- Check it loads correctly
- Test navigation between pages

---

## Part 5: Troubleshooting

### Problem: "This site can't be reached"
**Solution:** DNS not propagated yet
- Wait 1-4 hours
- Check dnschecker.org
- Clear browser cache (Ctrl+Shift+Del)

### Problem: "Not Secure" warning
**Solution:** SSL not ready yet
- Wait 15-30 minutes after verification
- Try https:// instead of http://
- Contact Streamlit support if persists

### Problem: Shows old version of app
**Solution:** Clear cache
- Browser: Ctrl+Shift+R (hard refresh)
- Or: Ctrl+Shift+Del → Clear cached files

### Problem: Domain verification fails
**Solution:** Check TXT record
- Go to https://mxtoolbox.com/TXTLookup.aspx
- Enter: `_streamlit-verify.tangled.es`
- If not found, wait longer or re-add record

### Problem: 404 Error
**Solution:** Wrong CNAME target
- Double-check: `annaarrodriguez44-tangled.streamlit.app`
- No http://, no https://, no trailing /
- Just the domain name

---

## Part 6: Optional Enhancements

### 6.1 Email Forwarding (Optional)
If you want hello@tangled.es:
1. In arsys.es panel → Email
2. Set up forwarding to your Gmail
3. Cost: Usually €2-5/year

### 6.2 Analytics (Recommended)
Track visitors:
1. Sign up: https://analytics.google.com/
2. Add property: tangled.es
3. Get tracking code
4. Add to Streamlit app (in Home.py `st.html()`)

### 6.3 Social Media Integration
Update your links:
- Share `https://tangled.es` instead of long Streamlit URL
- Create QR code pointing to tangled.es
- Add to Instagram/Facebook bio

---

## Quick Reference Card

### Your DNS Records (arsys.es):
```
Type    Name    Target
CNAME   www     annaarrodriguez44-tangled.streamlit.app
CNAME   @       annaarrodriguez44-tangled.streamlit.app
TXT     _streamlit-verify   "your-verification-code"
```

### Your Streamlit Settings:
- Custom domains: tangled.es, www.tangled.es
- Main file: Home.py
- Branch: main
- Repository: annaarrodriguez44/Tangled

### Useful Links:
- arsys.es panel: https://panel.arsys.es/
- Streamlit dashboard: https://share.streamlit.io/
- DNS checker: https://dnschecker.org/
- SSL checker: https://www.ssllabs.com/ssltest/

---

## Timeline Expectations

| Step | Time to Complete | Time to Take Effect |
|------|-----------------|---------------------|
| Purchase domain | 15 min | Immediate |
| Add DNS records | 10 min | 1-4 hours |
| Connect to Streamlit | 10 min | 5-15 min |
| SSL certificate | Automatic | 15-30 min |
| Full propagation | - | 1-48 hours |

**Realistic total time: 4-6 hours from purchase to fully working**

Most of this is waiting time - you can do other things!

---

## Cost Breakdown

| Item | Cost | Frequency |
|------|------|-----------|
| tangled.es domain | €10-15 | Per year |
| DNS hosting | Included | - |
| SSL certificate | Free (Streamlit) | - |
| Streamlit hosting | Free | - |
| **TOTAL** | **€10-15/year** | - |

---

## Next Steps After Domain Works

1. **Update your README.md** with new URL
2. **Share on social media**: "Check out my new app at tangled.es!"
3. **Add to portfolio/CV**: Professional domain shows credibility
4. **Monitor usage**: Check Streamlit analytics
5. **Gather feedback**: Share with crochet communities
6. **Plan improvements**: Based on user feedback

---

## Support Contacts

**If you get stuck:**
- arsys.es support: https://www.arsys.es/ayuda (Spanish support)
- Streamlit forum: https://discuss.streamlit.io/
- Streamlit docs: https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/custom-domains

---

**Good luck! Your professional crochet pattern app will soon be live at tangled.es! 🧶✨**
