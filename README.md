# SQL-Agent

## Overview
SQL-Agent is a Python-based tool designed to perform similarity searches on a database of documents containing frequently asked questions (FAQs) or similar content. By retrieving relevant documents, SQL-Agent reduces hallucinations and improves the accuracy of AI-generated responses. The tool is ideal for enhancing the reliability of language model outputs by providing contextually relevant information from trusted sources.

---

## Features

- **Similarity Search**: Efficiently searches for documents with questions similar to the input query.
- **Reduced Hallucinations**: Minimizes errors in AI-generated responses by providing factual references.
- **Seamless Database Integration**: Connects to PostgreSQL databases for storing and retrieving documents.
- **Customizable**: Easily adaptable to different datasets and configurations.

---

## Requirements
The following Python libraries are required to run SQL-Agent:

- `python-dotenv`: For managing environment variables.
- `langchain_openai`: Integration with OpenAI's language models.
- `langchain_community`: Community-driven tools for LangChain.
- `langchain_core`: Core LangChain functionalities.
- `langchain_experimental`: Experimental features for LangChain.
- `psycopg2-binary`: PostgreSQL database adapter for Python.
- `google_search_results`: API for Google Search integration.

To install the dependencies, run:
```bash
pip install -r requirements.txt
```

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/PragalvhaSharma/SQL-Agent.git
   ```
2. Navigate to the project directory:
   ```bash
   cd SQL-Agent
   ```
3. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Environment Setup**:
   Create a `.env` file in the project directory with the following variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

2. **Database Configuration**:
   Ensure your PostgreSQL database is set up and populated with the required documents. Use the provided SQL schema (if available) to structure your database correctly.

3. **Running the Script**:
   Execute the main Python script to start the similarity search:
   ```bash
   python main.py
   ```

4. **Query Example**:
   Input a question or query, and the system will retrieve similar documents from the database to enhance the response quality.

---

## Contributing
Contributions are welcome! If you have ideas, suggestions, or bug fixes, please open an issue or submit a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For questions or support, contact [Pragalvha Sharma](mailto:pragalvhasharma@gmail.com).

---

## Acknowledgments
Special thanks to the LangChain community and contributors for providing tools that made this project possible.

