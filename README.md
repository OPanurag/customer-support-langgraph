# customer-support-langgraph
Graph-based customer support agent built with Lang Graph orchestration, state persistence, and MCP client routing across Atlas and Common servers.


.
├── .gitignore
├── LICENSE
├── README.md
├── config/
│   └── stages.yaml
├── data/
│   └── kb_faq.json
├── pyproject.toml
├── requirements.txt
├── sample.json
├── scripts/
│   └── run.sh
├── src/langie/
│   ├── __init__.py
│   ├── __main__.py
│   ├── abilities.py
│   ├── cli.py
│   ├── logger.py
│   ├── mcp_client.py
│   ├── models.py
│   ├── pipeline.py
│   └── retriever.py
├── test_pipeline.py
└── test_retriever.py
