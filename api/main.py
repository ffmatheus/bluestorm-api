from routers import patients, pharmacies, transactions, users
from init import app
import uvicorn

app.include_router(users.router)
app.include_router(patients.router)
app.include_router(pharmacies.router)
app.include_router(transactions.router)

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)