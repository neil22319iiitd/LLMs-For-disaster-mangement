# Install chromadb if not already installed
!pip install chromadb

import pandas as pd
import re
from transformers import AutoTokenizer, AutoModel
import torch
import chromadb
from chromadb.config import Settings

# Function to load and concatenate all CSV files
def load_csv_files(file_list):
    dataframes = []
    for file in file_list:
        df = pd.read_csv(file)
        dataframes.append(df)
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df

# Function to preprocess text
def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)  # remove URLs
    text = re.sub(r'@\w+', '', text)  # remove mentions
    text = re.sub(r'#\w+', '', text)  # remove hashtags
    text = re.sub(r'\W', ' ', text)  # remove non-word characters
    text = text.lower().strip()  # convert to lower case and strip white spaces
    return text

# Function to generate embeddings using a pre-trained model
def embed_text(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings

# List of CSV files
csv_files = [
    '/kerala_floods_2018_tweets1.csv',
    '/kerala_floods_2018_tweets2.csv',
    '/kerala_floods_2018_tweets3.csv',
    '/kerala_floods_2018_tweets5.csv',
    '/kerala_floods_2018_tweets6.csv',
    '/kerala_floods_2018_tweets7.csv',
    '/kerala_floods_2018_tweets8.csv',
    '/kerala_floods_2018_tweets9.csv',
    '/kerala_floods_2018_tweets10.csv',
    '/kerala_floods_2018_tweets11.csv',
    '/kerala_floods_2018_tweets12.csv',
    '/kerala_floods_2018_tweets13.csv',
    '/kerala_floods_2018_tweets14.csv',
    '/kerala_floods_2018_tweets15.csv',
    '/kerala_floods_2018_tweets16.csv',
    '/kerala_floods_2018_tweets17.csv',
    '/kerala_floods_2018_tweets18.csv',
    '/kerala_floods_2018_tweets19.csv',
    '/kerala_floods_2018_tweets20.csv'

]

# Load and preprocess data
df = load_csv_files(csv_files)
df['Processed_Tweets'] = df['Tweets'].apply(preprocess_text)

# Load pre-trained model and tokenizer
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Generate embeddings
embeddings = [embed_text(tweet, tokenizer, model).numpy().flatten() for tweet in df['Processed_Tweets']]

# Print embeddings
for i, embedding in enumerate(embeddings):  # Print embeddings of first 5 tweets as an example
    print(f"Embedding {i}:")
    print(embedding)
    print()

# Initialize ChromaDB
chroma_client = chromadb.Client()

# Create a collection with a new name
collection_name = 'tweets_new25'  # Change this to a new name
collection = chroma_client.create_collection(name=collection_name)

# Prepare documents for insertion
ids = []
embedding_vectors = []
metadata = []

for i, embedding in enumerate(embeddings):
    ids.append(str(i))
    embedding_vectors.append(embedding.tolist())
    metadata.append({
        'UserTags': df['UserTags'][i],
        'TimeStamps': df['TimeStamps'][i],
        'Replys': df['Replys'][i],
        'ReTweets': df['ReTweets'][i],
        'Likes': df['Likes'][i]
    })

# Insert documents into the vector database
collection.add(ids=ids, embeddings=embedding_vectors, metadatas=metadata)

print(f'Successfully stored {len(embeddings)} embeddings in the vector database.')