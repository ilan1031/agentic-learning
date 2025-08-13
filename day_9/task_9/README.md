# AI Product Recommendation System

This system provides intelligent product recommendations using AI agents. It combines real-time web research with product database information to deliver comprehensive recommendations.

## Features

- **Smart Query Routing**: Automatically determines the best approach for each query
- **Live Price Research**: Gets current pricing and availability from the web
- **Product Database**: Retrieves specifications from a curated product database
- **AI Summarization**: Combines information into concise recommendations
- **Conversation History**: Remembers previous queries and responses

## How It Works

1. **User Query**: The user enters a product-related question
2. **Routing Agent**: Determines the appropriate processing path
3. **Information Gathering**:
   - Web Research: For live pricing and reviews
   - RAG Search: For product specifications from database
4. **Summarization**: Combines information into a comprehensive response
5. **Presentation**: Displays results in an intuitive interface

## Setup Instructions

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set environment variables**:
Create a `.env` file with:
```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

3. **Start services**:
```bash
# Start LLM service
python app/llm_flask.py

# Start agent runner
python app/runner.py

# Start Streamlit UI
streamlit run streamlit_app.py
```

4. **Access the UI**:
Open `http://localhost:8501` in your browser

## Example Queries

- "Current price of iPhone 15"
- "Specs of MacBook Air M2"
- "Best laptops under $1000"
- "Compare iPhone 15 and Samsung Galaxy S24"
- "Top-rated wireless headphones"

## How to Run the Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:
```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
```

3. Start the services in separate terminals:

**Terminal 1 (LLM Service):**
```bash
python app/llm_flask.py
```

**Terminal 2 (Agent Runner):**
```bash
python app/runner.py
```

**Terminal 3 (Streamlit UI):**
```bash
streamlit run streamlit_app.py
```

## Features of the Streamlit UI

1. **Intuitive Interface**:
   - Clean, modern design with product-themed colors
   - Clear section organization
   - Responsive layout for all screen sizes

2. **Comprehensive Product Search**:
   - Category filters
   - Price range slider
   - Preference toggles
   - Multiple search modes (Search, Compare, Recommend)

3. **Results Presentation**:
   - Summary card with AI-generated recommendation
   - Detailed product specifications
   - Web research results with links
   - Visual distinction between different information types

4. **Conversation History**:
   - Persistent query history
   - Expandable previous responses
   - One-click history clearing

5. **User Feedback**:
   - Processing status with steps
   - Clear error messages
   - Visual indicators for different states

The UI provides a complete user experience with all necessary elements for product research and recommendation. Users can easily enter queries, filter results, view recommendations, and explore detailed product information.