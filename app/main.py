from fastapi import FastAPI
from app.modules.check_ngo_service.router import check_ngo_service_router
from app.modules.generate_campaigns.router import campaigns_router
from app.modules.selected_campaigns.router import selected_campaign_router

app = FastAPI(
    title="CSR_AGENT",
    description="Corportae Social Responsibility (CSR) AI Agent.",
    version="v1",
)

app.include_router(router=check_ngo_service_router,prefix="/api/{version}")
app.include_router(router=campaigns_router,prefix="/api/{version}")
app.include_router(router=selected_campaign_router,prefix="/api/{version}")
#app.include_router(router=recommended_volunteer_services_router,prefix="/api/{version}") 

