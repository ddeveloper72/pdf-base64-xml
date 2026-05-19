# PDF Base64 Encoder/Decoder

A Flask web application for encoding PDFs to base64 strings and extracting base64-encoded PDFs embedded in XML documents.

🔗 **Live Demo:** [pdf-base64-xml on Heroku](https://ddeveloper72-base64-topdf-1b37f4832a97.herokuapp.com/)

## What Does This Application Do?

This tool provides a simple web interface for working with PDFs and base64 encoding in two ways:

1. **PDF to Base64 Encoding** - Upload a PDF file and convert it to a base64-encoded string
2. **XML to PDF Extraction** - Upload an XML file containing embedded base64-encoded PDF data and extract/decode it back to a viewable PDF

## How It Works

### PDF Upload Process
1. User uploads a PDF file through the web interface
2. The application reads the file binary content
3. Encodes the content to a base64 string
4. Displays the result page with:
   - Live PDF preview (embedded in browser)
   - Complete base64 string (with copy-to-clipboard functionality)
   - Download link for the decoded PDF

### XML Upload Process
1. User uploads an XML file containing embedded PDF data
2. The application searches for base64 content within specific XML tags:
   ```xml
   <text mediaType="application/pdf" representation="B64">
   [base64 encoded PDF data]
   </text>
   ```
3. Extracts the base64 string from between the tags
4. Decodes and displays the PDF with the same features as PDF upload

## Why This Application?

### Use Cases
- **Healthcare Systems Integration**: Many healthcare standards (like HL7 CDA) embed PDF documents as base64 strings within XML structures. This tool helps developers and integrators quickly extract and verify these embedded PDFs.
- **Document Management**: Useful for systems that store PDFs as base64 strings in databases or configuration files.
- **API Testing & Debugging**: Quickly encode PDFs for API payloads or decode base64 responses to verify content.
- **Data Migration**: Extract PDFs from legacy XML-based document systems.
- **Development Tool**: Avoid command-line tools - get instant visual feedback with browser-based PDF preview.

### Benefits
- No command-line knowledge required
- Instant visual verification with embedded PDF preview
- Copy base64 strings directly to clipboard
- Web-based - accessible from any device
- Free and open-source

## Technology Stack

- **Flask 3.0.3** - Lightweight Python web framework
- **Gunicorn 23.0.0** - Production WSGI server for deployment
- **Python Standard Library**:
  - `base64` - Encoding/decoding binary data
  - `io` - Handling file streams and BytesIO objects
  - `secrets` - Generating secure session keys

## Installation & Setup

### Prerequisites
- Python 3.8+ (for local development)
- pip (Python package manager)
- **Optional**: Docker & Docker Compose (for containerized deployment)

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/ddeveloper72/pdf-base64-xml.git
   cd pdf-base64-xml
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

### Docker Deployment

Run the application using Docker:

1. **Using Docker Compose** (recommended):
   ```bash
   docker-compose up -d
   ```

2. **Using Docker directly**:
   ```bash
   # Build the image
   docker build -t pdf-base64-xml .
   
   # Run the container
   docker run -d -p 5000:5000 --name pdf-base64-xml pdf-base64-xml
   ```

3. Access the application at `http://localhost:5000`

4. **Stop the container**:
   ```bash
   docker-compose down  # If using docker-compose
   docker stop pdf-base64-xml  # If using docker run
   ```

### Deployment

The application is configured for multiple deployment options:

- **Heroku**: Uses the included `Procfile`
- **Docker**: Deploy the container to any platform (Azure Container Apps, AWS ECS, Google Cloud Run, etc.)

Set environment variables for `IP` and `PORT` as needed for your deployment platform.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Displays the file upload form |
| `/` | POST | Handles file upload and processing |
| `/serve_pdf` | POST | Serves decoded PDF files to the browser |

## Error Handling

The application includes comprehensive error handling:
- **File validation**: Ensures proper file extensions (.pdf or .xml)
- **XML parsing**: Validates presence of required base64 tags
- **404 & 500 errors**: Custom error pages with user-friendly messages
- **Flash messages**: Real-time feedback for user actions

## Security Features

- Secure session key generation using `secrets.token_hex()`
- File type validation to prevent malicious uploads
- Server-side processing only - no file storage

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for use and modification.

## Author

Created by **Duncan Falconer**

- GitHub: [@ddeveloper72](https://github.com/ddeveloper72)
- LinkedIn: [Duncan Falconer](https://www.linkedin.com/in/duncanfalconer/)
