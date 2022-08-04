from api.routers.patients import router as UsersRouter
from api.routers.users import router as PatientsRouter
from api.routers.pharmacies import router as PharmaciesRouter
from api.routers.transactions import router as TransactionsRouter
from api.init import app


app.include_router(UsersRouter)
app.include_router(PatientsRouter)
app.include_router(PharmaciesRouter)
app.include_router(TransactionsRouter)
