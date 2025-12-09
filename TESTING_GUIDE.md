# 🧶 Tangled - Testing Guide

## ✅ All 10 Features Implemented!

Congratulations! All features are now complete and ready for testing.

---

## 🚀 Quick Start

**Your app is running at:** http://localhost:8508

**Last commits:**
- `c935c8c` - Added 5 features (Notes/Ratings, Price Tracker, Advanced Filters, Batch Processor)
- `9727f83` - Completed UI polish with updated homepage

---

## 📋 Pre-Testing Checklist

### 1. Install New Dependencies
```bash
conda activate crochet_rag
pip install plotly Pillow
```

### 2. Verify API Key
Check that `.env` file contains:
```
GEMINI_API_KEY=your_api_key_here
```

---

## 🧪 Feature Testing Guide

### 1. 🏠 **Homepage** (streamlit_app.py)
**What to test:**
- [ ] Feature boxes display correctly
- [ ] Navigation buttons work (Browse, Stash, Gallery)
- [ ] Stats show: 18+ Patterns, 102 Yarns, 10+ Locations, AI Powered
- [ ] Complete feature list visible in "Complete Feature Set" section
- [ ] All emojis render properly

**Navigation links:**
- Pattern Browser → pages/1__Pattern_Browser.py
- Yarn Inventory → pages/3_🧵_Yarn_Inventory.py
- Photo Gallery → pages/6_📸_Photo_Gallery.py

---

### 2. 🔍 **Pattern Browser** (pages/1__Pattern_Browser.py)
**What to test:**

**Basic Features:**
- [ ] Pattern cards display with images
- [ ] Filter by difficulty (Beginner, Easy, Intermediate, Advanced, Expert)
- [ ] Filter by yarn weight (Fingering, Sport, DK, Worsted, Bulky)
- [ ] Search by pattern name/description

**NEW: Advanced Filters:**
- [ ] **Season Filter**: Select Spring/Summer/Fall/Winter (multiselect)
  - Cotton patterns → Summer/Spring
  - Wool patterns → Winter/Fall
- [ ] **Project Type**: Clothing, Home Decor, Toys/Amigurumi, Accessories
  - Check pattern name matching works
- [ ] **Time Estimate**: Quick (<5h), Weekend (5-20h), Week (20-40h), Long-term (40+h)
  - Based on difficulty level
- [ ] **Color Complexity**: 1 Color, 2-3 Colors, 4+ Colors
  - Parses "Recommended Colors" field

**Expected behavior:**
- Filters should combine (AND logic)
- Search should work with filters active
- Pattern count updates as filters change

---

### 3. 🧵 **Yarn Inventory** (pages/3_🧵_Yarn_Inventory.py)
**What to test:**

**Add Yarn:**
- [ ] Click "Add New Yarn" expander
- [ ] Fill all fields: Name, Brand, Color, Weight, Fiber, Quantity, Grams/Skein, Location, Price
- [ ] Click "Add Yarn" button
- [ ] Verify yarn appears in inventory table
- [ ] Check Excel file created: `yarn_inventory.xlsx`

**Search & Filter:**
- [ ] Search by brand (multiselect dropdown)
- [ ] Filter by yarn weight (multiselect)
- [ ] Search bar (by name)

**Statistics:**
- [ ] Total yarns count
- [ ] Total skeins count
- [ ] Total weight in kg
- [ ] Total inventory value
- [ ] Chart: Yarns by Weight (bar chart)
- [ ] Chart: Yarns by Brand (bar chart)

**Low Stock Alerts:**
- [ ] Add yarn with 1 skein
- [ ] Check if alert appears (<2 skeins)

**Edit/Delete:**
- [ ] Click "Edit" on a yarn
- [ ] Modify fields and save
- [ ] Click "Delete" and confirm

---

### 4. 📝 **Project Tracker** (pages/4_📝_Project_Tracker.py)
**What to test:**

**Create Project:**
- [ ] Fill: Project Name, Pattern (dropdown from database), Yarns Used, Hook Size, Target Date, Status
- [ ] Click "Create Project"
- [ ] Verify project card appears
- [ ] Check Excel file: `projects.xlsx`

**Project Cards:**
- [ ] Status emoji displays (📅 Planned, 🚧 In Progress, ⏸️ On Hold, ✅ Completed, ❌ Abandoned)
- [ ] Progress bar shows 0%
- [ ] Days active calculation correct

**Quick Actions:**
- [ ] Click "Edit" → Modify project details
- [ ] Click "Delete" → Confirm deletion
- [ ] Update progress slider (0-100%)
- [ ] At 100% → Status should auto-change to "Completed"

**Statistics:**
- [ ] Total projects count
- [ ] In Progress count
- [ ] Completion rate (%)
- [ ] Average time per project
- [ ] Longest WIP project

**Project Statuses:**
- [ ] Try all 5 statuses: Planned, In Progress, On Hold, Completed, Abandoned

---

### 5. ⚖️ **Pattern Comparison** (pages/5_⚖️_Pattern_Comparison.py)
**What to test:**

**Compare Patterns:**
- [ ] Select 2-3 patterns from dropdown
- [ ] Click "Compare Patterns"
- [ ] Verify table shows: Pattern Name, Difficulty, Yarn Weight, Hook Size, Structure, Stitches, Est. Cost

**Insights:**
- [ ] "Easiest Pattern" detected correctly
- [ ] "Most Affordable" calculated from yarn database
- [ ] Pros/Cons analysis generated

**Cost Calculation:**
- [ ] Estimated cost based on yarn weight match
- [ ] Check if yarn prices pulled from `Database_YARN.xlsx`

**Decision Helper:**
- [ ] Click "Pick Random Pattern for Me!"
- [ ] Verify random selection from compared patterns

---

### 6. 📸 **Photo Gallery** (pages/6_📸_Photo_Gallery.py)
**What to test:**

**Upload Photo:**
- [ ] Click "Upload New Project Photo"
- [ ] Upload JPG/PNG image (any size)
- [ ] Fill: Pattern Name (dropdown), Project Name, Completion Date, Yarn Used, Hook Size, Caption, Tags, Rating
- [ ] Click "Upload Photo"
- [ ] Verify image appears in gallery
- [ ] Check file saved in: `project_photos/` directory (as JPEG, max 1200px width)
- [ ] Check Excel file: `project_gallery.xlsx`

**View Modes:**
- [ ] Grid View (3 columns) - cards with images
- [ ] List View - detailed table

**Search:**
- [ ] Search by project name
- [ ] Search by pattern name
- [ ] Search by tags (comma-separated)
- [ ] Search in caption

**Rating:**
- [ ] Verify 1-5 star rating displays
- [ ] Check if rating filter works

**Recent Photos:**
- [ ] Most recent photos appear at top

---

### 7. ⭐ **Pattern Notes & Ratings** (pages/7_⭐_Pattern_Notes.py)
**What to test:**

**Rate Pattern Tab:**
- [ ] Select pattern from dropdown
- [ ] Rate 1-5 stars
- [ ] Select difficulty vs listed (Much Easier → Much Harder)
- [ ] Check "Would Make Again?"
- [ ] Enter completion date
- [ ] Enter time taken (hours)
- [ ] Write review text
- [ ] Click "Save Rating"
- [ ] Check Excel file: `pattern_ratings.xlsx`
- [ ] Try to rate same pattern again → Should warn "already rated"

**Add Note Tab:**
- [ ] Select pattern
- [ ] Choose note type (General, Modification, Yarn Substitution, Hook Size Change, Tip)
- [ ] Enter note text
- [ ] Fill optional: Hook Size Used, Yarn Substitution, Modifications, Tips
- [ ] Click "Save Note"
- [ ] Check Excel file: `pattern_notes.xlsx`
- [ ] Add multiple notes to same pattern

**Overview Tab:**
- [ ] Total patterns rated
- [ ] Average rating
- [ ] Would-make-again percentage
- [ ] Top rated patterns list
- [ ] Difficulty feedback distribution chart
- [ ] Notes by type chart

---

### 8. 💰 **Price Tracker** (pages/8_💰_Price_Tracker.py)
**What to test:**

**Add Price Tab:**
- [ ] **Manual Entry**: Fill Yarn Name, Brand, Price, Date, Store, Link, Notes
- [ ] **Import from Database**: Select yarn from dropdown → Auto-fill Brand
- [ ] Click "Add Price Entry"
- [ ] Check Excel file: `yarn_price_history.xlsx`

**Price Trends Tab:**
- [ ] Select yarn from dropdown
- [ ] View interactive plotly line chart with:
  - Individual price points (markers)
  - Average price line
- [ ] Check metrics: Current Price, Average Price, Min Price, Max Price
- [ ] View price history table (Date, Store, Price, Notes)

**Sale Alerts Tab:**
- [ ] Adjust threshold slider (10-50%)
- [ ] View current sales (>20% below average)
- [ ] View price volatility analysis (yarns with most variation)
- [ ] Check if alerts appear when price drops

**Plotly Charts:**
- [ ] Hover over points → See details
- [ ] Zoom in/out
- [ ] Pan chart
- [ ] Export chart (camera icon)

---

### 9. 📚 **Batch Pattern Processor** (pages/9_📚_Add_Patterns.py)
**What to test:**

**IMPORTANT**: This feature uses Gemini API - ensure `.env` file has valid `GEMINI_API_KEY`

**Preview Tab:**
- [ ] Select PDF from `PDFPatterns/` directory
- [ ] Click "Preview Text"
- [ ] View extracted text (first 5 pages, 3000 chars)
- [ ] Click "Extract with AI"
- [ ] Verify JSON output with 9 fields:
  - Pattern Name, Pattern Structure, Yarn Weight, Recommended Yarn Composition
  - Hook Size, Difficulty Level, Materials Needed, Recommended Colors, Stitches Required

**Batch Process Tab:**
- [ ] Click "Process All Unprocessed PDFs"
  - Should show PDFs not yet in `pattern_database.xlsx`
- [ ] OR manually select specific files
- [ ] Click "Start Processing"
- [ ] Watch progress bar (20 PDFs total)
- [ ] View status messages per file
- [ ] Check error collection at end
- [ ] Verify patterns added to `pattern_database.xlsx`

**Database View Tab:**
- [ ] View all patterns in database
- [ ] Search by pattern name
- [ ] Sort by: Pattern Name, Difficulty, Yarn Weight, Date Added
- [ ] Export to CSV
- [ ] Click "Reload Database" to refresh
- [ ] **WARNING**: "Clear All Database" deletes all patterns

**Expected AI Extraction:**
- Accuracy: 80-90% (may need manual review)
- Missing fields: Marked as "Not specified" or empty
- Errors: Continue processing, collect at end

---

### 10. 🎨 **UI/Design Polish**
**What to test:**

**Homepage:**
- [ ] Hero section gradient background
- [ ] Stats boxes (4 columns)
- [ ] 3 main feature boxes with navigation buttons
- [ ] "Complete Feature Set" section (3 columns, 12 features listed)
- [ ] "How It Works" section (4 steps)
- [ ] CTA button "Start Now"
- [ ] Footer with Tangled branding

**Consistent Elements Across Pages:**
- [ ] Pink accent color (#E8819C) on buttons
- [ ] Emoji navigation in sidebar
- [ ] Responsive layout (3 columns → 1 on mobile)
- [ ] Loading spinners for slow operations
- [ ] Success/error messages with st.success/st.error

**Mobile Responsiveness:**
- [ ] Test on small screen (resize browser)
- [ ] Columns should stack vertically
- [ ] Buttons should be tappable
- [ ] Text should be readable

---

## 🐛 Known Issues & Limitations

### Potential Issues:
1. **Plotly not installed**: Run `pip install plotly`
2. **Pillow not installed**: Run `pip install Pillow`
3. **Gemini API key missing**: Check `.env` file
4. **Excel files locked**: Close Excel if files are open
5. **Image upload fails**: Check `project_photos/` directory exists and is writable
6. **Streamlit Cloud deployment**: Main file path must be `streamlit_app.py`

### Design Limitations:
- Advanced filters may show no results if criteria too restrictive
- AI extraction accuracy depends on PDF quality (scanned vs text-based)
- Price charts require at least 2 price entries
- Project photos stored locally (not cloud storage)

---

## 📊 Expected Test Results

**After full testing, you should have:**
- ✅ 7 Excel files created:
  - `yarn_inventory.xlsx`
  - `projects.xlsx`
  - `pattern_ratings.xlsx`
  - `pattern_notes.xlsx`
  - `yarn_price_history.xlsx`
  - `project_gallery.xlsx`
  - `pattern_database.xlsx` (updated with AI-extracted patterns)
- ✅ Photos in `project_photos/` directory
- ✅ All 9 page navigation items in sidebar
- ✅ No Python errors in terminal

---

## 🔄 Next Steps After Testing

1. **Document Issues**: Note any bugs or unexpected behavior
2. **Request Adjustments**: Share feedback on UI/UX improvements
3. **Deploy to Streamlit Cloud**: 
   - Go to Streamlit Cloud dashboard
   - Update main file path to `streamlit_app.py`
   - Add `GEMINI_API_KEY` to Secrets
   - Redeploy
4. **Optional Enhancements**:
   - Add more patterns (batch process remaining PDFs)
   - Customize color scheme
   - Add more chart types
   - Implement pattern favoriting

---

## 💡 Testing Tips

- **Start Simple**: Test one feature at a time
- **Check Excel Files**: Open files after operations to verify data structure
- **Use Real Data**: Add actual yarns/projects for realistic testing
- **Test Edge Cases**: Empty fields, very long text, special characters
- **Browser DevTools**: Open Console (F12) to see JavaScript errors
- **Streamlit Rerun**: Click "Always rerun" for faster testing

---

## 🎉 Congratulations!

You now have a fully-featured crochet pattern management system with:
- 📚 Pattern browsing & comparison
- 🧵 Yarn inventory & price tracking
- 📝 Project tracking with progress
- 📸 Photo gallery with ratings
- ⭐ Pattern notes & reviews
- 🤖 AI-powered PDF extraction

**Happy Crocheting! 🧶✨**
