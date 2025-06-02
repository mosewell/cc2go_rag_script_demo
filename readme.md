# RAG Scripting Demo
##

# readme.md: Project overview and instructions
# - Describes the purpose, features, and usage of the code meta-analysis demo
# - See below for a sample populated README (edit as needed for your project)
#
# Code Meta-Analysis Demo

This project provides a simple web interface and backend for performing code meta-analysis on a directory of files. It is designed for rapid experimentation and integration with OpenWebUI or similar APIs.

## Features
- **Web UI** (Flask): Enter API key, server URL, directory, collection name, and description.
- **Directory Upload**: Select a local directory for processing (works best in Chrome).
- **Backend Processing**: Processes files in the selected directory and sends data to a server/API.
- **Modular Design**: Easily extend processing logic and API integration.

## File Overview
- `demo_server.py`: Flask web server. Renders the form and handles user input. Calls `process_files` on form submission.
- `process_files.py`: Main logic for processing files in the selected directory. Implement your analysis or upload logic here.
- `openwebui_api_client.py`: (Optional) Client for interacting with OpenWebUI or other APIs.
- `env.py`: (Optional) Manage environment variables and configuration.
- `requirements.txt`: Python dependencies.
- `test/`: Example test files (e.g., PDFs) for demo purposes.

## Usage
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the server:**
   ```bash
   python demo_server.py
   ```
3. **Open your browser:**
   Go to [http://localhost:5000](http://localhost:5000)

4. **Fill out the form:**
   - Enter your API key and server URL.
   - Click "Choose Directory" and select a folder (Chrome recommended).
   - Enter collection name and description.
   - Click Submit.

5. **Processing:**
   - The backend will process the files and (optionally) send data to the server/API.
