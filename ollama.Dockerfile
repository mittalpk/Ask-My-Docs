FROM ollama/ollama:latest

# Create directory for models
RUN mkdir -p /root/.ollama

# Start ollama in background, pull models, then stop it
RUN /bin/ollama serve & \
    sleep 10 && \
    /bin/ollama pull nomic-embed-text && \
    /bin/ollama pull llama3 && \
    pkill ollama

# The models are now baked into the image at /root/.ollama
# When the container starts, they'll be available immediately

# Use the same entrypoint and cmd as the base image
ENTRYPOINT ["/bin/ollama"]
CMD ["serve"]