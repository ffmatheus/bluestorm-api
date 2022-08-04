from fastapi import FastAPI

#Start FastAPI application
app = FastAPI(
    title="Bluestorm-API",
    version="0.1.0",
    description="Management of pharmacies data and transactions",
    openapi_tags=[{
        "name": "Users",
        "description": "Manage users, login and get auth token"
    },
    {
        "name": "Patients",
        "description": "Manage patients, create, update, list and delete"
    },
    {
        "name": "Pharmacies",
        "description": "Manage pharmacies, create, update, list and delete"
    },
    {
        "name": "Transactions",
        "description": "Manage transactios, list and create"
    }
    ]
)
