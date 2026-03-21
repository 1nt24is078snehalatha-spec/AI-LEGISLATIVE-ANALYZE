from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(chunks):
    return model.encode(chunks, convert_to_tensor=True)

def search(query, chunks, embeddings):
    query_embedding = model.encode(query, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, embeddings)[0]
    top_results = scores.argsort(descending=True)[:5]

    return [chunks[i] for i in top_results]