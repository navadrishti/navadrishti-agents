from fastapi import HTTPException, status
from app.shared.clients.supabase_client import supabase

class SelectedCampaignsService:
    def store_selected_campaign(self,campaign: dict, company_id: int) -> dict:

        result = supabase.table("campaigns").insert({
            "title":            campaign.get("title"),
            "description":      campaign.get("description"),
            "category":         campaign.get("category"),
            "location":         campaign.get("location"),
            "budget_inr":       campaign.get("budget_inr"),
            "budget_breakdown": campaign.get("budget_breakdown"),
            "schedule_vii":     campaign.get("schedule_vii"),
            "sdg_alignment":    campaign.get("sdg_alignment"),
            "impact_metrics":   campaign.get("impact_metrics"),
            "milestones":       campaign.get("milestones"),
            "start_date":       campaign.get("start_date"),
            "end_date":         campaign.get("end_date"),
            "company_id":       company_id,
            "status":           "draft"
        }).execute()
        #print(result)
        #print(result.data)
        if not result.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to insert campaign")
        return result.data[0]
        
    def update_selected_campaign(self, campaign_id: str, updates: dict, company_id: int) -> dict:

        current = supabase.table("campaigns").select("status").eq("id", campaign_id).eq("company_id", company_id).execute()
        if not current.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Campaign not found")
        if current.data[0]["status"] == "active":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot update an active campaign")

        result = (
            supabase.table("campaigns")
            .update(updates)
            .eq("id", campaign_id)
            .eq("company_id", company_id)
            .execute()
        )
        if not result.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update campaign")
        return result.data[0]
