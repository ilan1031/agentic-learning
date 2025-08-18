
# JSON Data Validation System

AI-powered JSON validation system using CrewAI multi-agent architecture with Gemini 1.5 Flash.

## Features

- **Multi-agent Validation**:
  - Manager Agent: Oversees validation process
  - Data Analyzer: Identifies syntax and schema errors
  - Data Corrector: Fixes errors and produces valid JSON
- **Comprehensive Validation**:
  - Syntax checking
  - Schema validation
  - Detailed error reporting
  - Automatic correction
- **User-friendly Interface**:
  - JSON input with syntax highlighting
  - Template library
  - Detailed error reports
  - Corrected JSON output
- **Advanced Features**:
  - Error classification
  - Location detection
  - Suggested fixes
  - Schema enforcement

## How It Works

1. **Input**: User provides JSON string
2. **Analysis**:
   - Syntax validation
   - Schema checking
   - Error detection
3. **Correction**:
   - Automatic fixes
   - Data type conversion
   - Structure adjustment
4. **Output**:
   - Validation report
   - Corrected JSON
   - Raw validation data

## Setup Instructions

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set environment variables**:
Create a `.env` file with:
```env
GOOGLE_API_KEY=your_google_api_key
```

3. **Start services**:
```bash
# Start Flask backend
python app/flask_app.py

# Start Streamlit UI
streamlit run streamlit_app.py
```

4. **Access the UI**:
Open `http://localhost:8501` in your browser

## Usage

1. Enter JSON in the input area
2. Click "Analyze & Correct"
3. View results in tabs:
   - Validation Report: Detailed error information
   - Corrected JSON: Fixed JSON with syntax highlighting
   - Raw Output: Full validation results
4. Use templates for quick testing
```

## How to Run the Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Google API key:
```env
GOOGLE_API_KEY=your_google_api_key
```

3. Start the services in separate terminals:

**Terminal 1 (Flask Backend):**
```bash
python app/flask_app.py or python -m app.flask_app
```

**Terminal 2 (Streamlit UI):**
```bash
streamlit run streamlit_app.py
```

## Features of the Streamlit UI

1. **Professional Dashboard**:
   - Modern header with gradient background
   - Card-based layout for results
   - Consistent color scheme

2. **JSON Input**:
   - Large text area for JSON input
   - Template library for quick testing
   - Auto-validate option

3. **Validation Workflow**:
   - Analyze Only button (for error detection)
   - Analyze & Correct button (full validation)
   - Processing status with steps

4. **Results Display**:
   - Tabbed interface for different views
   - Validation status cards (success/error)
   - Detailed error reports with classification
   - Syntax-highlighted JSON output
   - Raw data view

5. **Error Handling**:
   - Clear error messages
   - Error classification (syntax/schema)
   - Location detection (line, column, path)
   - Suggested fixes

6. **Additional Features**:
   - Download corrected JSON
   - Documentation section
   - Responsive layout

The UI provides a complete JSON validation solution with all necessary elements for inspecting and correcting JSON data. The design is clean, professional, and focused on the needs of developers working with JSON data.


Great question 👍

This kind of **JSON Data Validation System** has **real-world uses** wherever applications rely on exchanging or storing structured data.

Here’s **what it’s used for** and **where it helps**:

---

### 🔹 **What it’s used for**

* **Automatic Error Detection** → Finds mistakes in JSON files (missing commas, wrong types, schema mismatches).
* **Automatic Correction** → Fixes the errors instead of requiring manual debugging.
* **Data Quality Assurance** → Ensures JSON is valid and consistent before it’s consumed by applications or APIs.
* **Workflow Automation** → Saves time in pipelines where large volumes of JSON files need validation.

---

### 🔹 **Where it will be helpful**

1. **APIs & Web Services**

   * APIs often send/receive JSON.
   * If a client sends broken JSON, this system can auto-correct before processing.
   * Ensures smoother **API communication** without crashes.

2. **Data Pipelines & ETL (Extract, Transform, Load)**

   * When integrating data from multiple sources, JSON files may have formatting issues.
   * This system can **validate and correct incoming data** before loading it into databases.

3. **Configuration Files**

   * Many applications (Node.js, Docker, VSCode, etc.) use JSON configs.
   * A corrupted config file can break apps → this system ensures configs are always valid.

4. **Database Imports/Exports**

   * JSON is widely used for exporting/importing data (e.g., MongoDB, Elasticsearch).
   * Helps ensure that **data migrations don’t fail** due to invalid JSON.

5. **Big Data & Machine Learning**

   * Datasets often come as JSON (logs, events, training data).
   * Validating/correcting JSON ensures clean input for models and analytics.

6. **Developer Tools**

   * Could be integrated into IDEs or CI/CD pipelines to automatically catch and fix JSON errors during development.

---

✅ **In short:**
This system is most useful anywhere **JSON is a critical data format** (APIs, configs, databases, data pipelines). It helps by **reducing manual debugging, preventing system crashes, and improving data quality**.



