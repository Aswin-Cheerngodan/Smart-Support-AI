from src.utils.logger import setup_logger
from src.core.state import SupportState

logger = setup_logger(__name__, log_file="logs/app.log")


def assign_priority(state: SupportState) -> SupportState:
    """
    Assigns a priority level to the customer query based on category and sentiment.
    """
    # Fetch the category and sentiment values
    category = state["category"]
    sentiment = state["sentiment"]
    logger.info(f"Category and sentiment")
    # Priority rules
    priority_rules = {
        "Login and Account": {
            "Very Negative": "High",
            "Negative": "High",
            "Neutral": "Medium",
            "Positive": "Low",
            "Very Positive": "Low",
        },
        "Order": {
            "Very Negative": "High",
            "Negative": "High",
            "Neutral": "Medium",
            "Positive": "Low",
            "Very Positive": "Low",
        },
        "Warranty": {
            "Very Negative": "High",
            "Negative": "High",
            "Neutral": "Medium",
            "Positive": "Low",
            "Very Positive": "Low",
        },
        "Cancellations and returns": {
            "Very Negative": "High",
            "Negative": "Medium",
            "Neutral": "Low",
            "Positive": "Low",
            "Very Positive": "Low",
        },
        "Shipping": {
            "Very Negative": "Medium",
            "Negative": "Medium",
            "Neutral": "Low",
            "Positive": "Low",
            "Very Positive": "Low",
        },
        "Shopping": {
            "Very Negative": "Medium",
            "Negative": "Medium",
            "Neutral": "Low",
            "Positive": "Low",
            "Very Positive": "Low",
        },
    }
    
    try:
    # Determine priority
        priority = priority_rules.get("Warranty").get("Very Negative")
        logger.info(f"Priority identified: {priority}")
    
    except Exception as e:
        logger.error(f"Failed priortiy identification: {str(e)}")
        state["priority"] = "None"
    
    # Update the state with the priority
    state["priority"] = priority
    return state
