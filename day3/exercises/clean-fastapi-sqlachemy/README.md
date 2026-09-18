## Project Directory Architecture

day3-clean-fastapi/
├── app/
│   ├── domain/                  # PURE PYTHON: Entities & Protocols (Zero Framework Imports)
│   │   ├── models.py
│   │   └── repositories.py
│   ├── application/             # USE CASES: Orchestrates business workflows
│   │   └── use_cases.py
│   ├── infrastructure/          # ADAPTERS: SQLAlchemy ORM & DB drivers
│   │   ├── db.py
│   │   ├── models.py
│   │   └── repositories.py
│   └── api/                     # DELIVERY: FastAPI Routes & Pydantic Schemas
│       ├── schemas.py
│       ├── dependencies.py
│       └── routers.py
├── main.py                      # Application Entrypoint
└── pyproject.toml