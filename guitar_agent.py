from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory, VectorStoreRetrieverMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import json
import os
from dotenv import load_dotenv
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime

# Load environment variables
load_dotenv()

class GuitarRecommendationAgent:
    def __init__(self):
        # Initialize LLM and embeddings
        self.llm = OpenAI(temperature=0.7)
        self.embeddings = OpenAIEmbeddings()
        
        # Initialize vector store for RAG
        self.vector_store = self._init_vector_store()
        
        # Initialize memory with vector store
        self.memory = VectorStoreRetrieverMemory(
            retriever=self.vector_store.as_retriever(),
            memory_key="chat_history",
            return_docs=True
        )
        
        # Initialize tools
        self.tools = self._create_tools()
        
        # Initialize agent with MCP
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent="conversational-react-description",
            memory=self.memory,
            verbose=True
        )
    
    def _init_vector_store(self) -> Chroma:
        """Initialize and load guitar product data into vector store"""
        # Load guitar product data
        guitars = [
            {
                "id": "GTR001",
                "name": "Fender Stratocaster",
                "brand": "Fender",
                "price": 1299.99,
                "type": "Electric",
                "features": ["Single-coil pickups", "Tremolo bridge", "Maple neck"],
                "description": "Classic electric guitar with versatile sound and iconic design."
            },
            {
                "id": "GTR002",
                "name": "Gibson Les Paul",
                "brand": "Gibson",
                "price": 1699.99,
                "type": "Electric",
                "features": ["Humbucker pickups", "Mahogany body", "Rosewood fretboard"],
                "description": "Premium electric guitar with rich, warm tone and excellent sustain."
            },
            # Add more guitars as needed
        ]
        
        # Convert to DataFrame for vector store
        df = pd.DataFrame(guitars)
        
        # Create vector store
        vector_store = Chroma(
            collection_name="guitar_products",
            embedding_function=self.embeddings
        )
        
        # Add guitar data to vector store
        for _, row in df.iterrows():
            vector_store.add_texts(
                texts=[row['description']],
                metadatas=[{
                    "id": row['id'],
                    "name": row['name'],
                    "brand": row['brand'],
                    "price": row['price'],
                    "type": row['type'],
                    "features": row['features']
                }]
            )
        
        return vector_store

    def _create_tools(self):
        tools = [
            Tool(
                name="ProductSearch",
                func=self._search_products,
                description="Use this tool to search for guitars based on user preferences. Input should be a JSON object containing search parameters."
            ),
            Tool(
                name="RecommendationEngine",
                func=self._recommend_products,
                description="Use this tool to generate personalized guitar recommendations based on user preferences and search results."
            )
        ]
        return tools

    def _search_products(self, query: str):
        """Search products using RAG approach"""
        try:
            search_params = json.loads(query)
            
            # Find relevant products using vector search
            docs = self.vector_store.similarity_search(
                query,
                k=5  # Return top 5 most relevant products
            )
            
            # Format results
            results = []
            for doc in docs:
                metadata = doc.metadata
                results.append({
                    "id": metadata['id'],
                    "name": metadata['name'],
                    "brand": metadata['brand'],
                    "price": metadata['price'],
                    "type": metadata['type'],
                    "features": metadata['features']
                })
            
            return json.dumps(results)
        except Exception as e:
            return f"Error searching products: {str(e)}"

    def _recommend_products(self, query: str):
        """Generate personalized recommendations using RAG and context"""
        try:
            user_prefs = json.loads(query)
            
            # Get relevant products using RAG
            docs = self.vector_store.similarity_search(
                json.dumps(user_prefs),
                k=3  # Get top 3 most relevant products for recommendations
            )
            
            # Format context for LLM
            context = "\n".join([
                f"Product: {doc.metadata['name']} ({doc.metadata['brand']})\n"
                f"Type: {doc.metadata['type']}\n"
                f"Price: ${doc.metadata['price']}\n"
                f"Features: {', '.join(doc.metadata['features'])}\n"
                f"Description: {doc.page_content}\n"
                for doc in docs
            ])
            
            # Use LLM to generate personalized recommendations with context
            template = """Based on the user preferences: {preferences}, 
            and considering the following guitar products:
            {context}
            
            Provide personalized recommendations for the user. Consider factors like:
            - User's budget constraints
            - Preferred guitar type
            - Preferred features
            - Brand preferences
            - Price range
            
            Format your response as a JSON object with the following structure:
            {
                "recommendations": [
                    {
                        "product_id": "",
                        "reason": "",
                        "score": ""
                    }
                ]
            }"""
            
            prompt = PromptTemplate(
                input_variables=["preferences", "context"],
                template=template
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            return chain.run(
                preferences=user_prefs,
                context=context
            )
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"

    def run_agent(self, user_input: str):
        """Run the agent with user input"""
        try:
            response = self.agent.run(user_input)
            return response
        except Exception as e:
            return f"Error processing request: {str(e)}"

# Example usage
def main():
    agent = GuitarRecommendationAgent()
    
    # Example conversation
    print("\nStarting guitar recommendation chatbot...")
    print("Type 'quit' to exit")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
            
        response = agent.run_agent(user_input)
        print(f"\nAgent: {response}")

if __name__ == "__main__":
    main()
