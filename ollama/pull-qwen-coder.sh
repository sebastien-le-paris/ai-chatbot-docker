#!/bin/sh

# Define the model directory
export OLLAMA_MODELS="$MODEL_PATH"

# Start the server in the background with the custom model path
OLLAMA_MODELS="$MODEL_PATH" ./bin/ollama serve &

# Get the PID of the server process
pid=$!

# Wait for the server to initialize
sleep 5

# Define the model name
MODEL_NAME="qwen2.5-coder:0.5b"

# Check if the model already exists
if [ ! -d "$MODEL_PATH/qwen2.5-coder" ]; then
    echo "Pulling $MODEL_NAME model into $MODEL_PATH"

    # Ensure the destination path exists
    mkdir -p "$MODEL_PATH"

    # Pull the model
    ollama pull "$MODEL_NAME"
else
    echo "Model $MODEL_NAME already exists in $MODEL_PATH, skipping download."
fi

# Wait for the server to finish running
wait $pid

