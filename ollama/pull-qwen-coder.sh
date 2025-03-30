# Start the server in the background
./bin/ollama serve &

# Get the PID of the server process
pid=$!

# Wait for a few seconds
sleep 5

# Pull the model
echo "Pulling qwen2.5-coder model"
ollama pull qwen2.5-coder:0.5b

# Wait for the server to finish running
wait $pid
