from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from services.inventory_service import InventoryService
from models.inventory_models import InventoryStatus, ReorderRequest, ThresholdUpdate

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize inventory service
inventory_service = InventoryService()

@router.get("/status", response_model=List[InventoryStatus])
async def get_inventory_status(
    store_id: Optional[str] = None,
    category: Optional[str] = None,
    critical_only: bool = False
):
    """
    Get current inventory status for products
    """
    try:
        status = await inventory_service.get_inventory_status(
            store_id=store_id,
            category=category,
            critical_only=critical_only
        )
        return status
    except Exception as e:
        logger.error(f"Error fetching inventory status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reorder", response_model=Dict[str, Any])
async def generate_reorder_request(
    request: ReorderRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate automated reorder request based on dynamic thresholds
    """
    try:
        logger.info(f"Generating reorder request for {len(request.product_ids)} products")
        
        # Add to background tasks for processing
        background_tasks.add_task(
            inventory_service.process_reorder_request,
            request.product_ids,
            request.store_id,
            request.priority
        )
        
        return {
            "message": "Reorder request generated successfully",
            "request_id": f"ro_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "processing",
            "estimated_completion": datetime.now() + timedelta(minutes=2)
        }
    except Exception as e:
        logger.error(f"Error generating reorder request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/thresholds", response_model=List[Dict[str, Any]])
async def get_dynamic_thresholds(
    product_id: Optional[str] = None,
    store_id: Optional[str] = None
):
    """
    Get dynamic replenishment thresholds
    """
    try:
        thresholds = await inventory_service.get_dynamic_thresholds(
            product_id=product_id,
            store_id=store_id
        )
        return thresholds
    except Exception as e:
        logger.error(f"Error fetching thresholds: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/thresholds/update")
async def update_thresholds(request: ThresholdUpdate):
    """
    Update dynamic thresholds for products
    """
    try:
        await inventory_service.update_thresholds(
            request.product_id,
            request.store_id,
            request.new_threshold,
            request.reason
        )
        return {
            "message": "Thresholds updated successfully",
            "product_id": request.product_id,
            "store_id": request.store_id,
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error updating thresholds: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alerts/critical")
async def get_critical_alerts():
    """
    Get critical inventory alerts
    """
    try:
        alerts = await inventory_service.get_critical_alerts()
        return {
            "alerts": alerts,
            "count": len(alerts),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching critical alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/perishable/monitoring")
async def get_perishable_monitoring():
    """
    Get perishable item monitoring data
    """
    try:
        perishable_data = await inventory_service.get_perishable_monitoring()
        return {
            "perishable_items": perishable_data["items"],
            "expiring_soon": perishable_data["expiring_soon"],
            "markdown_candidates": perishable_data["markdown_candidates"],
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching perishable monitoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/perishable/markdown")
async def trigger_markdown(
    product_id: str,
    store_id: str,
    markdown_percentage: float,
    background_tasks: BackgroundTasks
):
    """
    Trigger automated markdown for perishable items
    """
    try:
        background_tasks.add_task(
            inventory_service.trigger_markdown,
            product_id,
            store_id,
            markdown_percentage
        )
        
        return {
            "message": "Markdown triggered successfully",
            "product_id": product_id,
            "store_id": store_id,
            "markdown_percentage": markdown_percentage,
            "triggered_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error triggering markdown: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/waste-reduction")
async def get_waste_reduction_analytics(
    start_date: str,
    end_date: str,
    store_id: Optional[str] = None
):
    """
    Get waste reduction analytics
    """
    try:
        analytics = await inventory_service.get_waste_reduction_analytics(
            start_date,
            end_date,
            store_id
        )
        return {
            "period": f"{start_date} to {end_date}",
            "waste_reduced": analytics["waste_reduced"],
            "cost_savings": analytics["cost_savings"],
            "sustainability_score": analytics["sustainability_score"],
            "details": analytics["details"]
        }
    except Exception as e:
        logger.error(f"Error fetching waste reduction analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/supplier/orders")
async def get_supplier_orders(
    supplier_id: Optional[str] = None,
    status: Optional[str] = None
):
    """
    Get supplier order history and status
    """
    try:
        orders = await inventory_service.get_supplier_orders(
            supplier_id=supplier_id,
            status=status
        )
        return {
            "orders": orders,
            "total_orders": len(orders),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching supplier orders: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 