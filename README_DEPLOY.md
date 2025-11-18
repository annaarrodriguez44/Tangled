# 🧶 Tangled - Crochet Pattern Planner

**Temperature-aware yarn recommendations for your crochet projects**

## Features

- 📋 Browse 32+ crochet patterns with detailed information
- 🌡️ Temperature-based yarn recommendations (not just seasons!)
- 📍 Location-aware matching (Sweden, Spain, UK, USA, Canada, and more)
- 🧵 Smart yarn scoring algorithm matching 102+ yarns
- 🪡 Stitch tutorials and guidance
- 🎨 Color palette inspiration
- 🛒 Direct purchase links (Hobbii, Katia)
- 🔍 Advanced pattern search and filtering

## How It Works

1. **Select your location** - App adjusts for your local temperature
2. **Browse patterns** - Filter by difficulty, yarn weight, or search
3. **Get recommendations** - Top 3 yarns matched to pattern + temperature
4. **View details** - Stitches needed, materials, color suggestions
5. **Shop directly** - Links to purchase recommended yarns

## Temperature-Based Matching

Unlike simple seasonal recommendations, Tangled considers:
- Your actual location temperature (Sweden winter ≠ Spain winter)
- Yarn fiber composition (wool for cold, cotton for warm)
- Comfort ranges for each yarn type
- Combined pattern + temperature scoring

Example: In November, Sweden (8°C) gets wool recommendations while Spain (15°C) gets blends.

## Tech Stack

- **Frontend**: Streamlit
- **AI**: Google Gemini Pro for pattern extraction
- **Vector DB**: ChromaDB for semantic search
- **Data**: Excel databases (patterns + yarns)
- **PDF Processing**: pdfplumber

## Local Development

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/Tangled.git
cd Tangled

# Install dependencies
pip install -r requirements_deploy.txt

# Set up API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Run app
streamlit run pattern_planner_app.py
```

## Deployment

Deployed on Streamlit Community Cloud with automatic GitHub integration.

## Data Sources

- 18 unique crochet patterns extracted from PDFs
- 102 yarns from Hobbii and Katia databases
- Temperature data for 10+ global locations

## Project Structure

```
Tangled/
├── pattern_planner_app.py      # Main Streamlit app
├── slice10_yarn_match.py       # Yarn matching algorithm
├── Database_YARN.xlsx          # Yarn database (102 yarns)
├── pattern_database.xlsx       # Pattern database (32 patterns)
├── PDFPatterns/                # Original pattern PDFs
├── requirements_deploy.txt     # Python dependencies
└── .streamlit/config.toml      # Streamlit config
```

## Contributing

This is a personal project but suggestions welcome! Open an issue or PR.

## License

MIT License - feel free to use for your own crochet projects!

---

Made with ❤️ for crochet enthusiasts by Anna R.
