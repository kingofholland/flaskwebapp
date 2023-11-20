from flask import Flask, request, jsonify
import openai
import os
import time

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Assume you have stored the ID of the assistant in your environment variables
assistant_id = os.getenv('ASSISTANT_ID')

@app.route('/generate-practice', methods=['POST'])
def generate_practice():
    data = request.json
    query = data['query']  # User's query to generate a soccer practice
    
    # Create a thread for the conversation
    thread = openai.Thread.create(assistant_id=assistant_id)
    
    # Add user's message to the thread
    openai.Message.create(
        thread_id=thread.id,
        role="user",
        content=query
    )
    
    # Run the assistant to generate a practice plan
    run = openai.Run.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    
    # Polling for the run status
    while True:
        run_status = openai.Run.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status['status'] == 'completed':
            # When the run is completed, retrieve the messages
            messages = openai.Message.list(thread_id=thread.id)
            # The last message should be the assistant's response
            assistant_response = messages['data'][-1]['content']
            break
        elif run_status['status'] == 'failed':
            return jsonify({"error": "The run has failed."}), 500
        time.sleep(1)  # Sleep for a short period to avoid rate limits

    return jsonify({"response": assistant_response})

if __name__ == '__main__':
    app.run(debug=True)
