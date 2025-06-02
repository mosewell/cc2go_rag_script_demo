# openwebui_api_client.py: Client for interacting with OpenWebUI API
# - Use this module to send requests to the OpenWebUI server
# - Can be used by process_files.py or other scripts to store/query data
# Hints:
# - Implement functions for authentication, data upload, and querying as needed
# - Use requests or httpx for HTTP requests
# - Store server URL and API key as parameters or environment variables
# - Add error handling for network/API issues

import requests, mimetypes, json

BASE_URL = "http://localhost:8080"
API_KEY = "sk-d524e876a79545af870adba4215aac27"

# Set the headers with the Bearer token
BASE_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}",
    "Connection": "keep-alive",
    "Cookie": f"token={API_KEY}",
}

def get_user_id():
    # Get user ID
    response = requests.get(BASE_URL + "/api/v1/auths/", headers=BASE_HEADERS)
    if response:
        return response.json().get("id")
    return None

def create_or_retrieve_collection(name, description):
    # Create knowledge
    knowledge_body = {
        "name": name,
        "description": description,
        "data": {},              
        "access_control": {}      
    }

    response = requests.get(BASE_URL + "/api/v1/knowledge", headers=BASE_HEADERS)
    if response:
        for item in response.json():
            if item.get('name') == name:
                return item.get('id')

    response = requests.post(BASE_URL + "/api/v1/knowledge/create", json=knowledge_body, headers=BASE_HEADERS)
    if response:
        return response.json().get("id")
    return None

def get_mime_type(file_path):
    # Guess the MIME type and ignore encoding for HTTP purposes
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type:
        return mime_type  # Return just the MIME type as a string
    else:
        return "text/plain" # Return as text file
        # raise Exception(f"Could not determine MIME type for file: {file_path}")

def upload_file(file_path, collection_id=None):
    with open(file_path, 'rb') as file:
        # Prepare files dictionary with an active file object
        files = {
            'file': (file_path, file, get_mime_type(file_path))
        }

        # Make a POST request with files and headers
        response = requests.post(
            BASE_URL + "/api/v1/files", 
            headers=BASE_HEADERS, 
            files=files
            )
        
        if response:        
            file_id = response.json().get("id")
            if not collection_id is None:
                add_files_to_collection(collection_id, [file_id])
        else:
            return None
        
def add_files_to_collection(collection_id, file_ids):
    # Add files to knowledge
    for file_id in file_ids:
        response = requests.post(
            BASE_URL + f"/api/v1/knowledge/{collection_id}/file/add",
            json={"file_id": file_id},
            headers=BASE_HEADERS
        )
        if response.status_code == 200:
            print(f"File {file_id} added to knowledge {collection_id}.")
        else:
            print(f"Failed to add file {file_id} to knowledge {collection_id}.")


def create_chat():
    # Create chat
    chat_body = {
        "chat": {}
        }
    
    response = requests.post(BASE_URL + "/api/v1/chats/new", json=chat_body, headers=BASE_HEADERS)
    if response:
        return response.json().get("id")
    return None

def query_collection(prompt, collection, model="llama3.2:latest"):
    
    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': 'Answer the question by using the provided document collection. Only cite the documents in the provided collection.'}, 
            {'role': 'user', 'content': prompt}
        ],
        'files': [{'type': 'collection', 'id': collection}] 
    }

    response = requests.post(
        BASE_URL + f"/api/chat/completions",
        json=payload,
        headers=BASE_HEADERS
    )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to query collection {collection}.")
        return None

def ollama_prompt(prompt, model="llama3.2:latest"):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    try:
        response = requests.post(
            BASE_URL + f"/ollama/api/generate", 
            json=payload, headers=BASE_HEADERS)

        if response.status_code == 200:
            return json.loads(response.text)['response']
        else:
            print(f"Failed with status code {response.status_code}, response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")

