from flask import Flask, render_template, request
import base64
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error_message='No file part in the request.')
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error_message='No file selected.')

        # Extract and check file extension
        if '.' in file.filename:
            file_extension = file.filename.rsplit('.', 1)[1].lower()
        else:
            return render_template('index.html', error_message='Invalid file. Please upload a file with a proper extension.')

        if file_extension == 'pdf':
            if file:
                try:
                    # Read the file contents
                    file_contents = file.read()
                    # Encode the file contents to base64
                    encoded_string = base64.b64encode(file_contents).decode('utf-8')
                    return render_template('result.html', encoded_string=encoded_string)
                except Exception as e:
                    return render_template('index.html', error_message=f'Error processing PDF file: {str(e)}')

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
                            return render_template('result.html', encoded_string=encoded_string)
                    return render_template('index.html', error_message='Base64 content not found in XML.')
                except Exception as e:
                    return render_template('index.html', error_message=f'Error processing XML file: {str(e)}')

        else:
            return render_template('index.html', error_message='Invalid file type. Please upload a PDF or XML file.')

    return render_template('index.html')



# convert the base64 string back into a virtual pdf document and preview it in the result.html as well as allow the user to download it
@app.route('/preview', methods=['POST'])
def preview():
    encoded_string = request.form['encoded_string']
    # Decode the base64 string
    decoded_string = base64.b64decode(encoded_string)
    # Create a virtual file to write the decoded content
    virtual_file = io.BytesIO(decoded_string)
    return render_template('result.html', virtual_file=virtual_file, encoded_string=encoded_string)           

if __name__ == '__main__':
    app.debug = True
    app.run()
