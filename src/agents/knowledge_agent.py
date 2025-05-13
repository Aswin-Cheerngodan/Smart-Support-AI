from sentence_transformers import SentenceTransformer
import numpy as np
import json
import os
from pathlib import Path
from src.utils.logger import setup_logger
from src.core.state import SupportState

logger = setup_logger(__name__, "logs/app.log")

model_dir = Path(r'models/embedding_model')
if not model_dir.exists():
    logger.error(f"Local model not found at {model_dir}")

model = SentenceTransformer(str(model_dir))
dim = 384

embedding_dir = Path(r'data/embeddings')

category_embeddings = {}
category_metadata = {}

def load_category_embeddings(category: str):
    """Load embeddings and metadata for specific category."""
    if category in category_embeddings and category in category_metadata:
        return
    
    embeddings_file = embedding_dir / f"{category}_embeddings.npy"
    metadata_file = embedding_dir / f"{category}_metadata.json"
    if not embeddings_file.exists() or not metadata_file.exists():
        logger.warning(f"No precomputed embedding for category: {category}")
        return None
    else:
        embedidng = np.load(embeddings_file)
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        category_embeddings[category] = embedidng
        category_metadata[category] = metadata
        logger.info(f"Loaded embeddings and metadata for category: {category}")



def Knowledge_update(state: SupportState) -> SupportState:
    """Finds the related conversation from the knowledge base and updates the state
    
    Args:
        state: Current support state with updated upto priority.
    Returns:
        state: updated support state
    """
    query = state['query']
    category = state['category']
    try:
        #Load embeddings for the specific category
        load_category_embeddings(category)
        logger.info(f"Loading the embeddings for the category is completed")
        
        embeddings = category_embeddings[category]
        metadata = category_metadata[category]
        # Making query embedding and calculating similarities
        query_embed = np.array([model.encode([query])[0]])
        similarities = np.sum(embeddings * query_embed, axis=1).flatten() / (
            np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embed)
        )
        logger.info(f"Found similiarities between the queries.")

        #Finding top results
        top_indices = np.argsort(similarities)[::-1][:3]
        top_similarities = similarities[top_indices]
        top_results = [(metadata[str(i)], s) for i, s in zip(top_indices, top_similarities)]
        logger.info(f"Found the top results for the qurey from the knowledge base with top similiarities {top_similarities}")

        #Updating state
        state['kb_answer'] = top_results
        state['top_similarity_score'] = top_similarities[0]
        logger.info(f"Updated the state with knowledge base answer and the top similarity score") 
        return state
    except Exception as e:
        logger.error(f"Error while updating state with converesations knowledge base: {str(e)}", exc_info=True)
        state["kb_answer"] = "An error occurred while searching. Please try again later."
        state['top_similarity_score'] = None
        return state




