# demo_server.py: Flask web server for code meta-analysis demo
# - Renders a web form for user input (API key, server URL, directory, collection info)
# - On POST, retrieves form data and calls process_files to process the selected directory
# Hints:
# - To run: python demo_server.py
# - Ensure process_files.py exists and is implemented
# - Directory selection uses a hidden file input with webkitdirectory for folder upload (works best in Chrome)
# - You can change the default API key and server URL in the form_template
# - Debug mode is enabled for development
# - To add more fields, edit form_template and update the index() function accordingly
# - To deploy, set debug=False and consider using a production WSGI server

from flask import Flask, request, render_template_string
import sys
import io
from process_files import process_files

app = Flask(__name__)

form_template = """
<!doctype html>
<html>
    <head>
        <title>SNSU</title>
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <script>
            function getDirectoryPath() {
                var fileInput = document.getElementById('file_input');
                fileInput.click();
                fileInput.onchange = function() {
                    var files = fileInput.files;
                    if (files.length > 0) {
                        var firstFile = files[0];
                        if (firstFile && firstFile.webkitRelativePath) {
                            var fullPath = firstFile.path || firstFile.webkitRelativePath;
                            document.getElementById('directory_path').value = fullPath;
                        }
                    }
                };
            }
            function disableSubmitButton() {
                document.getElementById('submitBtn').disabled = true;
                document.getElementById('submitBtn').innerText = 'Processing...';
            }
        </script>
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center mb-4">Code Meta-Analysis Demo</h1>
            <div class="card">
                <div class="card-body">
                    <form method="post" onsubmit="disableSubmitButton()">
                        <div class="form-group">
                            <label for="api_key">API Key:</label>
                            <input type="text" class="form-control" id="api_key" name="api_key" value="sk-d524e876a79545af870adba4215aac27" required>
                        </div>
                        <div class="form-group">
                            <label for="server_url">Server URL:</label>
                            <input type="text" class="form-control" id="server_url" name="server_url" value="http://localhost:8080" required>
                        </div>
                        <div class="form-group">
                            <label for="directory_path">Directory Path:</label>
                            <input type="text" class="form-control" id="directory_path" name="directory_path" placeholder="Click 'Choose Files' to select directory" required>
                            <input type="file" id="file_input" webkitdirectory directory style="display: none;" onchange="getDirectoryPath()">
                            <button type="button" class="btn btn-secondary btn-sm mt-2" onclick="getDirectoryPath()">Choose Directory</button>
                        </div>
                        <div class="form-group">
                            <label for="collection_name">Collection Name:</label>
                            <input type="text" class="form-control" id="collection_name" name="collection_name" required>
                        </div>
                        <div class="form-group">
                            <label for="collection_desc">Collection Description:</label>
                            <input type="text" class="form-control" id="collection_desc" name="collection_desc" required>
                        </div>
                        <button type="submit" class="btn btn-primary btn-block" id="submitBtn">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve form values
        api_key = request.form.get('api_key')
        server_url = request.form.get('server_url')
        directory_path = request.form.get('directory_path')
        collection_name = request.form.get('collection_name')
        collection_desc = request.form.get('collection_desc')
        
        # Call your process_files function
        process_files(directory_path, collection_name, collection_desc)
    
    return render_template_string(form_template)

if __name__ == '__main__':
    app.run(debug=True)