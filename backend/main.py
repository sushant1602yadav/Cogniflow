
from fastapi import FastAPI

from backend.api.actions import router as actions_router
from backend.api.tickets import router as tickets_router
from backend.api.policy import router as policy_router
from backend.api.approvals import router as approvals_router
from backend.api.audit import router as audit_router
from backend.api.agent import router as agent_router

# Import database models before creating tables
from backend.database.db import Base, engine
from backend.models.ticket import Ticket
from backend.models.approval import Approval
from backend.models.audit_log import AuditLog


# Create all registered database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Cogniflow API",
    description="Intelligent Business Workflows & Autonomous AI Platform",
    version="0.1.0",
)


# Register API routers
app.include_router(tickets_router)
app.include_router(policy_router)
app.include_router(approvals_router)
app.include_router(actions_router)
app.include_router(audit_router)
app.include_router(agent_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Cogniflow API",
        "status": "running",
    }
