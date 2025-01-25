from ollama import chat, embeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup

# 1. Extract and preprocess content from URL
def extract_content_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()  # Extract plain text from the HTML
        return content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return ""

# Replace with the desired URL(s)
urls = [
    "https://ensani.ir/fa/article/83978/%D8%AE%D9%84%DB%8C%D9%81%D9%87-%D8%B3%D9%84%D8%B7%D8%A7%D9%86-%D8%B3%D9%84%D8%B7%D8%A7%D9%86-%D8%A7%D9%84%D8%B9%D9%84%D9%85%D8%A7-%D9%81%D9%82%DB%8C%D9%87-%D9%88-%D9%88%D8%B2%DB%8C%D8%B1-%D8%A7%D8%B9%D8%B8%D9%85-%D8%B9%D8%B5%D8%B1-%D8%B5%D9%81%D9%88%D9%89",
    "https://article.bsfe.ir/ArticleShow.aspx?rs=326"
]

# Aggregate content from URLs
text = ""
for url in urls:
    text += extract_content_from_url(url) + "\n"

# 2. Split with overlap
chunk_size = 1000
overlap = 200
chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size - overlap)]

# 3. Create embeddings using dorna-llama3
chunk_embeddings = []
for chunk in chunks:
    response = embeddings(model='partai/dorna-llama3', prompt=chunk)
    chunk_embeddings.append(response['embedding'])

# 4. Context retrieval system
def find_relevant_chunks(query, top_k=3):
    # Generate query embedding
    query_embed = embeddings(model='partai/dorna-llama3', prompt=query)['embedding']

    # Calculate similarities
    scores = cosine_similarity([query_embed], chunk_embeddings)[0]

    # Return top chunks
    best_indices = np.argsort(scores)[-top_k:][::-1]
    return "\n---\n".join([chunks[i] for i in best_indices])

# 5. RAG-enhanced chat function
def rag_chat(query):
    # Retrieve context
    context = find_relevant_chunks(query)

    # Create augmented prompt
    prompt = f"""Answer the question using this context:
{context}

Question: {query}
Answer clearly and concisely in Persian:"""

    # Get response
    response = chat(model='partai/dorna-llama3', messages=[
        {'role': 'user', 'content': prompt}
    ])

    return response['message']['content']

# Example usage
from datetime import datetime
start = datetime.now()

response = rag_chat("خلیفه سلطان که بود و چه کرد؟")

duration  = datetime.now() - start
# Format timedelta without microseconds
hours, remainder = divmod(duration.total_seconds(), 3600)
minutes, seconds = divmod(remainder, 60)
formatted_duration = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
print('process time: ',formatted_duration)  # Output: 00:35:51

file_path = r'C:\\Users\\User\\Desktop\\LLM\\Test_LLM_fun-tuning\\output_url1_2.txt'
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(response + '\n\n')
print(f"Responses saved to {file_path}")
print("پاسخ:", response)
