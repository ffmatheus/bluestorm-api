from routers.patients import router as  PatientsRouter
from routers.users import router as UsersRouter
from routers.pharmacies import router as PharmaciesRouter
from routers.transactions import router as TransactionsRouter
from start import app


app.include_router(UsersRouter)
app.include_router(PatientsRouter)
app.include_router(PharmaciesRouter)
app.include_router(TransactionsRouter)
