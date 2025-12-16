# Tangled - System Architecture

**Project:** Crochet Pattern Management System  
**Version:** 1.0  
**Last Updated:** December 16, 2025  
**Author:** Anna R.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [Application Architecture](#application-architecture)
4. [Data Architecture](#data-architecture)
5. [AI/LLM Integration](#aillm-integration)
6. [File Structure](#file-structure)
7. [Page Components](#page-components)
8. [Data Flow](#data-flow)
9. [Security & Configuration](#security--configuration)
10. [Deployment](#deployment)

---

## System Overview

**Tangled** is a comprehensive crochet pattern management system built with Streamlit. It provides pattern browsing, yarn inventory tracking, project management, AI-powered pattern extraction, and community features.

### Key Features

- **Pattern Management**: Browse 18+ patterns with advanced filtering
- **Yarn Inventory**: Track personal yarn stash with 102 yarns
- **AI Pattern Extraction**: Batch process PDF patterns using Google Gemini API
- **Temperature-Aware Recommendations**: Location-based yarn suggestions
- **Project Tracking**: Monitor WIP and completed projects
- **Community Forum**: Share tips, ask questions, showcase projects
- **Price Tracking**: Monitor yarn prices with trend visualization
- **Photo Gallery**: Upload and manage project photos
- **Pattern Notes**: Document modifications and personal notes

### Architecture Type

**Multi-Page Application (MPA)** with:
- Centralized data storage (Excel files)
- Vector database for semantic search (ChromaDB)
- External API integration (Google Gemini)
- Session-based state management

---

## Technology Stack

### Core Framework

- **Streamlit 1.40+** - Web application framework
- **Python 3.13** - Programming language
- **Conda** - Environment management (`crochet_rag`)

### Data Management

- **Pandas** - Data manipulation and analysis
- **openpyxl** - Excel file I/O
- **ChromaDB** - Vector database for semantic search

### AI/LLM

- **Google Gemini API** - Pattern extraction and content generation
  - Model: `gemini-2.5-flash`
  - Features: PDF text analysis, structured data extraction
- **google-generativeai** - Python SDK for Gemini

### PDF Processing

- **pdfplumber** - PDF text extraction
- **PyPDF2** - Alternative PDF reading

### Visualization

- **Plotly** - Interactive charts (price trends)
- **Pillow (PIL)** - Image processing for photo gallery

### Environment

- **python-dotenv** - Environment variable management
- **OS/Platform**: Windows 10/11, cross-platform compatible

---

## Application Architecture

### Architectural Pattern

**Modular Multi-Page Architecture** with shared state and utilities.

```
┌─────────────────────────────────────────────────────────────┐
│                    User Browser                             │
│                  (http://localhost:8508)                    │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 Streamlit Server                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Homepage (streamlit_app.py / Home.py)                │  │
│  │  - Navigation hub                                     │  │
│  │  - Feature cards                                      │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Pages Module (pages/)                                │  │
│  │  ┌─────────────────┬──────────────────┬─────────────┐ │  │
│  │  │ Pattern Browser │ Yarn Inventory   │ Add Patterns│ │  │
│  │  │ Project Tracker │ Price Tracker    │ Photo Gallery│ │  │
│  │  │ Pattern Notes   │ Comparison Tool  │ Community   │ │  │
│  │  └─────────────────┴──────────────────┴─────────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Business Logic Layer                                 │  │
│  │  - slice10_yarn_match.py (matching algorithms)        │  │
│  │  - ratings_notes_utils.py (rating utilities)          │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────┬─────────────────────┬─────────────────────┬────┘
             │                     │                     │
             ▼                     ▼                     ▼
    ┌────────────────┐    ┌────────────────┐    ┌──────────────┐
    │ Excel Files    │    │ ChromaDB       │    │ Gemini API   │
    │ (Data Storage) │    │ (Vector Search)│    │ (AI Extract) │
    └────────────────┘    └────────────────┘    └──────────────┘
```

### Layer Responsibilities

#### Presentation Layer (Streamlit Pages)
- User interface rendering
- Form validation
- Session state management
- User interactions

#### Business Logic Layer (Utility Scripts)
- Pattern-yarn matching algorithms
- Temperature-based recommendations
- Rating calculations
- Data validation

#### Data Access Layer
- Excel file operations (CRUD)
- Vector database queries
- API calls to external services

---

## Data Architecture

### Data Storage Strategy

**Hybrid Storage Model:**
1. **Structured Data** → Excel files (easy editing, Excel-compatible)
2. **Vector Embeddings** → ChromaDB (semantic search)
3. **Binary Data** → File system (PDFs, images)

### Database Schema

#### 1. `pattern_database.xlsx`
**Purpose:** Master pattern catalog

| Column | Type | Description |
|--------|------|-------------|
| Pattern Name | String | Unique pattern identifier |
| Pattern Structure | String | Construction method (rounds/flat/top-down) |
| Yarn Weight | String | Recommended yarn weight |
| Recommended Yarn Composition | String | Fiber preferences |
| Hook Size | String | Hook size (mm or US) |
| Difficulty Level | String | Skill level (beginner-expert) |
| Materials Needed | String | Complete materials list |
| Recommended Colors | String | Color suggestions |
| Stitches Required | String | List of stitches used |

#### 2. `Database_YARN.xlsx`
**Purpose:** Yarn product database (102 yarns)

| Column | Type | Description |
|--------|------|-------------|
| Name of the product | String | Yarn name |
| Price (€) | Float | Current price |
| Cotton (%) | Float | Cotton content |
| Acrylic (%) | Float | Acrylic content |
| Wool (%) | Float | Wool content |
| Silk (%) | Float | Silk content |
| Bamboo/Viscouse (%) | Float | Bamboo/viscose content |
| Linen (%) | Float | Linen content |
| Polyester (%) | Float | Polyester content |
| Nylon/Polyamide (%) | Float | Nylon content |
| Mohair/Alpaca (%) | Float | Mohair/alpaca content |
| Reflective Yarn (%) | Float | Reflective fiber content |
| Yarn thickness (web) | String | Web-listed thickness |
| Yarn thikness | String | Standardized thickness |
| Color | String | Color name |
| Needle/Hook Size (mm) | String | Recommended hook size |
| Rating (★) | Float | User rating |
| Brand | String | Manufacturer |

#### 3. `yarn_inventory.xlsx`
**Purpose:** Personal yarn stash tracking

| Column | Type | Description |
|--------|------|-------------|
| Yarn_Name | String | Yarn name |
| Brand | String | Brand name |
| Color | String | Color name |
| Weight | String | Yarn weight category |
| Fiber_Content | String | Fiber composition |
| Quantity_Skeins | Integer | Number of skeins |
| Grams_Per_Skein | Integer | Weight per skein |
| Total_Grams | Integer | Total weight |
| Needle_Hook_Size | String | Recommended hook size |
| Yarn_Thickness | String | Thickness category |
| Season | String | Best season for use |
| Location | String | Storage location |
| Purchase_Date | Date | Purchase date |
| Purchase_Price | Float | Price paid |
| Notes | String | Additional notes |
| Date_Added | Datetime | Record creation timestamp |

#### 4. `projects.xlsx`
**Purpose:** Project tracking

| Column | Type | Description |
|--------|------|-------------|
| Project_Name | String | Project name |
| Pattern_Name | String | Pattern used |
| Status | String | WIP/Completed/Planned |
| Yarn_Used | String | Yarn(s) used |
| Hook_Size | String | Hook size used |
| Start_Date | Date | Project start date |
| Completion_Date | Date | Completion date (if done) |
| Hours_Spent | Float | Time invested |
| Notes | String | Project notes |
| Photo_Path | String | Path to project photo |
| Date_Added | Datetime | Record creation |

#### 5. `pattern_ratings.xlsx`
**Purpose:** Pattern reviews and ratings

| Column | Type | Description |
|--------|------|-------------|
| Pattern_Name | String | Pattern name |
| Overall_Rating | Integer | 1-5 stars |
| Difficulty_vs_Listed | String | Easier/As Listed/Harder |
| Would_Make_Again | Boolean | Yes/No |
| Completed_Date | Date | When completed |
| Time_Taken_Hours | Float | Total time |
| Review_Text | String | Written review |
| Date_Added | Datetime | Review timestamp |

#### 6. `pattern_notes.xlsx`
**Purpose:** Pattern modifications and tips

| Column | Type | Description |
|--------|------|-------------|
| Pattern_Name | String | Pattern name |
| Note_Type | String | General/Modification/etc |
| Note_Text | String | Note content |
| Hook_Size_Used | String | Hook used |
| Yarn_Substitution | String | Yarn substitutions made |
| Modifications_Made | String | Pattern modifications |
| Tips | String | Tips for next time |
| Date_Added | Datetime | Note timestamp |

#### 7. `yarn_price_history.xlsx`
**Purpose:** Yarn price tracking over time

| Column | Type | Description |
|--------|------|-------------|
| Yarn_Name | String | Yarn name |
| Brand | String | Brand |
| Price | Float | Price (€) |
| Date | Date | Price observation date |
| Store | String | Store name |
| On_Sale | Boolean | Sale indicator |
| Notes | String | Additional notes |

#### 8. `project_gallery.xlsx`
**Purpose:** Photo gallery metadata

| Column | Type | Description |
|--------|------|-------------|
| Project_Name | String | Project name |
| Pattern_Name | String | Pattern used |
| Image_Path | String | Relative path to image |
| Caption | String | Photo caption |
| Completion_Date | Date | Project completion |
| Rating | Integer | Personal rating (1-5) |
| Tags | String | Comma-separated tags |
| Upload_Date | Datetime | Photo upload timestamp |

#### 9. `community_comments.xlsx`
**Purpose:** Community forum posts

| Column | Type | Description |
|--------|------|-------------|
| Comment_ID | String | Unique ID (timestamp-based) |
| Username | String | Poster username |
| Category | String | Discussion category |
| Subject | String | Post subject |
| Message | String | Post content |
| Timestamp | Datetime | Post time |
| Likes | Integer | Like count |
| Pattern_Referenced | String | Optional pattern reference |
| Tags | String | Post tags |

### Vector Database (ChromaDB)

**Collection:** `crochet_patterns`

**Purpose:** Semantic search for patterns

**Schema:**
```python
{
    "ids": ["pattern_1", "pattern_2", ...],
    "documents": ["Full pattern text...", ...],
    "metadatas": [
        {
            "pattern_name": "...",
            "difficulty": "...",
            "yarn_weight": "...",
            "hook_size": "..."
        },
        ...
    ],
    "embeddings": [[0.123, 0.456, ...], ...]  # Vector embeddings
}
```

---

## AI/LLM Integration

### Google Gemini API

**Model:** `gemini-2.5-flash`  
**API Version:** v1beta  
**Authentication:** API Key (stored in `.env`)

#### Use Cases

##### 1. PDF Pattern Extraction
**Location:** `pages/9_📚_Add_Patterns.py`

**Process:**
```
PDF Upload → pdfplumber extraction → Raw Text → Gemini API → Structured JSON → Excel Database
```

**Extracted Fields:**
- Pattern Name
- Pattern Structure
- Yarn Weight
- Recommended Yarn Composition
- Hook Size
- Difficulty Level
- Materials Needed
- Recommended Colors
- Stitches Required

**Prompt Template:**
```python
"""
Extract the following information from this crochet pattern:

{pdf_text}

Return ONLY a JSON object with these exact keys:
{
  "pattern_name": "...",
  "pattern_structure": "...",
  "yarn_weight": "...",
  "recommended_yarn_composition": "...",
  "hook_size": "...",
  "difficulty_level": "...",
  "materials_needed": "...",
  "recommended_colors": "...",
  "stitches_required": "..."
}
"""
```

**Error Handling:**
- Retry logic with exponential backoff (15s → 30s → 60s)
- Rate limit detection (429 errors)
- Quota exceeded handling
- Invalid JSON response recovery

##### 2. Future AI Features (Planned)
- Pattern difficulty re-assessment
- Yarn substitution suggestions
- Image recognition for pattern diagrams
- Multi-language pattern translation

---

## File Structure

```
crochet_project/
│
├── streamlit_app.py              # Main homepage (entry point)
├── Home.py                        # Copy of homepage for navigation
│
├── pages/                         # Multi-page app pages
│   ├── 1__Pattern_Browser.py     # Pattern browsing & recommendations
│   ├── 2_ℹ️_About.py              # About page
│   ├── 3_🧵_Yarn_Inventory.py    # Personal yarn stash tracker
│   ├── 4_📝_Project_Tracker.py   # WIP & completed projects
│   ├── 5_⚖️_Pattern_Comparison.py # Compare 2-3 patterns
│   ├── 6_📸_Photo_Gallery.py     # Project photos
│   ├── 7_⭐_Pattern_Notes.py     # Pattern notes & ratings
│   ├── 8_💰_Price_Tracker.py     # Yarn price history
│   ├── 9_📚_Add_Patterns.py      # AI-powered batch PDF processor
│   └── 10_💬_Community_Forum.py  # Community discussion forum
│
├── slice*.py                      # Development slices (implementation steps)
│   ├── slice1_pdf_read.py
│   ├── slice2_gemini_extract.py
│   ├── slice3_full_extract.py
│   ├── slice4_excel_integration.py
│   ├── slice5_batch_process.py
│   ├── slice6_chromadb_setup.py
│   ├── slice7_semantic_search.py
│   ├── slice8_query_agent.py
│   ├── slice9_combined_agent.py
│   └── slice10_yarn_match.py     # Imported by Pattern Browser
│
├── ratings_notes_utils.py         # Shared utilities for ratings
│
├── pattern_database.xlsx          # Master pattern catalog
├── Database_YARN.xlsx             # Yarn product database
├── yarn_inventory.xlsx            # Personal yarn stash
├── projects.xlsx                  # Project tracking
├── pattern_ratings.xlsx           # Pattern reviews
├── pattern_notes.xlsx             # Pattern notes
├── yarn_price_history.xlsx        # Price tracking
├── project_gallery.xlsx           # Photo gallery metadata
├── community_comments.xlsx        # Forum posts
│
├── PDFPatterns/                   # PDF pattern storage (44 patterns)
│   ├── All-That-Zippered-Pouch.pdf
│   ├── Beach Bag.pdf
│   └── ...
│
├── project_photos/                # Uploaded project images
│   └── *.jpg, *.png
│
├── chroma_db/                     # ChromaDB vector database
│   ├── chroma.sqlite3
│   └── [collection_id]/
│
├── .env                           # Environment variables (API keys)
├── requirements.txt               # Python dependencies
├── requirements_deploy.txt        # Deployment-specific requirements
│
├── README.md                      # Project documentation
├── ARCHITECTURE.md                # This file
├── agents.md                      # AI agent specifications
├── memory.md                      # Session memory/progress
├── PROJECT_PROGRESS.md            # Development progress tracker
├── TESTING_GUIDE.md               # Testing procedures
├── DOMAIN_SETUP_TUTORIAL.md       # Domain setup guide
├── DOMAIN_DEPLOYMENT.md           # Deployment instructions
└── README_DEPLOY.md               # Deployment README

```

---

## Page Components

### 1. Homepage (`streamlit_app.py`)

**Purpose:** Navigation hub and feature showcase

**Components:**
- Hero section with app description
- Statistics display (patterns, yarns, projects)
- Feature cards (9 cards in 3 categories)
- How It Works section
- Call-to-action
- Footer

**Navigation:** `st.switch_page()` to feature pages

### 2. Pattern Browser (`pages/1__Pattern_Browser.py`)

**Purpose:** Browse patterns with temperature-aware yarn recommendations

**Features:**
- Location selector (10+ global locations)
- Real-time temperature adjustment
- Advanced filters (difficulty, yarn weight, structure, season)
- Semantic search (if vector DB available)
- Pattern-yarn matching algorithm
- Purchase links generation
- Favorites system

**Key Algorithm:**
```python
match_score = (
    pattern_match_score * 0.70 +
    temperature_match_score * 0.30
)
```

### 3. Yarn Inventory (`pages/3_🧵_Yarn_Inventory.py`)

**Purpose:** Track personal yarn stash

**Actions:**
- View Inventory (with 6 filters)
- Add New Yarn
- Edit/Delete Yarn
- Statistics Dashboard

**Filters:**
- Yarn Weight
- Brand
- Needle/Hook Size
- Yarn Thickness
- Season
- Search (name/color)

### 4. Add Patterns (`pages/9_📚_Add_Patterns.py`)

**Purpose:** Batch process PDF patterns with AI

**Tabs:**
1. **Preview** - Test extraction on single PDF
2. **Batch Process** - Process multiple PDFs
3. **Database View** - Browse extracted patterns

**AI Workflow:**
```
Upload PDFs → Extract Text (pdfplumber) → 
Send to Gemini → Parse JSON → Save to Excel → 
Store in Vector DB
```

### 5. Community Forum (`pages/10_💬_Community_Forum.py`)

**Purpose:** Community interaction

**Features:**
- Post comments with categories
- Like system
- Category filters (10 categories)
- Search functionality
- Sort by date/popularity
- Pattern references
- Tags

### 6. Price Tracker (`pages/8_💰_Price_Tracker.py`)

**Purpose:** Monitor yarn prices over time

**Features:**
- Add price observations
- Import from yarn database
- Price history charts (Plotly)
- Sale detection
- Price change alerts
- Brand filtering

### 7. Other Pages

- **Project Tracker** - Manage WIP/completed projects
- **Photo Gallery** - Upload/view project photos with ratings
- **Pattern Notes** - Document modifications and tips
- **Pattern Comparison** - Side-by-side comparison (2-3 patterns)
- **About** - App information and documentation

---

## Data Flow

### Pattern Browsing Flow

```
User Input (Location, Filters) 
    ↓
Pattern Database Query
    ↓
Apply Filters (difficulty, yarn weight, etc.)
    ↓
Yarn Database Query
    ↓
Match Algorithm (pattern + temperature)
    ↓
Score & Rank Yarns
    ↓
Display Top 3 Recommendations
    ↓
Generate Purchase Links
```

### AI Pattern Extraction Flow

```
PDF Upload
    ↓
pdfplumber Text Extraction
    ↓
Gemini API Request (with retry logic)
    ↓
JSON Response Parsing
    ↓
Data Validation
    ↓
Excel Database Insert
    ↓
ChromaDB Vector Storage (optional)
    ↓
Success Confirmation
```

### Price Tracking Flow

```
Manual Price Entry / Import from Database
    ↓
Append to price_history.xlsx
    ↓
Calculate Price Changes
    ↓
Detect Sales (>10% drop)
    ↓
Generate Plotly Chart
    ↓
Display Trends & Alerts
```

---

## Security & Configuration

### Environment Variables

**File:** `.env` (not committed to Git)

```env
GEMINI_API_KEY=your_api_key_here
```

**Loading:**
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
```

### Sensitive Data

**Excluded from Git:**
- `.env` (API keys)
- `*.xlsx` (user data - optional)
- `chroma_db/` (can be regenerated)
- `project_photos/` (user uploads)
- `__pycache__/`

### Data Validation

- Form input validation (required fields, ranges)
- Excel file existence checks
- DataFrame column validation
- JSON schema validation for API responses

---

## Deployment

### Local Development

**Requirements:**
- Python 3.13
- Conda environment `crochet_rag`
- Port 8508 (configurable)

**Commands:**
```powershell
conda activate crochet_rag
python -m streamlit run streamlit_app.py --server.port 8508
```

### Streamlit Cloud Deployment

**Platform:** Streamlit Community Cloud  
**Repository:** GitHub (annaarrodriguez44/Tangled)  
**Branch:** main

**Configuration:**
- Auto-deploy on push to main
- Secrets management (API keys)
- Resource limits (free tier)

**Custom Domain:**
- Subdomain configuration
- HTTPS automatic
- CDN support

### Docker Deployment (Optional)

**Dockerfile:**
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

---

## Performance Considerations

### Optimization Strategies

1. **Caching:**
   - `@st.cache_data` for database loads
   - `@st.cache_resource` for ChromaDB connection

2. **Lazy Loading:**
   - Load data only when needed
   - Defer heavy computations

3. **Pagination:**
   - Limit displayed records
   - Expandable sections for details

4. **API Rate Limiting:**
   - Exponential backoff for Gemini API
   - Batch processing with delays

### Known Limitations

- Free Gemini API quota (60 requests/minute)
- Excel file I/O performance (vs SQL)
- Vector DB requires local storage
- Session state not persistent across restarts

---

## Future Architecture Enhancements

### Planned Improvements

1. **Database Migration:**
   - Move from Excel to PostgreSQL/SQLite
   - Better concurrency and performance

2. **API Layer:**
   - RESTful API for data access
   - Separate frontend/backend

3. **Authentication:**
   - User accounts and login
   - Multi-user support
   - Personal data isolation

4. **Real-time Features:**
   - WebSocket for live forum updates
   - Real-time collaboration

5. **Advanced AI:**
   - Image recognition for pattern diagrams
   - Video pattern extraction
   - Multi-language support

6. **Mobile App:**
   - Native iOS/Android apps
   - Offline support
   - Camera integration

---

## Appendix

### Key Dependencies

```
streamlit>=1.40.0
pandas>=2.2.0
openpyxl>=3.1.0
chromadb>=0.4.0
google-generativeai>=0.3.0
pdfplumber>=0.10.0
plotly>=5.18.0
Pillow>=10.0.0
python-dotenv>=1.0.0
```

### Development Tools

- **VS Code** - IDE
- **Git** - Version control
- **GitHub** - Repository hosting
- **PowerShell** - Terminal
- **Conda** - Environment management

### References

- [Streamlit Documentation](https://docs.streamlit.io)
- [Google Gemini API](https://ai.google.dev/docs)
- [ChromaDB Documentation](https://docs.trychroma.com)
- [Plotly Python](https://plotly.com/python/)

---

**Last Updated:** December 16, 2025  
**Version:** 1.0  
**Maintainer:** Anna R.
