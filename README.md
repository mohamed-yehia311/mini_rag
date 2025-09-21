# Mini_RAG: Retrieval-Augmented Generation API Backend

Mini_RAG is a backend service built with FastAPI that implements Retrieval-Augmented Generation (RAG) workflows. It integrates document chunking, vector embeddings, semantic search, and large language models (LLMs) (e.g., OpenAI) to build intelligent search and chat capabilities over your data.

## Features

- **Retrieval-Augmented Generation (RAG):**  
  Combine document retrieval with generative models for enhanced Q&A and conversational AI.

- **REST API Endpoints:**  
  Endpoints for indexing (push), retrieving index information, searching, and answering questions.

- **Vector Database Integration:**  
  Uses Qdrant to store, index, and search vector embeddings of document chunks.

- **MongoDB:**  
  Uses MongoDB to store project metadata and document chunks.

- **LLM Integration:**  
  Connects with generation and embedding backends (e.g., OpenAI, Cohere) to generate embeddings and answers.

## Technologies

- Python & FastAPI  
- MongoDB  
- Qdrant  
- OpenAI & Cohere (for LLM and embeddings)  
- Pydantic (data validation)

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB instance running (default: `mongodb://localhost:27017/`)
- Qdrant instance (or local database file for Qdrant)
- API keys for OpenAI and/or Cohere (if used)

### Installation


1. **Clone the repository:**

   ```sh
   git clone https://github.com/<your-username>/mini_rag.git
   cd mini_rag
   ```

2. **Create a virtual environment and install dependencies:**

   ```sh
   python -m venv venv
   source venv/Scripts/activate   # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Install all required Python packages.**
    ```sh
    pip install -r requirments.txt
    ```
4. **Configure Environment Variables:**

   Create a `.env` file (or edit the existing one) with your settings. For example see the `.env.example`

### Running the Application

You can start the server using Uvicorn:

```sh
uvicorn main:app --reload
```

This will launch the FastAPI server with live reload enabled. Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API documentation.

## API Endpoints

Some of the key endpoints include:

- `POST /api/v1/chat/index/push/{project_id}`  
  Index document chunks into the vector database.

- `GET /api/v1/chat/index/info/{project_id}`  
  Retrieve vector database collection information for a project.

- `POST /api/v1/chat/index/search/{project_id}`  
  Search vectors in the database using a text query.

- `POST /api/v1/chat/index/answer/{project_id}`  
  Answer a question using RAG by retrieving relevant document chunks and generating an answer.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with proposed changes.

## License

[MIT License](LICENSE)

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Qdrant](https://qdrant.tech/)
- [OpenAI](https://openai.com/)
- [MongoDB](https://www.mongodb.com/)
