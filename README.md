# Mysoft RAG Chatbot

A sophisticated Retrieval-Augmented Generation (RAG) based chatbot system built for **Mysoft Heaven (BD) Ltd.** This intelligent chatbot leverages LangGraph workflow orchestration, Groq LLM, and FAISS vector storage to provide accurate, context-aware responses based on company-specific data.

## 🚀 Features

- **RAG Architecture**: Combines retrieval from company documents with LLM generation for accurate responses
- **Multi-Source Data Integration**: Processes both PDF documents and web-scraped content
- **Conversational Memory**: Maintains chat history using LangGraph's checkpointing system
- **FastAPI Backend**: RESTful API with CORS support for easy integration
- **Session Management**: Unique session and user ID tracking for personalized conversations
- **Intelligent Document Processing**: Automated text cleaning and chunking for optimal retrieval
- **Confidence-Based Responses**: Configurable similarity thresholds for answer quality

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   FastAPI App   │────▶│  Chat Endpoints │────▶│   InitChat      │
│   (app.py)      │     │  (chat_endpoints)│     │   (chat.py)     │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                              ┌────────────────────────┼────────────────────────┐
                              │                        │                        │
                              ▼                        ▼                        ▼
                    ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
                    │  GraphBuilder   │      │  MemorySaver    │      │   Groq LLM    │
                    │   (graph.py)    │      │ (checkpointer)  │      │  (groq_llm.py)│
                    └────────┬────────┘      └─────────────────┘      └─────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  ChatBotNode    │
                    │   (node.py)     │
                    │  RAG + LLM      │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
      │  Retriever  │ │   FAISS     │ │  Preprocess │
      │ (retriever) │ │Vector Store │ │   (PDF/Web) │
      └─────────────┘ └─────────────┘ └─────────────┘
```

## 📁 Project Structure

```
mysoft-rag/
├── app.py                          # FastAPI application entry point
├── config/
│   └── config.yaml                 # Configuration settings
├── src/mysoft_rag/
│   ├── __init__.py
│   ├── config.py                   # Configuration loader
│   ├── api/
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       └── chat_endpoints.py   # API route definitions
│   ├── data/
│   │   └── Mysoftheaven-Profile_2026.pdf  # Company profile PDF
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schema.py               # Pydantic models
│   ├── services/
│   │   └── chatbot/
│   │       ├── __init__.py
│   │       ├── chat.py             # Chat initialization & orchestration
│   │       ├── graph.py            # LangGraph workflow builder
│   │       ├── node.py             # RAG node implementation
│   │       ├── groq_llm.py         # LLM & embedding initialization
│   │       ├── retriever.py        # Vector store retriever
│   │       ├── state.py            # Graph state definitions
│   │       ├── preprocess_data.py  # PDF & web data processing
│   │       └── vector_store_data.py # Vector store creation
│   └── utils/
│       ├── __init__.py
│       ├── helper.py               # Utility functions
│       ├── logger.py               # Logging configuration
│       └── prompt.py               # System prompts
├── vector_database/                # FAISS vector store files
├── logs/                          # Application logs
├── research/                      # Research notebooks
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project metadata
└── README.md                      # This file
```

## 🛠️ Technology Stack

- **Framework**: FastAPI + Uvicorn
- **Workflow Engine**: LangGraph
- **LLM**: Groq (llama-3.3-70b-versatile)
- **Embeddings**: HuggingFace (sentence-transformers/all-MiniLM-L6-v2)
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Document Processing**: Docling (PDF), WebBaseLoader (Web scraping)
- **Configuration**: Pydantic Settings + YAML
- **Python**: 3.13+

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or higher
- Groq API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mysoft-rag
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # OR using uv
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

4. **Build vector database** (first time setup)
   ```bash
   # Start the application first
   python app.py
   
   # Then call the vector initialization endpoint
   curl -X POST http://localhost:8000/init_vector
   ```
   Or use the API endpoint directly:
   ```http
   POST /init_vector
   ```
   Response:
   ```json
   {
     "Response": "Data Vectorize Successful"
   }
   ```

5. **Run the application** (if not already running)

   ```bash
   python app.py
   # OR
   uvicorn app:app --host localhost --port 8000 --reload
   ```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints
### Initialize Vector Database
```http
POST /init_vector
```
This endpoint processes all PDF and web data, creates embeddings, and builds the FAISS vector store.

Response:
```json
{
  "Response": "Data Vectorize Successful"
}
```

**Note**: Call this once when setting up the system or when you need to refresh the vector database with new data.

### Chat Endpoint
```http
POST /chat
Content-Type: application/json

{
  "messages": "What services does Mysoft Heaven offer?",
  "user_id": "user123",
  "session_id": "session456"
}
```

Response:
```json
{
  "messages": "Mysoft Heaven offers various services including...",
  "session_id": "session456"
}
```

**Note**: If `session_id` is not provided, a new UUID will be generated automatically.


## 🧠 How It Works

1. **Data Ingestion**: 
   - PDF documents are processed using Docling
   - Website content is scraped using WebBaseLoader
   - Text is cleaned and structured into Document objects

2. **Vectorization**:
   - Documents are split into chunks (1000 chars, 150 overlap)
   - HuggingFace embeddings convert text to vectors
   - FAISS stores vectors for efficient similarity search

3. **Query Processing**:
   - User query is received via FastAPI endpoint
   - Query is embedded using the same embedding model
   - FAISS retrieves top-5 most similar document chunks

4. **Response Generation**:
   - Retrieved context + chat history + query are sent to Groq LLM
   - LLM generates context-aware response
   - Response is returned to user with session tracking

5. **Memory Management**:
   - LangGraph's MemorySaver maintains conversation state
   - Each user+session combination has isolated thread ID
   - Chat history is preserved across multiple turns

## 🔬 Technical Deep Dive

### Document Chunking Strategy

We use a smart approach to break down documents into manageable pieces:

**Why Chunking Matters:**
Imagine trying to find a specific sentence in a 100-page book versus a 1-page document. Smaller chunks make search faster and more accurate. But if chunks are too small, we lose context. If they're too big, we include irrelevant information.

**Our Approach - Recursive Character Text Splitter:**
- **Chunk Size**: 1000 characters (about 150-200 words)
  - This captures complete thoughts and paragraphs
  - Large enough to maintain context, small enough to stay focused
- **Chunk Overlap**: 150 characters
  - Creates a "bridge" between chunks so no information gets cut off mid-sentence
  - Ensures context flows naturally from one chunk to the next

**Example:**
```
Original Text: "Mysoft Heaven offers web development services. 
They specialize in React and Python. Their team has 10+ years experience..."

Chunk 1: "Mysoft Heaven offers web development services. They specialize in React and Python. Their team has..."
Chunk 2: "Their team has 10+ years experience. They also offer mobile app development..."
```
Notice how "Their team has" appears in both chunks? That's the overlap keeping context intact.

### Embedding Model Choice

**Why We Chose `sentence-transformers/all-MiniLM-L6-v2`:**

Think of embeddings like "fingerprints" for text. They convert sentences into numbers that capture meaning. Similar sentences get similar numbers.

**What Makes This Model Special:**

1. **Lightning Fast**: It's small and efficient (only 22MB)
   - Processes text in milliseconds
   - Perfect for real-time chat responses

2. **High Quality**: Despite being small, it understands context well
   - Trained on millions of sentence pairs
   - Understands that "web development" and "website building" mean the same thing

3. **Multilingual Support**: Handles English beautifully (our primary language)
   - Also works with other languages if needed in the future

4. **Perfect for Semantic Search**: 
   - User asks: "Who is the CEO?"
   - System finds: "CEO Message from John Doe..."
   - Even though the words don't match exactly, the meaning connects

**Comparison with Alternatives:**
- **OpenAI Embeddings**: More powerful but expensive and requires API calls
- **Larger Models**: Better accuracy but 10x slower and memory-heavy
- **Our Choice**: Sweet spot of speed, quality, and cost (completely free!)

### Handling Irrelevant or Unsupported Queries

**The Challenge:**
Users might ask anything - "What's the weather?" or "Tell me about NASA" - but our bot only knows about Mysoft Heaven. We need graceful ways to handle this.

**Our Three-Layer Defense:**

**Layer 1: Smart System Prompt**
Our system prompt explicitly tells the AI:
```
"You are a professional AI assistant for Mysoft Heaven (BD) Ltd.
Answer only questions related to Mysoft Heaven using the provided context.
Do not answer irrelevant or off-topic questions. Politely reply:
'I can only provide information related to Mysoft Heaven (BD) Ltd.'"
```

**Layer 2: Context-Only Responses**
The RAG system only feeds Mysoft Heaven documents to the LLM. Even if someone asks about NASA, the AI only sees Mysoft Heaven info in its context window. This naturally limits responses to company topics.

**Layer 3: Confidence Scoring (Ready for Implementation)**
We have built-in support for similarity score checking:
```python
# This code is ready to activate when needed:
docs_and_scores = vector_store.similarity_search_with_score(query)
_, top_score = docs_and_scores[0]

if top_score < CONFIDENCE_THRESHOLD:
    return "I'm not confident about that. Could you clarify or ask about Mysoft Heaven?"
```

**Real Examples:**
- ❌ "What's the capital of France?" → "I can only provide information related to Mysoft Heaven (BD) Ltd."
- ❌ "How do I cook pasta?" → "I can only provide information related to Mysoft Heaven (BD) Ltd."
- ✅ "What services does Mysoft offer?" → Detailed answer about web development, ML, etc.
- ✅ "Tell me about the CEO" → Information from CEO message page

### Supporting Multiple Companies in the Future

**The Vision:**
Right now, this chatbot serves Mysoft Heaven. But the architecture is designed to easily support multiple companies without rebuilding everything.

**How We'd Scale:**

**Option 1: Multi-Tenant Architecture (Recommended)**
```
Company A (Mysoft Heaven) → Vector DB A + Config A + Prompt A
Company B (TechCorp)     → Vector DB B + Config B + Prompt B
Company C (StartupX)     → Vector DB C + Config C + Prompt C
```

**Implementation Steps:**
1. **Separate Vector Stores**: Each company gets their own FAISS database folder
   - `vector_database/mysoft_heaven/`
   - `vector_database/techcorp/`
   - `vector_database/startupx/`

2. **Dynamic Configuration**: Pass company ID in API request
   ```json
   {
     "messages": "What are your services?",
     "user_id": "user123",
     "session_id": "session456",
     "company_id": "techcorp"
   }
   ```

3. **Company-Specific Prompts**: Each company gets tailored system instructions
   - Mysoft: "You are Mysoft Heaven's AI assistant..."
   - TechCorp: "You are TechCorp's support bot..."

4. **Shared Infrastructure**: Same FastAPI server, same LLM, same embedding model
   - Cost-efficient: One server handles many clients
   - Easy maintenance: Update once, deploy everywhere

**Option 2: White-Label Solution**
Create a template where new companies just provide:
- Their PDF documents
- Their website URLs
- Their custom prompt instructions
- Logo and branding colors

The system automatically:
- Scrapes their data
- Builds their vector store
- Deploys their branded chatbot

**Current Architecture Advantages:**
- Modular design makes swapping components easy
- Configuration-driven (YAML files) - no code changes needed
- Document processing pipeline is company-agnostic
- Same embedding model works for any company text

### Conversation Memory Explained

**What is Conversation Memory?**
Imagine talking to a friend who forgets what you said 30 seconds ago. Frustrating, right? Memory lets our chatbot remember the full conversation context.

**How It Works:**

**The Problem Without Memory:**
```
User: "What services do you offer?"
Bot: "We offer web development, mobile apps, and ML solutions."

User: "How much does the first one cost?"
Bot: "What do you mean by 'first one'?" ❌
```

**The Solution With Memory:**
```
User: "What services do you offer?"
Bot: "We offer web development, mobile apps, and ML solutions."

User: "How much does the first one cost?"
Bot: "Web development pricing depends on project scope..." ✅
```

**Technical Implementation:**

**1. Thread ID System**
Every conversation gets a unique ID combining user ID + session ID:
```python
full_id = f"{user_id}_{session_id}"
# Example: "alice_123e4567-e89b-12d3-a456-426614174000"
```

**2. LangGraph MemorySaver**
- Stores conversation history in memory
- Persists across multiple API calls
- Automatically retrieves previous messages when processing new ones

**3. Chat History in Prompts**
The system prompt includes a placeholder for chat history:
```python
MessagesPlaceholder(variable_name="chat_history")
```

When processing, we inject the conversation so far:
```python
chat_history = [previous_message_1, previous_message_2, ...]
current_input = "How much does the first one cost?"
```

**4. Memory Benefits:**
- Follow-up questions work naturally
- Users can reference previous answers
- Context builds up over long conversations
- Each user has isolated memory (privacy!)

### Confidence-Based Responses & Fallback Messaging

**Why Confidence Matters:**
Not all retrieved documents are equally relevant. Sometimes the best match is still a poor match. We need to detect this and respond appropriately.

**How Confidence Scoring Works:**

**Step 1: Get Similarity Scores**
When we search the vector database, FAISS returns both documents AND similarity scores:
```python
docs_and_scores = vector_store.similarity_search_with_score("query")
# Returns: [(doc1, 0.85), (doc2, 0.72), (doc3, 0.45)]
# Higher score = more similar
```

**Step 2: Set a Threshold**
We define what "confident" means:
```python
CONFIDENCE_THRESHOLD = 0.7  # 70% similarity or higher
```

**Step 3: Make a Decision**
```python
best_doc, best_score = docs_and_scores[0]

if best_score < CONFIDENCE_THRESHOLD:
    # Not confident - use fallback
    return "I'm not sure about that. Could you ask about Mysoft Heaven's services or products?"
else:
    # Confident - proceed with RAG
    return generate_response(best_doc)
```

**Fallback Strategies:**

**Strategy 1: Polite Deflection (Currently Active)**
```
User: "What's the weather in Tokyo?"
Bot: "I can only provide information related to Mysoft Heaven (BD) Ltd."
```

**Strategy 2: Clarification Request (Ready to Implement)**
```
User: "Tell me about development"
Bot: "I found some information, but I'm not completely sure what you're looking for. 
      Are you asking about web development services or software development careers at Mysoft Heaven?"
```

**Strategy 3: Suggest Related Topics (Ready to Implement)**
```
User: "Do you make apps?"
Bot: "I don't have specific information about 'apps', but Mysoft Heaven offers:
      - Mobile Application Development
      - Web Application Development
      
      Would you like to know more about either of these?"
```

**Real-World Scenarios:**

| User Query | Best Match Score | Action | Response |
|------------|------------------|--------|----------|
| "What is Mysoft's address?" | 0.92 | ✅ Answer | "Mysoft Heaven is located at..." |
| "Who is the CEO?" | 0.88 | ✅ Answer | "The CEO is..." |
| "Tell me about their cloud services" | 0.65 | ⚠️ Low Confidence | "I found limited information. Mysoft offers web services. Would you like details about those?" |
| "What's 2+2?" | 0.12 | ❌ Reject | "I can only provide information related to Mysoft Heaven (BD) Ltd." |

**The Code is Ready:**
The confidence checking code exists in `node.py` (commented out). To activate it, simply uncomment and adjust the threshold:
```python
# In node.py, uncomment this section:
docs_and_scores = self.load_vectore_store.similarity_search_with_score(current_input)
_, top_score = docs_and_scores[0]
CONF_THRESHOLD = 0.7

if top_score < CONF_THRESHOLD:
    return {"messages": ["I'm not confident about that. Could you clarify or ask another question?"]}
```


## 📝 Logging

Logs are stored in `logs/system_logs.log` with the following information:
- Application startup/shutdown
- LLM initialization
- Vector database operations
- Chat requests and responses
- Error details

## 🔒 Security Considerations

- API key is stored in environment variables
- CORS is configured to allow all origins (customize for production)
- No sensitive data is logged
- Vector database uses safe deserialization
