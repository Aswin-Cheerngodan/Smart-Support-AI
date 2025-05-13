from src.core.state import SupportState
from src.utils.logger import setup_logger

logger = setup_logger(__name__, "logs/app.log")

def calculate_escalation_score(sentiment: str, priority: str, max_similarity: float) -> float:
    """Calculate an escalation score based on sentiment, priority, and similarity.
    
    Args:
        sentiment (str): Sentiment of the query.
        priority (str): Priority assigned to the query.
        max_similarity (float): Maximum similarity score got from the knowledge base.
    Returns:
        total_score (float): Total escalation score
    """
    # Sentiment weights
    sentiment_scores = {
        "Very Positive": -0.5,
        "Positive": -0.2,
        "Neutral": 0.0,
        "Negative": 0.7,
        "Very Negative": 1.0
    }
    
    # Priority weights
    priority_scores = {
        "Low": 0.0,
        "Medium": 0.5,
        "High": 1
    }

    similarity_score = 1-max_similarity

    # Calculate total score
    sentiment_weight = 0.4
    priority_weight = 0.3
    similarity_weight = 0.3
    try:
        total_score = (sentiment_scores.get(sentiment, 0.0) * sentiment_weight +
                    priority_scores.get(priority, 0.0) * priority_weight +
                    similarity_score * similarity_weight)
        
        logger.info(f"Escalation scores - Sentiment: {sentiment_scores.get(sentiment, 0.0)}, Priority: {priority_scores.get(priority, 0.0)}, Similarity: {similarity_score}, Total: {total_score}")
        return total_score
    except Exception as e:
        logger.error(f"Error while calculating the escalation score : {str(e)}")
        return 


def escalation_agent(state: SupportState) -> SupportState:
    """Escalate query to human agent based on weighted sentiment, priority, and similarity"""
    query = state['query']
    sentiment = state['sentiment']
    priority = state['priority']
    max_similarity = state['top_similarity_score']
    try:
        escalation_score = calculate_escalation_score(sentiment, priority, max_similarity)
        escalate = escalation_score > 0.7

        if escalate:
            logger.info(f"Escalating query '{query}' due to score {escalation_score:.2f} (threshold 0.7)")
        else:
            logger.info(f"No escalation needed for query '{query}' with score {escalation_score:.2f}")
        
        state['escalate'] = escalate
        state['message'] = f"Sentiment: {sentiment}, Priority: {priority}, Max Similarity: {max_similarity:.2f}, Score: {escalation_score:.2f}"
        return state
    except Exception as e:
        logger.error(f"Error while escalation process: {str(e)}")
        state["escalate"] = True
        return state



