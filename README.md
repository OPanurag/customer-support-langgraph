# Customer Support LangGraph

**Customer Support LangGraph** is a modular and extensible pipeline for handling customer support queries. It processes incoming requests, extracts relevant information, retrieves answers from a knowledge base, and generates responses. The project is designed to be easily extensible and integrates with external systems for advanced functionality.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Testing](#testing)
- [License](#license)

---

## Features

- **Pipeline-Oriented Design**: Modular pipeline stages for processing customer queries.
- **Knowledge Base Integration**: Retrieve answers from a pre-defined knowledge base.
- **Entity Extraction**: Extract structured information from unstructured queries.
- **Extensibility**: Easily add new abilities or modify existing ones.
- **Logging**: Built-in logging for debugging and monitoring.
- **Web Interface**: A simple frontend for interacting with the system.

---

## Project Structure
. ├── config/ 
  │ └── stages.yaml # Configuration for pipeline stages 
  ├── data/ 
  │ ├── kb_faq.json # Knowledge base data 
  │ └── chroma/ # Chroma database files 
  ├── logs/ 
  │ └── pipeline.log # Log file for pipeline execution 
  ├── pipeline/ 
  │ └── abilities/ # Core abilities for the pipeline 
  │ └── knowledge_base_search.py 
  ├── scripts/ 
  │ ├── kb_ingest.py # Script for ingesting KB data 
  │ └── run.sh # Shell script for running the project 
  ├── src/langie/ # Main source code 
  │ ├── main.py # Entry point for the application 
  │ ├── abilities.py # Core abilities module 
  │ ├── cli.py # Command-line interface 
  │ ├── logger.py # Logging utilities 
  │ ├── mcp_client.py # MCP client routing logic 
  │ ├── models.py # Data models 
  │ ├── pipeline.py # Pipeline orchestration 
  │ └── retriever.py # Data retrieval logic 
  ├── static/ 
  │ └── index.html # Frontend for KB search 
  ├── tests/ 
  │ ├── test_pipeline.py # Unit tests for the pipeline 
  │ └── test_retriever.py # Unit tests for the retriever 
  ├── LICENSE # License file 
  ├── README.md # Project documentation 
  ├── requirements.txt # Python dependencies 
  └── pyproject.toml # Project metadata and build configuration


---

## File Descriptions

### **config/**

- **`stages.yaml`**: Defines the configuration for the pipeline stages, including the order of execution and parameters for each stage.

### **data/**

- **`kb_faq.json`**: Contains the knowledge base data in JSON format. This is used to retrieve answers to customer queries.
- **`chroma/`**: Stores the Chroma database files for efficient data retrieval.

### **logs/**

- **`pipeline.log`**: Stores logs generated during the execution of the pipeline for debugging and monitoring.

### **pipeline/abilities/**

- **`knowledge_base_search.py`**: Implements the logic for searching the knowledge base and retrieving relevant answers.

### **scripts/**

- **`kb_ingest.py`**: Script for ingesting knowledge base data into the system.
- **`run.sh`**: Shell script for running the project.

### **src/langie/**

- **`__main__.py`**: The entry point for the application. It initializes and runs the pipeline.
- **`abilities.py`**: Contains the core abilities (functions) used in the pipeline, such as entity extraction, query parsing, and response generation.
- **`cli.py`**: Implements a command-line interface for interacting with the system.
- **`logger.py`**: Provides logging utilities for the application.
- **`mcp_client.py`**: Handles MCP client routing logic for integrating with external systems.
- **`models.py`**: Defines data models used throughout the application.
- **`pipeline.py`**: Orchestrates the execution of the pipeline stages.
- **`retriever.py`**: Implements the logic for retrieving data from the knowledge base.

### **static/**

- **`index.html`**: A simple web interface for interacting with the knowledge base search functionality.

### **tests/**

- **`test_pipeline.py`**: Unit tests for the pipeline orchestration logic.
- **`test_retriever.py`**: Unit tests for the data retrieval logic.

### **Other Files**

- **`LICENSE`**: Specifies the license under which the project is distributed.
- **`README.md`**: Provides documentation for the project.
- **`requirements.txt`**: Lists the Python dependencies required for the project.
- **`pyproject.toml`**: Contains metadata and build configuration for the project.

---

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/customer-support-langgraph.git
   cd customer-support-langgraph
   ```
2.  Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```

---
Usage
Running the Application
1. Ingest Knowledge Base Data:
```
python scripts/kb_ingest.py
```
2. Start the Application:
```
python -m src.langie
```
3. Access the Web Interface: Open static/index.html in your browser to interact with the KB search.

---
Configuration
1. Pipeline Stages: Configure the pipeline stages in config/stages.yaml.
2. Knowledge Base: Update or replace the KB data in data/kb_faq.json.

---
Testing
Run the unit tests to ensure everything is working correctly:
```
pytest
```

---
License
This project is licensed under the MIT License. See the LICENSE file for details.

---

### Explanation of Each File

#### **Core Files**
- **`abilities.py`**: Contains the main functions (abilities) for processing customer queries, such as parsing requests, extracting entities, and generating responses.
- **`pipeline.py`**: Orchestrates the execution of the pipeline stages, ensuring that each ability is executed in the correct order.
- **`retriever.py`**: Handles the logic for retrieving data from the knowledge base.

#### **Scripts**
- **`kb_ingest.py`**: Prepares and ingests the knowledge base data into the system.
- **`run.sh`**: A convenience script for running the project.

#### **Frontend**
- **`index.html`**: Provides a simple web interface for interacting with the system.

#### **Tests**
- **[test_pipeline.py](http://_vscodecontentref_/7)**: Tests the pipeline orchestration logic.
- **[test_retriever.py](http://_vscodecontentref_/8)**: Tests the data retrieval functionality.

Let me know if you need further clarification