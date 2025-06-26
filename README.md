# Guitar Recommendation AI Agent

A modern, context-aware AI chatbot for recommending guitars, built with FastAPI, RAG (Retrieval-Augmented Generation), and MCP (Model Context Protocol).

---

## 🚀 Overview
This project delivers personalized guitar recommendations by combining semantic search (RAG) and dynamic user context management (MCP). It’s ideal for e-commerce chatbots or digital assistants.

---

## 🏗️ Architecture
- **FastAPI Backend:** Handles API requests and responses
- **RAG System:**
  - **FAISS:** Vector store for semantic product search
  - **OpenAI Embeddings:** For understanding user queries and product descriptions
  - **LLM:** Generates natural language recommendations
- **MCP Context Manager:**
  - Tracks user preferences (e.g., style, budget, brand)
  - Updates context throughout the conversation

---

## ⚙️ How It Works
### 1. RAG (Retrieval-Augmented Generation)
- **User query:** "I want an electric guitar for rock, under $800."
- **Embedding:** Query and product descriptions are embedded
- **Retrieval:** FAISS finds the most relevant guitars
- **Generation:** LLM crafts a recommendation using the retrieved products

**Toy Example:**
- User: "Looking for a $600 acoustic Yamaha."
- System: Finds Yamaha acoustics under $600 and responds: "I recommend the Yamaha FG800, a great acoustic guitar within your budget."

### 2. MCP (Model Context Protocol)
- **Tracks conversation context:**
  - User: "I want an acoustic guitar." → `{style: "acoustic"}`
  - User: "My budget is $600." → `{style: "acoustic", budget: 600}`
  - User: "I prefer Yamaha." → `{style: "acoustic", budget: 600, brand: "Yamaha"}`
- **Always uses latest context for recommendations**

---

## ✨ Features
- Personalized guitar recommendations
- Remembers user preferences across conversation
- Semantic product search using embeddings
- RESTful API interface

---

## 🛠️ Setup
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up environment variables**
   - Create a `.env` file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
3. **Run the server**
   ```bash
   python main.py
   ```

---

## 🔗 Example API Usage
**POST /recommend**
```json
{
  "message": "I want a classical guitar under $700"
}
```
**Response:**
```
"I recommend the Yamaha C40II, a great classical guitar under $700."
```

---

## 🧩 Technology Stack
| Component | Technology | Purpose |
|-----------|------------|---------|
| Backend   | FastAPI    | API server |
| RAG       | FAISS, OpenAI Embeddings, LLM | Semantic search & generation |
| MCP       | Context Object/Class | Tracks user preferences |

---

## 📖 References
- See `main.py` for implementation of RAG and MCP logic
- Look for functions like `retrieve_similar_guitars()` and `UserContext`

---


# How RAG and MCP Work in This Project

This section explains how Retrieval-Augmented Generation (RAG) and Model Context Protocol (MCP) are implemented in the guitar recommendation AI agent, with a step-by-step toy example.

---

## RAG (Retrieval-Augmented Generation)

**What is RAG?**
- RAG combines information retrieval (fetching relevant data from a knowledge base) with language generation (using an LLM to generate responses).

### How RAG is Used Here
1. **User Input:** The user specifies their guitar preferences (e.g., "I want an acoustic guitar under $500").
2. **Embedding:** The system converts the query and all product descriptions into vector embeddings using OpenAI's embedding model.
3. **Retrieval:** FAISS is used to semantically search for the most relevant guitars in the product database.
4. **Generation:** The top results are passed to the LLM, which generates a personalized recommendation message.

#### Toy Example: RAG Flow
- **User:** "I am looking for an electric guitar for rock music, budget $800."
- **System:**
    1. Embeds the query and searches the vector store.
    2. Finds products like "Fender Player Stratocaster" and "Yamaha Pacifica".
    3. Passes these products to the LLM.
    4. LLM responds: "Based on your preferences, I recommend the Fender Player Stratocaster. It's great for rock and fits your budget."

---

## MCP (Model Context Protocol)

**What is MCP?**
- MCP manages conversation context (user preferences, history, etc.) in a structured way, allowing the agent to remember and use information across multiple interactions.

### How MCP is Used Here
1. **Context Tracking:** The agent stores user preferences (budget, style, brand, etc.) as the conversation progresses.
2. **Context Update:** Each new message updates the context (e.g., if the user changes their mind or adds a new preference).
3. **Context-Aware Recommendation:** The agent always uses the latest context to retrieve and generate the most relevant recommendations.

#### Toy Example: MCP Flow
- **User:** "I want an acoustic guitar."
    - MCP context: `{"style": "acoustic"}`
- **User:** "My budget is $600."
    - MCP context: `{"style": "acoustic", "budget": 600}`
- **User:** "I prefer Yamaha."
    - MCP context: `{"style": "acoustic", "budget": 600, "brand": "Yamaha"}`
- **System:** Uses this context to retrieve and recommend the best Yamaha acoustic guitars under $600.

---

## Code Reference
- **RAG Implementation:**
    - Look for functions using FAISS and OpenAI embeddings (e.g., `retrieve_similar_guitars()`)
    - LLM generation (e.g., `generate_recommendation()`)
- **MCP Implementation:**
    - Context object/class (e.g., `UserContext`)
    - Context update logic in the request/response cycle

---

## Summary Table
| Component | Technology | Purpose |
|-----------|------------|---------|
| RAG | FAISS, OpenAI Embeddings, LLM | Finds and explains best-fit guitars |
| MCP | Context Object/Class | Remembers user preferences |

---

## Example API Interaction

1. **POST /recommend**
    - Request: `{ "message": "I want a classical guitar under $700" }`
    - Response: `"I recommend the Yamaha C40II, a great classical guitar under $700."`

---
python main.py
```

## API Endpoints

- POST `/recommend/`: Get guitar recommendations
  - Request Body: GuitarPreferences model
  - Response: List of ProductRecommendation objects

## Example Usage

```python
import requests

preferences = {
    "budget": 2000,
    "style": "electric",
    "brand_preference": "Fender",
    "features": ["humbuckers", "tremolo"],
    "experience_level": "intermediate"
}

response = requests.post("http://localhost:8000/recommend/", json=preferences)
recommendations = response.json()
print(recommendations)
```

## Project Structure

- `main.py`: FastAPI application and recommendation logic
- `requirements.txt`: Project dependencies
- `README.md`: Project documentation
