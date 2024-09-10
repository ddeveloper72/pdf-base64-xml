import io
import os
import base64
import secrets
from flask import Flask, flash, render_template, request, send_file

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(16)

# Home page
@app.route('/')
def index():
    return render_template('index.html')


# Upload file and display the PDF preview
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    error = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part in the request. Please upload a file.', 'alert-danger')
            return render_template('index.html')
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file. Please upload a file.', 'alert-warning')
            return render_template('index.html')

        # Extract and check file extension
        if '.' in file.filename:
            file_extension = file.filename.rsplit('.', 1)[1].lower()
        else:
            flash('Invalid file. Please upload a file with a proper extension.', 'alert-danger')
            return render_template('index.html')

        if file_extension == 'pdf':
            if file:
                try:
                    # Read the file contents
                    file_contents = file.read()
                    # Encode the file contents to base64
                    encoded_string = base64.b64encode(file_contents).decode('utf-8')
                    return render_template('result.html', encoded_string=encoded_string, page_title='PDF Preview')
                except IOError as e:
                    flash(f'Error processing PDF file: {str(e)}')
                    return render_template('index.html')

        elif file_extension == 'xml':
            if file:
                try:
                    # Read the file contents
                    file_contents = file.read()
                    # Find the base64 encoding in the XML file
                    start_tag = b'<text mediaType="application/pdf" representation="B64">'
                    end_tag = b'</text>'
                    start_index = file_contents.find(start_tag)
                    if start_index != -1:
                        start_index += len(start_tag)
                        end_index = file_contents.find(end_tag, start_index)
                        if end_index != -1:
                            encoded_string = file_contents[start_index:end_index].decode('utf-8')
                            return render_template('result.html', encoded_string=encoded_string, page_title='PDF Preview')                      
                    else:
                        flash('No base64 string was found in this XML.', 'alert-warning')
                        return render_template('index.html', error=error)
                    
                except IOError as e:
                    flash(f'Error processing XML file: {str(e)}')
                    return render_template('index.html')

        else:
            flash('Invalid file type. Please upload a PDF or XML file.', 'alert-danger')
            return render_template('index.html')

    return render_template('index.html')


# Serve the PDF file
@app.route('/serve_pdf', methods=['POST'])
def serve_pdf():
    encoded_string = request.form['encoded_string']

    # Decode the base64 string
    decoded_string = base64.b64decode(encoded_string)

    # Create a virtual file for the PDF and serve it
    virtual_file = io.BytesIO(decoded_string)
    virtual_file.seek(0)
    
    # Send the PDF file to the browser
    return send_file(virtual_file, as_attachment=False, mimetype='application/pdf', download_name="preview.pdf")


# Page not found error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal server error handler
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
            port=os.getenv('PORT'),
            debug=False)
