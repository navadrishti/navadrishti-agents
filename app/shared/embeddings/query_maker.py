from app.modules.check_ngo_service.schema import CheckNGOServicesRequest
def make_query(payload: CheckNGOServicesRequest) -> str:
    return (
        f"CSR requirement for Category: {payload.category} in Location: {payload.location}. "
        f"Budget: {payload.budget}. "
        f"Timeline: {payload.timeline_start} to {payload.timeline_end}. "
        f"Milestones: {payload.milestones}. "
        f"Support beneficiaries under Category: {payload.category} in Location: {payload.location}."
 )