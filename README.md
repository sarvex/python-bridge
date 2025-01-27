# Bridge

Bridge is a metadata extraction and publishing service that scans Python codebases and publishes their metadata to the Mobius no-code/low-code platform.

## Features

- Recursive directory scanning for Python files
- Extracts metadata from Python code including:
  - Functions and their signatures
  - Classes and their methods
  - Docstrings and documentation
- FastAPI-powered REST API
- Extensible connector system for publishing metadata
- Clean and modular architecture

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
uvicorn bridge.main:app --reload
```

2. Send a POST request to `/scan-and-publish` endpoint:
```json
{
    "path": "/path/to/python/project",
    "mobius_url": "https://your-mobius-instance.com",
    "api_key": "your-api-key"  // Optional
}
```

## Project Structure

```
bridge/
├── bridge/
│   ├── core/
│   │   ├── scanning.py    # Code scanning functionality
│   │   └── metadata.py    # Metadata generation and processing
│   ├── connectors/
│   │   └── mobius.py      # Mobius platform connector
│   └── main.py            # FastAPI application and endpoints
├── requirements.txt
└── README.md
```

## Dependencies

- FastAPI: 0.115.7
- Uvicorn: 0.34.0
- Pydantic: 2.10.6

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.