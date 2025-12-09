# Crochet Pattern RAG Agents

## Core Instructions

### 0. Communication Style

**NO SYCOPHANTIC WORDING. NO FAWNING. NO SUPPLICATION. NO HYPERBOLE.**

You are a work colleague, not a personal assistant. Provide direct, honest feedback even if it's uncomfortable.

**Do:**

- Point out flaws, gaps, and weaknesses directly
- Say "This section is weak" not "This section could be strengthened"
- Say "This won't work" not "We might want to reconsider"
- Challenge assumptions and bad ideas
- Give honest assessments of likelihood of success
- Identify problems the user hasn't considered
- Use plain, direct language

**Don't:**

- Use phrases like "excellent," "wonderful," "great job," "amazing," "sophisticated," "elegant," "brilliant"
- Use flowery or dramatic language ("deep-seated," "merely intuitive," "profound")
- Praise the user or their ideas with adjectives
- Cushion criticism with praise
- Ask permission to give feedback ("Would you like me to...")
- Use excessive politeness or deference
- Pretend problems don't exist to avoid hurting feelings

**Tone:** Professional, direct, honest, plain. Like a colleague who respects you enough to tell you the truth without decoration.

### 1. Update memory.md Every 10 Changes

**CRITICAL INSTRUCTION:** After every 10 substantive changes, updates, or additions to the project, you MUST update the memory.md file to reflect:

- Current status of implementation
- Decisions made
- Code/documents completed or in progress
- Any new information discovered
- Changes to strategy or approach
- Progress on timeline
- Issues encountered and solutions

**What counts as a change:**

- Completing a major code section
- Adding new features or functions
- Making strategic decisions about implementation
- Receiving clarifications about requirements
- Completing code reviews
- Making significant edits to existing code
- Processing batches of PDFs
- Database schema changes

### 2. Slice Method Programming

**FAIL FAST. TEST SMALL. VERIFY OFTEN.**

Break all work into small, testable slices. Never write more than 50 lines of code without testing.

**Slice Approach:**

1. **Identify the smallest testable unit** - What's the absolute minimum that proves this works?
2. **Implement only that** - No feature creep, no "while I'm here" additions
3. **Test immediately** - Run it, verify output, check for errors
4. **Fix or proceed** - If it fails, fix it now. Don't move forward with broken code
5. **Document the slice** - Note what works, what doesn't, what's next

**Example: PDF Extraction Agent**

❌ **Wrong approach:**
```
Build entire PDF extraction system → Test after 500 lines → Everything breaks
```

✅ **Slice approach:**
```
Slice 1: Read one PDF, print raw text (20 lines) → Test
Slice 2: Extract pattern name only (30 lines) → Test
Slice 3: Extract yarn weight only (25 lines) → Test
Slice 4: Combine extractions (40 lines) → Test
Slice 5: Add error handling (35 lines) → Test
```

**Mandatory checks after each slice:**

- Does it run without errors?
- Does the output match expectations?
- Are edge cases handled?
- Is the code readable?
- Can it be tested independently?

**If a slice fails:** Stop. Fix it. Don't proceed to the next slice with broken code underneath.

---

## Environment Setup

### Conda Environment

**Environment Name:** `crochet_rag`  
**Python Version:** 3.11

### CRITICAL: Always Activate Environment Before Running Code

**MANDATORY STEP before ANY Python execution:**

```powershell
conda activate crochet_rag
```

**Every single time you:**
- Run Python scripts
- Install packages
- Test code
- Execute notebooks
- Use the terminal for Python work

**Check if environment is active:**
```powershell
conda env list
# Active environment has * next to it
```

**If you forget to activate:**
- Code will fail with import errors
- Packages will install to wrong environment
- You'll waste time debugging non-issues

**Installation commands (run AFTER activating environment):**

```powershell
# Activate first
conda activate crochet_rag

# Install packages
pip install -r requirements.txt

# Or install individually
pip install google-generativeai chromadb pandas openpyxl python-dotenv
```

**Deactivate when done:**
```powershell
conda deactivate
```

---

## Overview
This document describes the AI agents used in the Crochet Pattern Management System. The system uses multiple specialized agents to extract, process, and query crochet pattern information.

---

## Agent 1: PDF Pattern Extraction Agent

### Purpose
Extracts structured information from crochet pattern PDFs and populates the Excel database with pattern details.

### Capabilities
- **PDF Text Extraction**: Reads and processes PDF documents containing crochet patterns
- **Information Extraction**: Uses Gemini Pro API to identify and extract specific pattern details
- **Data Validation**: Ensures extracted data matches expected formats and ranges
- **Batch Processing**: Can process multiple PDFs at once or individually
- **Error Handling**: Manages missing information and inconsistent PDF formats

### Extracted Fields
The agent extracts the following information from each PDF:

1. **Pattern Name**: The name/title of the crochet pattern
2. **Pattern Structure**: Overall structure (e.g., worked in rounds, worked flat, top-down, bottom-up)
3. **Yarn Weight**: Recommended yarn weight (e.g., fingering, sport, DK, worsted, bulky)
4. **Recommended Yarn Composition**: Preferred fiber content (e.g., 100% cotton, acrylic blend)
5. **Hook Size**: Crochet hook size in mm or US sizing
6. **Difficulty Level**: Skill level (beginner, easy, intermediate, advanced, expert)
7. **Materials Needed**: Complete list of materials (yarn, hooks, notions, tools)
8. **Recommended Colors**: Suggested color combinations or number of colors needed
9. **Stitches Required**: List of stitches used in the pattern (e.g., sc, dc, hdc, special stitches)

### Tools Used
- **LLM**: Google Gemini Pro (Student API)
- **PDF Processing**: PyPDF2 or pdfplumber
- **Vector Database**: ChromaDB or FAISS for semantic search
- **Data Storage**: openpyxl for Excel integration

### Workflow

**Why NOT using langextract:** We have Gemini Pro, which handles varied formats and nuanced extraction better than rule-based systems.

**Technology Stack:**
- `pdfplumber` - Better text extraction (handles tables, columns, varied layouts)
- Gemini Pro - Understanding and structuring data
- No intermediate parsing libraries needed

**Implementation Slices:**

**Slice 1: Basic PDF Reading (20 lines)**
- Read one PDF file
- Extract raw text using pdfplumber
- Print output to verify
- Test with real PDF

**Slice 2: Gemini Extraction - Single Field (30 lines)**
- Send raw text to Gemini Pro
- Extract pattern name only
- Verify JSON response structure
- Handle API errors

**Slice 3: Full Field Extraction (40 lines)**
- Expand prompt for all 9 fields
- Parse complete JSON response
- Validate all fields present
- Test with multiple PDFs

**Slice 4: Excel Integration (35 lines)**
- Write extracted data to Excel row
- Handle existing file vs new file
- Verify data formatting
- Test append operations

**Slice 5: Batch Processing (45 lines)**
- Loop through PDF directory
- Add progress tracking
- Error handling per file
- Summary report

**Slice 6: ChromaDB Setup (30 lines)**
- Initialize ChromaDB collection
- Store one pattern + metadata
- Test retrieval by ID
- Verify persistence

**Slice 7: Embeddings & Search (40 lines)**
- Generate embeddings for pattern text
- Store in vector database
- Test similarity search
- Validate results quality

**Slice 8: Basic Query Agent (35 lines)**
- Parse user question
- Query Excel database
- Filter and return results
- Format response

**Slice 9: Semantic Search Integration (40 lines)**
- Add vector database queries
- Combine Excel + vector results
- Rank by relevance
- Handle no-results case

**Slice 10: Pattern-Yarn Matching (50 lines)**
- Implement scoring algorithm
- Match yarn properties to pattern needs
- Rank recommendations
- Generate explanations

**Each slice:** Build → Test → Fix → Document → Move to next

### Configuration
- **API Key**: Gemini Pro API key (stored in environment variables)
- **Processing Mode**: Single file or batch
- **Output Format**: JSON → Excel row
- **Retry Logic**: 3 attempts for failed extractions
- **Confidence Threshold**: Flags entries with low confidence for manual review

---

## Agent 2: Database Query & Recommendation Agent

### Purpose
Provides natural language interface to query the yarn and pattern database, matching patterns with suitable yarns based on multiple criteria.

### Capabilities
- **Natural Language Queries**: Understands questions like "What yarn should I use for a baby blanket pattern?"
- **Multi-criteria Matching**: Matches patterns to yarns based on:
  - Yarn composition
  - Weight/thickness
  - Season suitability
  - Washing requirements
  - Price range
  - Rating
  - Pattern requirements
- **Smart Recommendations**: Suggests optimal yarn choices considering all factors
- **Comparative Analysis**: Can compare multiple yarn options for a single pattern

### Query Types Supported
1. **Pattern-to-Yarn**: "Which yarns work with [pattern name]?"
2. **Yarn-to-Pattern**: "What patterns can I make with [yarn name]?"
3. **Composition Search**: "Find 100% cotton yarns suitable for summer projects"
4. **Budget-Based**: "Show affordable options for this pattern under €X"
5. **Difficulty-Based**: "Beginner-friendly patterns using worsted weight yarn"
6. **Stitch-Based**: "Patterns that use only basic stitches (sc, dc, hdc)"

### Tools Used
- **LLM**: Google Gemini Pro for query understanding and response generation
- **Database**: Excel file with yarn composition and properties
- **Vector Search**: Semantic search through pattern descriptions
- **Pandas**: Data manipulation and filtering

### Workflow
```
1. User query → 2. Parse intent with Gemini → 3. Query Excel database + Vector DB
→ 4. Apply filters and matching logic → 5. Rank results
→ 6. Generate natural language response with recommendations
```

### Matching Algorithm
The agent uses a weighted scoring system:
- **Yarn Weight Match**: 25% (must match or be compatible)
- **Composition Suitability**: 20% (based on pattern requirements)
- **Season Compatibility**: 15% (if specified)
- **Washing Compatibility**: 15% (convenience factor)
- **Overall Rating**: 15% (quality indicator)
- **Price/Value**: 10% (budget consideration)

---

## Agent 3: Conversation Memory Agent (Future Enhancement)

### Purpose
Maintains context across conversations to provide personalized recommendations based on user preferences and history.

### Planned Capabilities
- Remember user preferences (favorite yarns, colors, difficulty level)
- Track completed projects
- Suggest new patterns based on past preferences
- Learn from user feedback

---

## Integration & Communication

### Agent Coordination
- Agents work independently but share access to the same databases
- PDF Extraction Agent populates the database
- Query Agent reads from the database
- Both agents can trigger updates to the vector database for improved search

### Error Handling
- Missing PDF fields → Flag for manual entry
- API failures → Retry with exponential backoff
- Invalid queries → Request clarification from user
- Database conflicts → Version control and backup

### Performance Optimization
- Batch PDF processing during off-peak times
- Cache frequent queries
- Pre-compute common yarn-pattern matches
- Incremental vector database updates

---

## Usage Examples

### Example 1: Extract from PDF
```python
from pdf_extraction_agent import PDFPatternExtractor

extractor = PDFPatternExtractor(api_key="GEMINI_API_KEY")
pattern_data = extractor.process_pdf("amigurumi_bear.pdf")
# Returns: {name, structure, yarn_weight, composition, hook_size, ...}
```

### Example 2: Query Database
```python
from query_agent import PatternQueryAgent

agent = PatternQueryAgent(database_path="yarn_database.xlsx")
results = agent.query("Find cotton yarns for a beginner amigurumi pattern")
# Returns: Ranked list of suitable yarns with explanations
```

---

## Future Enhancements
- [ ] Add image recognition for pattern diagrams
- [ ] Support for video pattern extraction (YouTube tutorials)
- [ ] Multi-language pattern support
- [ ] Community pattern sharing integration
- [ ] Cost calculator for complete projects
- [ ] Yarn substitution suggestions
- [ ] Pattern difficulty re-assessment based on user feedback

---

**Last Updated**: October 28, 2025  
**Version**: 1.0  
**Maintained by**: Anna R.
