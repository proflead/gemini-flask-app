# The json module is used to work with JSON data.
# The os module is used to interact with the operating system.

import json
import os

# Flask: Creates the Flask web application.
# jsonify: Converts data to JSON format for responses.
# request: Accesses incoming request data.
# send_file: Sends files to the client.
# send_from_directory: Sends files from a specified directory.

from flask import Flask, jsonify, request, send_file, send_from_directory

# HumanMessage from langchain_core.messages: Represents a message from a human user.
# ChatGoogleGenerativeAI from langchain_google_genai: Provides a chat interface for Google's generative AI.

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI


# Creates a Flask web application named app.
app = Flask(__name__)

# Sets an environment variable GOOGLE_API_KEY with a specified API key.
os.environ["GOOGLE_API_KEY"] = "AIzaSyDV_TzW4k3dqapFmDLha2jh9BARbeUIWos"; 

# Defines a route for the home page (/) that sends the index.html file from the web directory.
@app.route('/')
def home():
    return send_file('web/index.html')


# Defines a route for the /api/generate endpoint that accepts POST requests.
# When a POST request is received, it gets the JSON data from the request body.
# Extracts the "contents" and "model" from the JSON data.
# Creates a ChatGoogleGenerativeAI model and a HumanMessage with the content.
# Streams the model's response in chunks, sending each chunk as a JSON event stream.
# If an error occurs, it returns a JSON response with the error message.
@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        try:
            req_body = request.get_json()
            content = req_body.get("contents")
            model = ChatGoogleGenerativeAI(model=req_body.get("model"))
            message = HumanMessage(
                content=content
            )
            response = model.stream([message])
            def stream():
                for chunk in response:
                    yield 'data: %s\n\n' % json.dumps({ "text": chunk.content })

            return stream(), {'Content-Type': 'text/event-stream'}

        except Exception as e:
            return jsonify({ "error": str(e) })


# Defines a route to serve static files from the web directory for any given path.
# When a request matches the path, it sends the requested file from the web directory.
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

# If the script is run directly, it starts the Flask app in debug mode.
if __name__ == '__main__':
    app.run(debug=True)