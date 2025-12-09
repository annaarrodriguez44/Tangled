# 🧶 Crochet Pattern & Yarn Management System

A RAG (Retrieval-Augmented Generation) based system for extracting, storing, and querying crochet pattern information, with intelligent yarn recommendation capabilities.

---

## 📋 Project Overview

This system helps crochet enthusiasts manage their pattern library and find the perfect yarn for each project. It uses AI agents powered by Google Gemini Pro to:

1. **Extract information** from crochet pattern PDFs automatically
2. **Store structured data** about yarns and their properties
3. **Match patterns to yarns** based on multiple criteria
4. **Answer natural language queries** about patterns and yarn choices

### Why This Project?

Managing a growing collection of crochet patterns and choosing the right yarn can be overwhelming. This system:
- ✅ Eliminates manual data entry from pattern PDFs
- ✅ Provides instant yarn recommendations based on pattern requirements
- ✅ Considers multiple factors: fiber content, weight, price, washability, season
- ✅ Helps you make informed decisions about your crochet projects
- ✅ Grows smarter as you add more patterns and yarns

---

## 🏗️ System Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface                            │
│              (Streamlit / Jupyter / CLI)                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                     AI Agents Layer                          │
│  ┌──────────────────────┐    ┌──────────────────────┐      │
│  │ PDF Extraction Agent │    │  Query Agent         │      │
│  │ (Gemini Pro)         │    │  (Gemini Pro)        │      │
│  └──────────────────────┘    └──────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Memory Systems                            │
│  ┌────────────────┐  ┌────────────────┐  ┌───────────────┐ │
│  │  Vector DB     │  │  Excel DB      │  │  Conversation │ │
│  │  (ChromaDB)    │  │  (Yarn+Pattern)│  │  Memory       │ │
│  │  Semantic      │  │  Structured    │  │  Context      │ │
│  └────────────────┘  └────────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Key Technologies

- **AI/LLM**: Google Gemini Pro (Student API)
- **Vector Database**: ChromaDB
- **Structured Data**: Excel (.xlsx) with pandas
- **PDF Processing**: PyPDF2 or pdfplumber
- **Interface**: Streamlit (web app) or Jupyter Notebooks
- **Language**: Python 3.10+

---

## 📂 Documentation Files

This project includes comprehensive documentation:

### 1. [`agents.md`](./agents.md)
Detailed documentation of all AI agents in the system:
- **PDF Pattern Extraction Agent**: How it extracts data from pattern PDFs
- **Database Query Agent**: How it matches patterns to yarns
- **Future enhancements**: Planned features

**Read this if you want to understand:**
- How the agents work
- What data gets extracted
- How queries are processed
- The matching algorithm

### 2. [`memory.md`](./memory.md)
Complete guide to the memory and storage systems:
- **Vector Database**: Semantic search capabilities
- **Excel Database**: Structured data schema
- **Conversation Memory**: Chat context management
- **Cache System**: Performance optimization

**Read this if you want to understand:**
- Where data is stored
- Database schemas
- How searches work
- Data flow and backup strategies

### 3. This README
High-level overview, quick start guide, and usage examples.

---

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.10 or higher
- **RAM**: 16GB (you have this ✓)
- **Storage**: ~1GB for dependencies + pattern storage
- **API Key**: Google Gemini Pro API key (free for students)

### Installation

1. **Clone or navigate to the project directory**
   ```powershell
   cd c:\Users\annar\OneDrive\Escritorio\Biomedical_Python_Course\crochet_project
   ```

2. **Create virtual environment** (recommended)
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies** (to be created)
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up API key**
   Create a `.env` file:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### Required Python Packages

Create `requirements.txt` with:
```
google-generativeai>=0.3.0
chromadb>=0.4.0
pandas>=2.0.0
openpyxl>=3.1.0
PyPDF2>=3.0.0
pdfplumber>=0.10.0
python-dotenv>=1.0.0
streamlit>=1.28.0
numpy>=1.24.0
```

---

## 💡 How It Works

### Workflow 1: Adding New Patterns

```
1. Download pattern PDF → Save to /patterns/ folder
2. Run extraction agent → python extract_patterns.py --batch
3. Agent reads PDF → Extracts key information using Gemini Pro
4. Validates data → Stores in Excel + Vector DB
5. Ready to query! → Ask questions about the pattern
```

### Workflow 2: Finding the Right Yarn

```
1. Ask question → "What yarn should I use for baby blanket pattern?"
2. Query agent → Searches vector DB + Excel DB
3. Matches criteria → Weight, composition, season, washability
4. Ranks results → Weighted scoring algorithm
5. Get recommendations → With explanations and alternatives
```

---

## 🎯 Use Cases

### For Pattern Management
- "What patterns do I have that use worsted weight yarn?"
- "Show me beginner-friendly amigurumi patterns"
- "Which patterns need only basic stitches?"
- "Find patterns similar to this granny square blanket"

### For Yarn Selection
- "What's the best yarn for a summer top pattern?"
- "Find cotton yarns under €5 per ball"
- "Which of my yarns works for this baby blanket?"
- "Compare these three yarns for my pattern"

### For Project Planning
- "How much will this project cost with different yarns?"
- "What's a good substitute for this discontinued yarn?"
- "Show me patterns I can make with the yarn I already have"

---

## 📊 Data Structure

### Pattern Information Extracted
- Pattern Name
- Pattern Structure (construction method)
- Yarn Weight (fingering, sport, DK, worsted, etc.)
- Recommended Yarn Composition
- Hook Size (mm)
- Difficulty Level
- Complete Materials List
- Recommended Colors
- Required Stitches

### Yarn Database Fields
- Product Name & Brand
- Price (€)
- Fiber Composition (% of each fiber type)
- Yarn Thickness/Weight
- Rating (1-5 stars)
- Season Recommendation
- Washing Instructions
- Overall Quality Score (weighted)

---

## 🔧 Configuration

### Extraction Settings
Customize in `config.yaml`:
```yaml
extraction:
  batch_size: 10
  retry_attempts: 3
  confidence_threshold: 0.7
  output_format: "excel"
  
gemini:
  model: "gemini-pro"
  temperature: 0.1
  max_tokens: 2048
```

### Query Settings
```yaml
query:
  max_results: 10
  similarity_threshold: 0.75
  enable_conversation_memory: true
  
matching:
  weights:
    yarn_weight: 0.25
    composition: 0.20
    season: 0.15
    washing: 0.15
    rating: 0.15
    price: 0.10
```

---

## 📈 Current Status & Roadmap

### ✅ Phase 1: Foundation (Current)
- [x] System architecture design
- [x] Documentation created
- [ ] PDF extraction agent implementation
- [ ] Vector database setup
- [ ] Excel integration
- [ ] Basic query agent

### 🔄 Phase 2: Core Features
- [ ] Streamlit web interface
- [ ] Batch PDF processing
- [ ] Pattern-to-yarn matching algorithm
- [ ] Natural language queries
- [ ] Data validation & error handling

### 🔮 Phase 3: Enhancements
- [ ] Image recognition for pattern diagrams
- [ ] Cost calculator for projects
- [ ] Yarn substitution engine
- [ ] Community pattern sharing
- [ ] Mobile-friendly interface

---

## 🎓 Learning Outcomes

This project demonstrates:
- **RAG Systems**: Retrieval-Augmented Generation with LLMs
- **Vector Databases**: Semantic search and embeddings
- **API Integration**: Working with Google Gemini Pro
- **Data Processing**: PDF extraction and structured data management
- **Agent Design**: Multi-agent system architecture
- **Python Best Practices**: Clean code, documentation, error handling

---

## 📝 Example Usage

### Extract Pattern from PDF
```python
from agents.pdf_extractor import PDFPatternExtractor

extractor = PDFPatternExtractor()
pattern = extractor.extract("patterns/baby_blanket.pdf")

print(pattern['name'])  # "Cozy Baby Blanket"
print(pattern['yarn_weight'])  # "DK"
print(pattern['difficulty'])  # "Beginner"
```

### Query for Yarn Recommendations
```python
from agents.query_agent import QueryAgent

agent = QueryAgent()
results = agent.query(
    "Find soft, machine-washable yarns for baby blanket pattern",
    pattern_id="baby_blanket_01"
)

for yarn in results:
    print(f"{yarn.name}: {yarn.score:.2f} - {yarn.reason}")
```

### Batch Process PDFs
```python
from agents.pdf_extractor import PDFPatternExtractor

extractor = PDFPatternExtractor()
results = extractor.batch_process(
    directory="patterns/",
    pattern="*.pdf"
)

print(f"Processed {len(results)} patterns")
print(f"Successful: {sum(1 for r in results if r.success)}")
```

---

## 🤝 Contributing

This is a personal learning project, but suggestions are welcome!

### To Suggest Improvements
1. Review the documentation
2. Consider the use cases
3. Propose enhancements that align with the project goals

---

## 📄 License

Personal project for educational purposes.

---

## 👤 Author

**Anna R.**  
Biomedical Python Course Project  
Created: October 28, 2025

---

## 🆘 Troubleshooting

### Common Issues

**PDF extraction fails**
- Check PDF is text-based (not scanned image)
- Verify Gemini API key is valid
- Check internet connection

**Query returns no results**
- Ensure patterns are added to database
- Check spelling and query phrasing
- Verify Excel database is accessible

**Out of memory errors**
- Reduce batch size
- Process fewer PDFs at once
- Close other applications

---

## 📚 Additional Resources

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Pandas Excel Guide](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html)
- [RAG Systems Overview](https://python.langchain.com/docs/use_cases/question_answering/)

---

## 🎉 Acknowledgments

- Google for Gemini Pro Student API access
- Crochet community for pattern inspiration
- Biomedical Python Course for the learning framework

---

**Happy Crocheting! 🧶✨**
