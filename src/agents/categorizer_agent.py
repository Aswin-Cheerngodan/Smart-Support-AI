from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from src.core.state import SupportState
import torch
import logging
import yaml
from pathlib import Path


# Load configuration
config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="logs/main_log.log",
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


MODEL_PATH = Path("models/fine_tuned_distilbert")
LABELS = ["Login and Account", "Order", "Shipping", "Cancellations and returns", "Warranty", "Shopping"]

# Load fine-tuned DistilBERT model and tokenizer
try:
    tokenizer = DistilBertTokenizer.from_pretrained(MODEL_PATH)
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
    model.eval()
    logger.info(f"Loaded fine-tuned distilBERT from {MODEL_PATH}")
except Exception as e:
    logger.error(f"Failed to load the model {e}")
    raise

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def categorizer(state: SupportState) -> SupportState:
    """
    Categorize the query using the fine-tuned DistilBERT model.

    Args:
        state: Current SupportState with the raw query.

    Returns:
        SupportState: Updated state with the predicted category.
    """
    query = state['query']
    try:
        # Tokenize input
        inputs = tokenizer(
            query,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_lenth=512
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Inference
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1).cpu().tolist()[0]
            predicted_idx = torch.argmax(logits, dim=1).item()
            category =  LABELS[predicted_idx]

        prob_dict = {label: round(prob, 4) for label, prob in zip(LABELS, probs)}
        logger.info(f"🔍 Query: '{query}' -> Probabilities: {prob_dict}, Predicted Category: {category}")

        state["category"] = category
        return state
    
    except Exception as e:
        logger.error(f"Error categorizing '{query}': {e}")
        state["category"] = "General"  
        return state



if __name__ == "__main__":
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
        updated_state = categorizer(state)  # Run categorization
        print(f"Query: '{query}' -> Predicted Category: {updated_state['category']}")
    