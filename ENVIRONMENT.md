# Crochet Pattern RAG - Environment Setup

## Conda Environment Details

**Name:** `crochet_rag`  
**Python:** 3.11  
**Created:** October 28, 2025  
**Location:** `C:\Users\annar\.conda\envs\crochet_rag`

---

## Quick Start

### Activate Environment
```powershell
conda activate crochet_rag
```

### Install Dependencies
```powershell
pip install -r requirements.txt
```

### Verify Installation
```powershell
python test_api.py
```

---

## Environment Management

### List all environments
```powershell
conda env list
```

### Check active environment
```powershell
conda info --envs
# Active environment has * next to it
```

### Export environment (for sharing/backup)
```powershell
conda env export > environment.yml
```

### Recreate environment from file
```powershell
conda env create -f environment.yml
```

### Remove environment (if needed)
```powershell
conda deactivate
conda env remove -n crochet_rag
```

---

## Installed Packages

**Core AI/LLM:**
- google-generativeai (Gemini Pro API)

**Vector Database:**
- chromadb (semantic search)

**Data Processing:**
- pandas (Excel/CSV handling)
- openpyxl (Excel file support)
- numpy (numerical operations)

**PDF Processing:**
- PyPDF2 (PDF text extraction)
- pdfplumber (alternative PDF parser)

**Environment & Config:**
- python-dotenv (environment variables)

**Web Interface:**
- streamlit (web app)

**Utilities:**
- tqdm (progress bars)

---

## Troubleshooting

### Environment not activating
```powershell
# Initialize conda for PowerShell
conda init powershell
# Restart terminal
```

### Wrong Python version
```powershell
python --version
# Should show Python 3.11.x
```

### Packages installing to wrong location
```powershell
# Check pip location
where.exe pip
# Should point to crochet_rag environment
```

### Import errors
```powershell
# Make sure environment is active
conda activate crochet_rag
# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

---

**Last Updated:** October 28, 2025
