from fastapi import responses, Security, Depends, HTTPException
from requests import patch
from sqlmodel import Session
from sqlalchemy import text
from .database import engine, contract_engine
from .routers import patients,pharmacies,transactions


app.include_router(patients.router)
app.include_router(pharmacies.router)
app.include_router(transactions.router)


@app.get(
    '/',
    include_in_schema=False,
    tags=["HEALTHZ"])
def read_root():
    return "It works."


@app.get(
    "/healthz/liveness",
    include_in_schema=False,
    tags=["HEALTHZ"])
def healthz_liveness():
    return {}


@app.get(
    "/healthz/readiness",
    include_in_schema=False,
    tags=["HEALTHZ"])
def healthz_readiness():
    with engine.connect() as connection:
        results = connection.execute(
            text('SELECT GETDATE() AS STATUS;'))
        row = results.fetchone()
    with contract_engine.connect() as conn:
        contract_results = conn.execute(
            text('SELECT GETDATE() AS STATUS;'))
        contract_row = contract_results.fetchone()
    return [row, contract_row]
