from flask import Flask, request, jsonify
from llamaapi import LlamaAPI
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

app = Flask(__name__)

# API Keys and Models
API_KEYS = {
    "Llama2": "LL-0B7kU8I0ogm1yJLPeheSTPDEMVy7sxEsiOFllgsLTnlpmQbrS8uqVdsknjRlSnsU",
    "Mistral": "EmQ5gcrQwTpKUq1EefLj40X1bLF1YwFZ"
}
MODELS = {
    "Llama2": "llama3-70b",
    "Mistral": "mistral-large-latest"
}


clients = {
    "Llama2": LlamaAPI(API_KEYS["Llama2"]),
    "Mistral": MistralClient(api_key=API_KEYS["Mistral"])
}

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
        api_request_json = {
            "model": MODELS[model],
            "messages": [{"role": "user", "content": "\n".join(conversation_context[model][user_id])}]
        }
        response = clients[model].run(api_request_json)
        response_text = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    elif model == "Mistral":
        messages = [ChatMessage(role="user", content=prompt)]
        response = clients[model].chat(
            model=MODELS[model],
            messages=messages
        )
        response_text = response.choices[0].message.content
    
    conversation_context[model][user_id].append(response_text)
    
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
