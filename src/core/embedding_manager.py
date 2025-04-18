from sentence_transformers import SentenceTransformer
import numpy as np
import json
import os
from pathlib import Path
from src.utils.logger import setup_logger

logger = setup_logger(__name__, "logs/app.log")

# Load the local model
model_dir = Path(r'models\embedding_model')
if not model_dir.exists():
    logger.error(f"Local model not found at {model_dir}.")

model = SentenceTransformer(str(model_dir))
dim = 384
embedding_dir = Path(r'data\embeddings')

# Dictionaries for embedding and metadata
category_embedding = {}
category_metadata = {}

def load_category_embedding()