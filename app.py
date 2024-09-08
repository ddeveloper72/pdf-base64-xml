from flask import Flask, render_template, request
import base64
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        if file_extension == 'pdf':
            if file:
                # Read the file contents
                file_contents = file.read()
                # Encode the file contents to base64
                encoded_string = base64.b64encode(file_contents).decode('utf-8')
                return render_template('result.html', encoded_string=encoded_string)
        if file_extension == 'xml':
            if file:
                # Read the file contents
                file_contents = file.read()
                # Find the base64 encoding in the XML file
                start_index = file_contents.find(b'<text mediaType="application/pdf" representation="B64">') + len(b'<text mediaType="application/pdf" representation="B64">')
                end_index = file_contents.find(b'</text>')
                if start_index != -1 and end_index != -1:
                    encoded_string = file_contents[start_index:end_index].decode('utf-8')
                    return render_template('result.html', encoded_string=encoded_string) 
                
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
