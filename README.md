# pdf-base64-xml

The live application is hosted on Heroku at [pdf-base64-xml](https://ddeveloper72-base64-topdf-1b37f4832a97.herokuapp.com/)

**⚒️ Work in progress 🚧**

This is a Flask application that allows users to upload PDF or XML files and encode them to base64. 
The encoded files can be previewed and downloaded by the user. 

**Usage:**
1. Run the Flask application.
2. Access the application in a web browser.
3. Upload a PDF or XML file.
4. The file will be encoded to base64 and displayed in the result page.
5. The user can preview the encoded file and download it.

**Dependencies:**
- Flask: A micro web framework for Python.
- base64: A module for encoding and decoding binary data using base64 representation.
- io: A module for working with streams and file-like objects.

**Endpoints:**
- '/' (GET, POST): The main page where users can upload files.
- '/preview' (POST): The page where users can preview the encoded file.
Note: This application assumes that the uploaded files are either in PDF or XML format.
