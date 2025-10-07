from fastapi import APIRouter
from app.models import DashboardStats
from app.sample_data import sample_dashboard_stats

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardStats)
async def get_dashboard_stats():
    """
    Get dashboard statistics including total income, expenses, net savings, and account balance.
    Returns data in camelCase format for frontend consumption.
    """
    return sample_dashboard_stats
