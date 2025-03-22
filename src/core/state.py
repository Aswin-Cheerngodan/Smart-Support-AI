from typing import TypedDict, Optional
from datetime import datetime

class SupportState(TypedDict):
    """
    Typed dictionary representing the state of a customer support interaction.
    This state is shared and updated by all agents in the workflow.
    """
    query: str
    """The raw customer query input."""
    
    category: str
    """The classified category of the query (e.g., 'Billing', 'Technical')."""
    
    sentiment: str
    """The emotional tone of the query (e.g., 'Positive', 'Negative', 'Urgent')."""
    
    priority: str
    """Priority level assigned to the query (e.g., 'High', 'Medium', 'Low')."""
    
    kb_answer: Optional[str]
    """Answer retrieved from the knowledge base, if available."""
    
    response: str
    """Generated response to the customer."""
    
    escalate: bool
    """Flag indicating if the query requires human intervention."""
    
    ticket_id: Optional[str]
    """Unique ticket ID for escalated queries."""
    
    feedback_score: Optional[int]
    """Customer satisfaction score (1-5), if provided."""
    
    timestamp: str
    """ISO timestamp of when the query was processed."""


def initialize_state(query : str) -> SupportState:
    """
    Initialize a new SupportState with default values for a given query.
    
    Args:
        query (str): The customer's input query.
    
    Returns:
        SupportState: A new state instance with default values.
    """

    return SupportState(
        query=query,
        category="",
        sentiment="",
        priority="",
        kb_answer=None,
        response="",
        escalate=False,
        ticket_id=None,
        feedback_score=None,
        timestamp=datetime.utcnow().isoformat()
    )
