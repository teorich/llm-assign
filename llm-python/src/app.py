from flask import Flask, request, jsonify
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import replicate

app = Flask(__name__)

# API Keys and Models
API_KEYS = {
    "Llama2": "r8_EQFRsfGsVZ5vHNJUARot2Xeee3roypZ3GFpZL",
    "Mistral": "EmQ5gcrQwTpKUq1EefLj40X1bLF1YwFZ"
}
MODELS = {
    "Llama2": "meta/meta-llama-3-70b-instruct",
    "Mistral": "mistral-large-latest"
}

# Initialize clients
clients = {
    "Llama2": replicate.Client(API_KEYS["Llama2"]),
    "Mistral": MistralClient(api_key=API_KEYS["Mistral"])
}

# In-memory storage for conversation context
conversation_context = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    model = data.get('model')
    prompt = data.get('prompt')
    user_id = data.get('user_id', 'default_user')
    
    if model not in API_KEYS:
        return jsonify({"error": "Model not supported"}), 400
    
    if model not in conversation_context:
        conversation_context[model] = {}
    
    if user_id not in conversation_context[model]:
        conversation_context[model][user_id] = []
    
    conversation_context[model][user_id].append(prompt)
    
    if model == "Llama2":
        inputs = {"prompt": "\n".join(conversation_context[model][user_id])}
        iterator = clients[model].run(MODELS[model], input=inputs)
        response = "".join(str(text) for text in iterator)
    elif model == "Mistral":
        messages = [ChatMessage(role="user", content=prompt)]
        response = clients[model].chat(
            model=MODELS[model],
            messages=messages
        ).choices[0].message.content
    
    conversation_context[model][user_id].append(response)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)