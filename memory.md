# Memory Systems Documentation

## Overview
This document describes the memory and data storage systems used in the Crochet Pattern Management System. The system employs multiple types of memory to handle different aspects of pattern and yarn information.

---

## 1. Vector Database (Semantic Memory)

### Purpose
Stores embeddings of PDF pattern content for semantic search and similarity matching.

### Technology
- **Primary Option**: ChromaDB (lightweight, persistent, Python-native)
- **Alternative**: FAISS (faster for large datasets)
- **Embedding Model**: Gemini Pro embeddings or sentence-transformers

### What's Stored
- **Pattern Descriptions**: Full text content from PDFs
- **Pattern Instructions**: Step-by-step crochet instructions
- **Metadata**: Pattern name, difficulty, stitches, materials
- **Embeddings**: Vector representations of pattern content (768 or 1536 dimensions)

### Storage Format
```
Collection: "crochet_patterns"
├── Document 1
│   ├── embedding: [0.23, -0.45, 0.12, ...]
│   ├── metadata: {name, difficulty, yarn_weight, hook_size, ...}
│   └── content: "Full pattern text..."
├── Document 2
│   ├── embedding: [0.18, -0.33, 0.09, ...]
│   ├── metadata: {...}
│   └── content: "..."
...
```

### Use Cases
- **Semantic Search**: "Find patterns similar to this granny square blanket"
- **Pattern Discovery**: "Show me patterns that use popcorn stitches"
- **Fuzzy Matching**: Match variations in pattern descriptions
- **Recommendation**: "Patterns similar to ones you've made before"

### Persistence
- **Location**: `./chroma_db/` directory in project folder
- **Backup**: Weekly automatic backups
- **Size**: Approximately 1-5MB per 100 patterns
- **Indexing**: Automatic on new pattern addition

### Performance
- **Search Speed**: < 100ms for queries across 1000+ patterns
- **Memory Usage**: ~500MB RAM for 1000 patterns
- **Scalability**: Handles up to 10,000 patterns efficiently

---

## 2. Excel Database (Structured Memory)

### Purpose
Stores structured, tabular data about yarns and their properties for precise filtering and matching.

### File Structure
**File**: `yarn_database.xlsx`

#### Current Schema

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| Name of the product | Text | Yarn brand and product name | "Scheepjes Catona" |
| Price (€) | Float | Price per ball/skein | 2.50 |
| Cotton (%) | Integer | Percentage of cotton | 100 |
| Acrylic (%) | Integer | Percentage of acrylic | 0 |
| Wool (%) | Integer | Percentage of wool | 0 |
| Silk (%) | Integer | Percentage of silk | 0 |
| Bamboo/Viscose (%) | Integer | Percentage of bamboo/viscose | 0 |
| Linen (%) | Integer | Percentage of linen | 0 |
| Polyester (%) | Integer | Percentage of polyester | 0 |
| Nylon/Polyamide (%) | Integer | Percentage of nylon/polyamide | 0 |
| Mohair/Alpaca (%) | Integer | Percentage of mohair/alpaca | 0 |
| Reflective Yarn (%) | Integer | Percentage of reflective fibers | 0 |
| Yarn thickness | Text | Weight category | "Sport", "DK", "Worsted" |
| Rating (★) | Float | User/community rating (1-5) | 4.5 |
| Total ponderation | Float | Weighted score based on composition and properties | 8.2 |
| Season recommended | Text | Best season for projects | "Spring/Summer" |
| Washing recommendation | Text | Care instructions | "Machine wash 30°C" |

#### Planned Pattern Table
**File**: `pattern_database.xlsx`

| Column Name | Data Type | Description |
|------------|-----------|-------------|
| Pattern Name | Text | Name of the pattern |
| Source File | Text | Original PDF filename |
| Pattern Structure | Text | Construction method |
| Yarn Weight | Text | Required yarn weight |
| Recommended Composition | Text | Ideal fiber content |
| Hook Size (mm) | Float | Crochet hook size |
| Difficulty Level | Text | Skill level required |
| Materials Needed | Text | Complete materials list |
| Recommended Colors | Text | Color suggestions |
| Stitches Required | Text | List of stitches used |
| Date Added | Date | When pattern was added |
| Last Updated | Date | Last modification date |
| Notes | Text | Additional user notes |

### Query Methods
1. **Direct Filtering**: pandas queries (e.g., `df[df['Cotton (%)'] == 100]`)
2. **Range Queries**: Price ranges, rating thresholds
3. **Multi-criteria**: Combined filters across multiple columns
4. **Sorting**: By price, rating, composition match

### Backup & Versioning
- **Auto-save**: After each pattern addition
- **Version Control**: Daily snapshots in `./backups/`
- **Format**: `.xlsx` for editing, `.csv` for version control
- **Cloud Sync**: Compatible with OneDrive auto-sync

---

## 3. Conversation Memory (Short-term Memory)

### Purpose
Maintains context during chat sessions with the Query Agent for more natural conversations.

### Technology
- **Implementation**: In-memory Python list/dict
- **Optional Persistence**: JSON file for session recovery
- **LLM Context**: Passed to Gemini Pro with each query

### What's Stored
- **Recent Queries**: Last 10 user questions
- **Agent Responses**: Last 10 agent answers
- **Session Preferences**: Temporary filters (e.g., "only show budget options")
- **Current Context**: Active pattern or yarn being discussed

### Storage Format
```json
{
  "session_id": "uuid-string",
  "started_at": "2025-10-28T14:30:00",
  "conversation_history": [
    {
      "role": "user",
      "content": "What yarns work for baby blankets?",
      "timestamp": "2025-10-28T14:31:00"
    },
    {
      "role": "assistant",
      "content": "For baby blankets, I recommend...",
      "timestamp": "2025-10-28T14:31:05"
    }
  ],
  "active_filters": {
    "yarn_weight": "DK",
    "max_price": 5.00
  },
  "referenced_patterns": ["baby_blanket_01.pdf"],
  "referenced_yarns": ["Scheepjes Catona"]
}
```

### Retention Policy
- **Duration**: Until session ends or 1 hour of inactivity
- **Size Limit**: 50 conversation turns (auto-summarize older content)
- **Persistence**: Optional save for important sessions
- **Privacy**: No sensitive data stored

---

## 4. Cache Memory (Performance Optimization)

### Purpose
Speeds up repeated queries and reduces API calls to Gemini Pro.

### What's Cached
- **PDF Extractions**: Parsed PDF content (to avoid re-parsing)
- **Frequent Queries**: Common search results
- **Embeddings**: Vector representations (to avoid re-embedding)
- **Pattern Matches**: Pre-computed yarn-pattern compatibility scores

### Cache Strategy
- **Type**: LRU (Least Recently Used) cache
- **Size Limit**: 100 entries
- **TTL**: 24 hours for query results, permanent for PDF parses
- **Invalidation**: Manual clear or when database updates

### Storage
- **Location**: `./cache/` directory
- **Format**: Pickle files for Python objects
- **Management**: Automatic cleanup of expired entries

---

## Memory Interaction Diagram

```
User Query
    ↓
Conversation Memory (context)
    ↓
Query Agent
    ↓
    ├─→ Excel Database (structured data)
    │       ↓
    │   Filter yarns/patterns
    │
    └─→ Vector Database (semantic search)
            ↓
        Find similar patterns
            ↓
        Merge Results
            ↓
    Check Cache (if exists, return)
    ↓
    Generate Response
    ↓
    Update Conversation Memory
    ↓
    Store in Cache
    ↓
Return to User
```

---

## Data Flow Examples

### Example 1: Adding a New Pattern
```
PDF File → PDF Extraction Agent
    ↓
Extract text + metadata
    ↓
    ├─→ Vector Database (store embedding + content)
    └─→ Excel Database (add new row with structured data)
    ↓
Update Cache (invalidate related queries)
```

### Example 2: Querying for Yarn Recommendations
```
User: "What yarn for summer top pattern?"
    ↓
Conversation Memory (check context)
    ↓
Query Agent parses intent
    ↓
    ├─→ Vector DB: Find "summer top" patterns
    └─→ Excel DB: Filter yarns (cotton, linen, high breathability)
    ↓
Match yarn properties to pattern requirements
    ↓
Rank results by compatibility score
    ↓
Generate response + Update conversation memory
```

---

## Maintenance & Optimization

### Regular Tasks
- [ ] **Weekly**: Backup Excel and Vector DB
- [ ] **Monthly**: Rebuild vector database index
- [ ] **Quarterly**: Clean up cache directory
- [ ] **As-needed**: Re-embed patterns if embedding model changes

### Monitoring
- Track vector DB size and query performance
- Monitor API usage (Gemini Pro calls)
- Log cache hit rates
- Review conversation memory for common patterns

### Scalability Considerations
- **Current System**: Handles 100-500 patterns efficiently
- **Growth to 1,000**: May need to switch to FAISS
- **Growth to 5,000+**: Consider PostgreSQL for structured data
- **Long-term**: Cloud-based vector database (Pinecone, Weaviate)

---

**Last Updated**: October 28, 2025  
**Version**: 1.0  
**Maintained by**: Anna R.
