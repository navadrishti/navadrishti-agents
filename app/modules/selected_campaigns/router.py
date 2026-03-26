from fastapi import APIRouter, HTTPException, status
from app.modules.selected_campaigns.schema import SelectedCampaignIn, SelectedCampaignResponse, UpdateSelectedCampaign
from app.modules.selected_campaigns.service import SelectedCampaignsService

selected_campaign_router = APIRouter(
    prefix="/selected-campaign",
    tags=["Selected Campaign"],
)

sc_service = SelectedCampaignsService()

@selected_campaign_router.post("/save_campaign", response_model=SelectedCampaignResponse)
async def store_campaign(req: SelectedCampaignIn) -> SelectedCampaignResponse:
    try:
        inserted = sc_service.store_selected_campaign(
            campaign=req.campaign.model_dump(),
            company_id=req.company_id
        )
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save campaign") from exc

    return SelectedCampaignResponse(
        id=inserted["id"],
        title=inserted["title"],
        status=inserted["status"],
        message="Campaign saved successfully"
    )


@selected_campaign_router.put("/update_campaign/{campaign_id}")
async def update_campaign(req: UpdateSelectedCampaign) -> SelectedCampaignResponse:
    updates = {}
    if req.campaign is not None:
        updates = req.campaign.model_dump(exclude_none=True, exclude_unset=True)

    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")

    try:
        updated = sc_service.update_selected_campaign(
            campaign_id=req.campaign_id,
            updates=updates,
            company_id=req.company_id
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to update campaign") from exc

    return SelectedCampaignResponse(
        id=updated["id"],
        title=updated["title"],
        status=updated["status"],
        message="Campaign updated successfully"
    )