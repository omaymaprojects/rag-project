from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration
import torch

# Initialize the tokenizer, retriever, and model
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
retriever = RagRetriever.from_pretrained("facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True)
model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

def generate_answer(query):
    input_ids = tokenizer(query, return_tensors="pt").input_ids
    with torch.no_grad():
        output_ids = model.generate(input_ids)
    return tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]

# Test the model
if __name__ == "__main__":
    query = "What is the capital of France?"
    print(generate_answer(query))
