from ollama import chat
from ollama import ChatResponse

# Define file path (raw string for Windows paths)
# First query and save
start = datetime.now()

response = chat(model='partai/dorna-llama3', messages=[
    {'role': 'user', 'content': 'خلیفه سلطان که بود و چه کرد؟'},])

duration  = datetime.now() - start
# Format timedelta without microseconds
hours, remainder = divmod(duration.total_seconds(), 3600)
minutes, seconds = divmod(remainder, 60)
formatted_duration = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
print('process time: ',formatted_duration)  # Output: 00:35:51

file_path = r'C:\Users\User\Desktop\LLM\Test_LLM_fun-tuning\output_Dorna.txt'
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(response['message']['content'] + '\n\n')
print(f"Responses saved to {file_path}")
print("پاسخ:", response['message']['content'])



# Second query and append
# response = chat(model='partai/dorna-llama3', messages=[
#     {'role': 'user', 'content': 'چرا اینترنت قطع میشه؟'},
# ])
# with open(file_path, 'w', encoding='utf-8') as f:
#     f.write(response['message']['content'] + '\n\n')
# print(f"Responses saved to {file_path}")

from ollama import chat, embeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
# 1. Load and chunk document
with open(r'C:\Users\User\Downloads\Telegram Desktop\data.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split with overlap
chunk_size = 1000
overlap = 200
chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size - overlap)]

# 2. Create embeddings using dorna-llama3
chunk_embeddings = []
for chunk in chunks:
    response = embeddings(model='partai/dorna-llama3', prompt=chunk)
    chunk_embeddings.append(response['embedding'])


# 3. Context retrieval system
def find_relevant_chunks(query, top_k=3):
    # Generate query embedding
    query_embed = embeddings(model='partai/dorna-llama3', prompt=query)['embedding']

    # Calculate similarities
    scores = cosine_similarity([query_embed], chunk_embeddings)[0]

    # Return top chunks
    best_indices = np.argsort(scores)[-top_k:][::-1]
    return "\n---\n".join([chunks[i] for i in best_indices])


# 4. RAG-enhanced chat function
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
start=datetime.now()

response = rag_chat("چرا اینترنت قطع میشود؟")

duration  = datetime.now() - start
# Format timedelta without microseconds
hours, remainder = divmod(duration.total_seconds(), 3600)
minutes, seconds = divmod(remainder, 60)
formatted_duration = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
print('process time: ',formatted_duration)  # Output: 00:35:51

file_path = r'C:\Users\User\Desktop\LLM\Test_LLM_fun-tuning\output_text_data.txt'
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(response + '\n\n')
print(f"Responses saved to {file_path}")
print("پاسخ:", response)
