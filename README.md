# AI-Powered RFP Processing System

This project uses Google's Gemini LLM to analyze Request for Proposal (RFP) documents, match them with products from a catalog, and generate bids with explainable AI reasoning.

## Prerequisites

- Python 3.8+
- A Google Gemini API Key ([Get one here](https://aistudio.google.com/))

## Setup Instructions

### 1. Installation

Clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configuration

1.  Create a `.env` file in the root directory (you can copy the example):
    ```bash
    # Windows
    copy .env.example .env
    
    # Linux/Mac
    cp .env.example .env
    ```
2.  Open `.env` and paste your Google Gemini API key:
    ```
    GEMINI_API_KEY=your_actual_api_key_here
    ```

### 3. Running the Application

Start the backend server:

```bash
python main.py
```

The API will be available at `http://localhost:8000`.
API Documentation (Swagger UI): `http://localhost:8000/docs`

### 4. Verification

To verify that the LLM integration is working correctly, run the included test script in a separate terminal while the server is running:

```bash
python test_llm.py
```

## Troubleshooting

- **ModuleNotFoundError: No module named 'numpy'**:
  Ensure you have installed all dependencies: `pip install -r requirements.txt`.
- **LLM/API Errors**:
  Check that your `GEMINI_API_KEY` in `.env` is valid and has not expired.
