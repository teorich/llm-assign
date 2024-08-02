# Chat Application

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository.
2. Navigate to the project root.

## Build and Run

```sh
docker-compose up --build
```

## API ENDPOINTS
1. Choose between Mistral or Llama2 for the model argurment
2. Run the curl code below:

```sh
curl -X POST http://localhost:3000/conversations \
-H "Content-Type: application/json" \
-d '{
  "model": "Mistral",
  "prompt": "Tell me a joke",
  "userId": "user123"
}'

```

```sh
curl -X GET http://localhost:3000/conversations

```

```sh
curl -X GET http://localhost:3000/conversations/1

```

```sh
curl -X GET http://localhost:3000/conversations/user/user123

```