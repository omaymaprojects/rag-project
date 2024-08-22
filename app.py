from flask import Flask, request, jsonify
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration
import torch

app = Flask(__name__)

# Initialize the tokenizer, retriever, and model
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
retriever = RagRetriever.from_pretrained("facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True)
model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

def generate_answer(query):
    input_ids = tokenizer(query, return_tensors="pt").input_ids
    with torch.no_grad():
        output_ids = model.generate(input_ids)
    return tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    query = data.get('query', '')
    if query:
        answer = generate_answer(query)
        return jsonify({'answer': answer})
    return jsonify({'error': 'No query provided'}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
