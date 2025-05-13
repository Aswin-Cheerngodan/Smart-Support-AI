import logging
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from src.core.state import SupportState, initialize_state
from src.agents.categorizer import categorizer
from src.agents.sentiment_agent import sentiment_analyzer
from src.agents.prioritizer import assign_priority
from src.agents.knowledge_agent import Knowledge_update
from src.agents.response_agent import generate_response
from src.agents.escalation import escalation_agent
from src.agents.ticket_raiser import ticket_agent
import yaml
from datetime import datetime
from src.utils.logger import setup_logger



# Load configuration
with open('config/config.yaml', 'r') as file :
    config = yaml.safe_load(file)


logger = setup_logger(__name__, "logs/app.log")


def setup_workflow() -> StateGraph:
    """
    Build and return the LangGraph workflow for the customer support system.
    
    Returns:
        StateGraph: Compiled workflow with all nodes and edges.
    """
    workflow = StateGraph(SupportState)

    # Add nodes (Agents)
    workflow.add_node("categorizer", categorizer)
    workflow.add_node("sentiment_analyzer", sentiment_analyzer)
    workflow.add_node("prioritizer", assign_priority)
    workflow.add_node("knowledge", Knowledge_update)
    workflow.add_node("response_generator", generate_response)
    workflow.add_node("escalation", escalation_agent)
    workflow.add_node("ticket_creator", ticket_agent)

    # Define edges (sequential flow)
    workflow.set_entry_point("categorizer")
    workflow.add_edge("categorizer", "sentiment_analyzer")
    workflow.add_edge("sentiment_analyzer", "prioritizer")
    workflow.add_edge("prioritizer", "knowledge")
    workflow.add_edge("knowledge", "response_generator")
    workflow.add_edge("response_generator", "escalation")

    def escalation_router(state : SupportState) -> str:
        """Route based on escalation status."""
        if state["escalate"]:
            logger.info(f"Escalating query: {state['query']}")
            return "ticket_creator"
        
        logger.info(f"Non-escalated query: {state['query']}")
        return END
    
    workflow.add_conditional_edges("escalation", escalation_router, 
                                   {"ticket_creator":"ticket_creator", END:END})

    # Final edges
    workflow.add_edge("ticket_creator", END)
    _workflow_cache = workflow
    logger.info("Workflow initialized and cached")
    return workflow


async def run_workflow(query: str) -> Dict[str, Any]:
    """
    Execute the workflow for a given query.
    
    Args:
        query (str): Customer query to process.
    
    Returns:
        Dict[str, Any]: Final state after processing.
    """
    try:
        workflow = setup_workflow()
        app = workflow.compile()
        initial_state = initialize_state(query)
        logger.info(f"Workflow started with query: {query}")
        result = await app.ainvoke(initial_state)
        logger.info(f"Workflow completed for query: {query}")
        return result
    except Exception as e:
        logger.error(f"Workflow failed for query '{query}': {str(e)}", exc_info=True)
        return {
            "query": query,
            "category": "",
            "sentiment": "",
            "priority": "",
            "kb_answer": "",
            "top_similarity_score":0,
            "response": "An error occurred. Please try again.",
            "escalate": False,
            "message": "Workflow failed",
            "ticket_id": "",
            "timestamp": datetime.now().astimezone().isoformat()
        }

