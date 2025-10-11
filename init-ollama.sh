#!/bin/bash

echo "🚀 Initializing Ollama models for AskMyDocs..."

# Check if Ollama container is running
if ! docker ps | grep -q "askmydocs-ollama"; then
    echo "❌ Ollama container is not running. Please start it first with: docker-compose up -d"
    exit 1
fi

echo "📥 Pulling embedding model (nomic-embed-text)..."
docker exec askmydocs-ollama ollama pull nomic-embed-text

echo "📥 Pulling chat model (llama3)..."
docker exec askmydocs-ollama ollama pull llama3

echo "✅ All models pulled successfully!"
echo "💡 Tip: To avoid re-pulling models, don't use 'docker-compose down -v'"
echo "💡 Instead use: 'docker-compose down' (without -v flag)"

# List available models
echo ""
echo "📋 Available models:"
docker exec askmydocs-ollama ollama list