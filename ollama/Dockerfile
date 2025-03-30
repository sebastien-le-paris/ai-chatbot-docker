# Use the latest Ollama image as the base
FROM ollama/ollama:latest

# Copy the model pulling script into the container
COPY ./pull-qwen-coder.sh /pull-qwen-coder.sh  

# Set the entry point to the model pulling script
ENTRYPOINT ["sh", "/pull-qwen-coder.sh"]  
