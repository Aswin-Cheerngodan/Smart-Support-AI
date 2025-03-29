from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.core.state import SupportState
import torch
import yaml
from pathlib import Path
from src.utils.logger import setup_logger



# Load configuration
config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

logger = setup_logger(__name__, "logs/app.log")

MODEL_PATH = Path(r"models\sentiment_model")
SENTIMENT_MAP = {0: "Very Negative", 1: "Negative", 2: "Neutral", 3: "Positive", 4: "Very Positive"}
# Load sentiment model and tokenizer
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    logger.info(f"Model and tokenizer loaded from {MODEL_PATH}")
except Exception as e:
    logger.error(f"Failed to load the model: {str(e)}")
    raise

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def sentiment_analyzer(state: SupportState) -> SupportState:
    """Classify the qurey sentiment using the sentiment model

    Args:
        state: current support state with query and query category.

    Returns:
        Updated support state with classified sentiment.
    """

    query = state['query']
    try:
        inputs = tokenizer(
            query,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}
        logger.info("Input query toknization done.")
        # Inference
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1).cpu()
            predicted_idx = torch.argmax(probs, dim=1).item()
            sentiment = SENTIMENT_MAP[predicted_idx]
            logger.info(f"Query: '{query}' -> Probabilities: {probs}, Predicted Category: {sentiment}")
            state['sentiment'] = sentiment
            logger.info(state)
            return state
        
    except Exception as e:
        logger.error(f"Sentiment analysis failed '{query}': {str(e)}")
        state['sentiment'] = "Neutral"
        return state





if __name__=="__main__":
    test_queries = [
        "I need to reset my password.",  # Expected: Login and Account
        "Where is my order?",  # Expected: Order
        "How long does shipping take?",  # Expected: Shipping
        "I want to return my product.",  # Expected: Cancellations and returns
        "Does my laptop come with a warranty?",  # Expected: Warranty
        "What are the available deals today?",  # Expected: Shopping
        ]

    # Run test cases
    for query in test_queries:
        state = SupportState({"query": query})  # Create state object
        updated_state = sentiment_analyzer(state)  # Run categorization
        # print(f"Query: '{query}' -> Predicted Category: {updated_state['category']}") 