from google import genai
import os
from dotenv import load_dotenv
from src.core.state import SupportState

from src.utils.logger import setup_logger


logger = setup_logger(__name__, "logs/app.log")

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)



def generate_response(state: SupportState) -> SupportState:
    """
    Generates a response using Gemini based on the user's query and past conversations.
    """
    try:
        # Extract values from state
        query = state['query']
        past_conversations = state['kb_answer']
        
        # Prepare the past conversations as formatted text
        formatted_conversations = ""
        for i in range(len(past_conversations)):
            conversation = past_conversations[i]
            formatted_conversations += f"This is {i}th conversation with similarity score {conversation[1]} with the query {query} similar conversation from the knowledge base \n {conversation[0]}\n\n"
        
        # Define the prompt template
        prompt_template = f"""
        You are an AI assistant helping a customer support agent. Your task is to analyze the user's query
        and generate a new useful response for the current user based on the following information:

        User Query:

        {query}

        Past Conversations from the knowledge base:

        {formatted_conversations}

        Instructions:
        "Consider every query as new and do not continue the past conversations. "
        "Respond concisely and politely, using the provided knowledge base answer if relevant. "
        "give the complete steps to follow to resolve the issue based on past conversations do not wait for anything. "
        "Consider the query category and conversation history for context. "
        "You don't need to ask for any other details. " 
        "If you can't get the proper answer, human agents are waiting . "
        "If the knowledge base answer is insufficient, provide a helpful response based on general knowledge. "
        "Keep responses under 200 words."

        Generated Response:
        """
        
        # Generate the response using Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt_template)
        generated_response = response.text
        
        # Log the generated response
        logger.info(f"Generated Response: {generated_response}")
        
        # Update the state with the generated response
        state["response"] = str(generated_response)
        return state
    except Exception as e:
        logger.error(f"Error generating response for '{query}': {e}")
        state["response"] = "I'm sorry, I encountered an issue. Please try again or contact support."
        return state


