import os, random
import env
from openwebui_api_client import *

# process_files.py: Handles processing of files in a directory for code meta-analysis
# - Expects a function: process_files(directory_path, collection_name, collection_desc)
# - Called by demo_server.py when the form is submitted
# Hints:
# - Implement your file reading, parsing, or analysis logic here
# - You can use os.walk to iterate through files in the directory
# - Use collection_name and collection_desc for organizing or labeling processed data
# - Add logging or print statements for debugging
# - Ensure this file is importable (no code should run on import except function/class definitions)

# Set the headers with the Bearer token
BASE_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}",
    "Connection": "keep-alive",
    "Cookie": f"token={API_KEY}",
}

TEMP_PATH = './temp'

def load_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            prompt = file.read()
            return prompt
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred reading the file: {str(e)}")
        return None
    
def random_emoji():
    emoji_range = range(0x1F600, 0x1F64F) 
    random_emoji_unicode = random.choice(list(emoji_range))
    return chr(random_emoji_unicode)


def process_files(directory_path, collection_name, collection_desc):
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)

    print(f"process_files called with: {directory_path}, {collection_name}, {collection_desc}")
    collection_id = create_or_retrieve_collection(collection_name, collection_desc)
    generate_manifest(directory_path, collection_id)
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.meta'):
                continue  # Skip files ending with .meta
            
            file_path = os.path.join(root, file)
            
            # Check if the file is binary
            if not is_binary_file(file_path):
                try:
                    if file.endswith('.md'):
                        new_filepath = file_path
                    else:      

                        # Read file as text
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            file_content = f.read()
                            file_content = interpret_code(file_path=file_path,file_content=file_content)
                            
                        
                        # Prepare new file name with .meta extension appended
                        new_filepath = os.path.join(TEMP_PATH, file + '.meta')
                    
                        if file_content is not None:
                            print(f"{random_emoji()} - {file_path}")
                            # Write the content to the new file
                            # Write the text to the new .meta file, overwriting if necessary
                            with open(new_filepath, 'w', encoding='utf-8') as f:
                                f.write(file_content)

                    upload_file(new_filepath, collection_id)

                    os.remove(new_filepath)
                        
                    print(f"Processed {file_path} -> {new_filepath}")
                
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
        
#    add_files_to_collection(collection_id=collection_id,file_ids=file_ids)

def interpret_code(file_path, file_content):
    file_prompt = (
        "You are a python coding expert, writing an output that will be read by a RAG process. Write an overview for the attached code. Include the following points:"
        f"In the first line, output this verbatim, with no commentary:  FILE_PATH={file_path}"
        "-Describe what the overall file does."
        "-For each element of the code, such as function, class, etc. write whe name of the element, then what it does, the other elements that reference it, which elements it references, its parameters and expected outputs."
        f"\n\nFILE_CODE=\n{file_content}"
    )
    return ollama_prompt(model="mistral-nemo:latest",prompt=file_prompt)


def is_binary_file(filepath):
    """Determine if a file is binary by reading its content."""
    try:
        with open(filepath, 'rb') as file:
            chunk = file.read(1024)
            if b'\0' in chunk:
                return True
        return False
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return True  # Handle potential read errors as binary

def generate_manifest(directory, collection_id):
    """Recursively list all files in a directory and its subdirectories."""
    file_list = []

    # Walk through the directory tree
    for root, _, files in os.walk(directory):
        for file in files:
            # Generate full file path
            full_path = os.path.join(root, file)
            # Add file path to the list
            file_list.append(full_path)

    # Define the manifest file path in the root directory
    manifest_path = os.path.join(directory, 'manifest.meta')

    # Write the file list to the manifest file
    try:
        with open(manifest_path, 'w', encoding='utf-8') as manifest_file:
            for file_path in file_list:
                manifest_file.write(file_path + '\n')
        print(f"Manifest saved at {manifest_path}")
    except Exception as e:
        print(f"Error saving manifest: {e}")

    upload_file(manifest_path, collection_id)


# if __name__ == "__main__":

#     #create knowledge


#     file_path="process_files.py"

#     file_contents=load_file(file_path)

#     collection_id = create_or_retrieve_collection("TestCollection", "Test collection description")

#     file_prompt = (
#         "You are a python coding expert, writing an output that will be read by a RAG process. Write an overview for the attached code. Include the following points:"
#         f"In the first line, include this verbatim:  FILE_PATH={os.path.abspath(file_path)}"
#         "-Describe what the overall file does."
#         "-For each element of the code, such as function, class, etc. write whe name of the element, then what it does, the other elements that reference it, which elements it references, its parameters and expected outputs."
#         f"\n\nFILE_CODE=\n{file_contents}"
#     )

    #print(f"Response: {ollama_prompt(model="llama3.2:latest",prompt="What is the name of the official animal of Australia?")}")
    #print(f"Response: {ollama_prompt(model="llama3.2:latest",prompt=file_prompt)}")

    #generate_manifest(".")

    #process_files(".")


    # file_ids = []

    # #upload file
    # file_path = "FILENAME.pdf"
    # file_id = upload_file(file_path)

    # if file_id:
    #     file_ids.append(file_id)
    #     print("File uploaded successfully:", file_id)
    # else:
    #     print("File upload failed.")

    # #add files to knowledge
    # add_files_to_collection(collection_id, file_ids)
    
    # #create_chat
    # chat_id = create_chat()
    # if chat_id:
    #     print("Chat created successfully:", chat_id)
    # else:
    #     print("Chat creation failed.")
    
    #Ask collection
    #query_collection("What is the main topic of the document?", "TestCollection")



