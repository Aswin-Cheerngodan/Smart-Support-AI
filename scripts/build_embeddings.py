from sentence_transformers import SentenceTransformer
import torch
import numpy as np
import pandas as pd
import json
import os
from src.utils.logger import setup_logger
from pathlib import Path

logger = setup_logger(__name__, "logs/app.log")

csv_file = Path(r'data/knowledge base data/knowledge_base.csv')
embedding_dir = Path(r'data/embeddings')
model_dir = Path(r'models/embedding_model')


model = SentenceTransformer(str(model_dir))
logger.info(f"Loaded model from {model_dir}")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
logger.info(f"Using device: {device}")

dim = 384

if not csv_file.exists():
    logger.error(f"CSV file not found at {csv_file}")

df = pd.read_csv(csv_file)
past_queries_by_category = {}

for _, row in df.iterrows():
    category = row['category']
    query = row['query']
    conversation = row['conversation']
    if category not in past_queries_by_category:
        past_queries_by_category[category] = {"queries": [], "conversations": []}
    past_queries_by_category[category]["queries"].append(query)
    past_queries_by_category[category]["conversations"].append(conversation)

# Generate and save embedding in batches
batch_size = 64
for category, data in past_queries_by_category.items():
    queries = data["queries"]
    conversations = data["conversations"]
    embedding_file = embedding_dir / f"{category}_embeddings.npy"
    metadata_file = embedding_dir / f"{category}_metadata.json"

    if not embedding_file.exists() or not metadata_file.exists():
        logger.info(f"Processing category '{category}' with {len(queries)} queries...")
        all_embeddings = []
        metadata = {}
    
        for i in range(0, len(queries), batch_size):
            batch = queries[i:i + batch_size]
            batch_conv = conversations[i:i+batch_size]
            batch_embeddings = model.encode(batch)
            all_embeddings.append(batch_embeddings)
            for j, conversation in enumerate(batch_conv):
                metadata[str(i + j)] = conversation

        embeddings = np.vstack(all_embeddings)
        np.save(embedding_file, embeddings)
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f)
        logger.info(f"Saved embeddings and metadata for '{category}'")
    else:
        logger.info(f"Skipping '{category}': Files already exist")

logger.info("Embedding pre-computation complete!")
    



