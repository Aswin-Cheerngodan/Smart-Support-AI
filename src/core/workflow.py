import logging
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from src.core.state import SupportState, initialize_state
from src.agents import (categorizer_agent,sentiment_agent, priority_agent, knowledge_agent,
                        response_agent, escalation_agent, ticket_agent, feedback_agent)
import yaml
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
    workflow.add_node("categorizer", categorizer_agent)
    workflow.add_node("sentiment", sentiment_agent)
    workflow.add_node("priority", priority_agent)
    workflow.add_node("knowledge", knowledge_agent)
    workflow.add_node("response", response_agent)
    workflow.add_node("escalation", escalation_agent)
    workflow.add_node("ticket", ticket_agent)
    workflow.add_node("feedback", feedback_agent)

    # Define edges (sequential flow)
    workflow.set_entry_point("categorizer")
    workflow.add_edge("categorizer", "sentiment")
    workflow.add_edge("sentiment", "priority")
    workflow.add_edge("priority", "knowledge")
    workflow.add_edge("knowledge", "response")
    workflow.add_edge("response", "escalation")

    def escalation_router(state : SupportState) -> str:
        """Route based on escalation status."""
        if state["escalate"]:
            logger.info(f"Escalating query: {state['query']}")
            return "ticket"
        
        logger.info(f"Non-escalated query: {state['query']}")
        return "feedback"
    
    workflow.add_conditional_edges("escalation", escalation_router, 
                                   {"ticket":"ticket", "feedback":"feedback"})

    # Final edges
    workflow.add_edge("ticket", "feedback")
    workflow.add_edge("feedback", END)

    return workflow


def run_workflow(query: str) -> Dict[str, Any]:
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
        result = app.invoke(initial_state)
        logger.info(f"Workflow completed for query: {query}")
        return result
    except Exception as e:
        logger.error(f"Workflow failed: {str(e)}")
        raise


if __name__ == "__main__":
    # Testing the workflow
    test_query = "My payement failed and I'm furious!"
    result = run_workflow(test_query)
    print(result)