
# AI Groundwater Information Assistant

An AI-powered application that answers groundwater-related questions using information extracted from a groundwater PDF report.

## Features
- Upload and process groundwater PDF reports
- Extract and split PDF text into chunks
- Retrieve relevant information using TF-IDF and FAISS
- Generate answers using Ollama and Qwen 2.5:3B
- Display source page references

## Technologies Used
- Python 3.11
- Streamlit
- FAISS
- Scikit-learn
- Ollama
- Qwen 2.5:3B
- PyPDF

## Installation

1. Clone this repository.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install Ollama and download the model:

```bash
ollama pull qwen2.5:3b
```

4. Place your groundwater PDF at `data/groundwater_report.pdf`.
5. Build the database:

```bash
python -m modules.build_database
```

6. Start the application:

```bash
python -m streamlit run app.py
```

## Project Group
OJ16

## Project Topic
P16 – AI Groundwater Information Assistant
 