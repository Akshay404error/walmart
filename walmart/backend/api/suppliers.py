from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from services.supplier_service import SupplierService
from services.notification_service import NotificationService
from models.supplier_models import SupplierOrder, ForecastShare, SupplierResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
supplier_service = SupplierService()
notification_service = NotificationService()

@router.post("/orders/create", response_model=Dict[str, Any])
async def create_supplier_order(
    order: SupplierOrder,
    background_tasks: BackgroundTasks
):
    """
    Create a new supplier order
    """
    try:
        logger.info(f"Creating order for supplier {order.supplier_id}")
        
        # Create order
        order_info = await supplier_service.create_order(order)
        
        # Add notification task
        background_tasks.add_task(
            notification_service.notify_supplier_order,
            order.supplier_id,
            order_info["order_id"]
        )
        
        return {
            "message": "Supplier order created successfully",
            "order_id": order_info["order_id"],
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error creating supplier order: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders/{supplier_id}")
async def get_supplier_orders(
    supplier_id: str,
    status: Optional[str] = None,
    limit: int = 50
):
    """
    Get orders for a specific supplier
    """
    try:
        orders = await supplier_service.get_supplier_orders(
            supplier_id=supplier_id,
            status=status,
            limit=limit
        )
        return {
            "supplier_id": supplier_id,
            "orders": orders,
            "total_orders": len(orders),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching supplier orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/forecast/share", response_model=Dict[str, Any])
async def share_forecast_with_supplier(
    forecast: ForecastShare,
    background_tasks: BackgroundTasks
):
    """
    Share demand forecast with suppliers for early planning
    """
    try:
        logger.info(f"Sharing forecast with supplier {forecast.supplier_id}")
        
        # Share forecast
        share_info = await supplier_service.share_forecast(forecast)
        
        # Add notification task
        background_tasks.add_task(
            notification_service.notify_forecast_share,
            forecast.supplier_id,
            share_info["forecast_id"]
        )
        
        return {
            "message": "Forecast shared successfully",
            "forecast_id": share_info["forecast_id"],
            "supplier_id": forecast.supplier_id,
            "shared_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error sharing forecast: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/orders/{order_id}/respond")
async def supplier_order_response(
    order_id: str,
    response: SupplierResponse
):
    """
    Handle supplier response to an order
    """
    try:
        await supplier_service.process_order_response(order_id, response)
        return {
            "message": "Order response processed successfully",
            "order_id": order_id,
            "response_status": response.status,
            "processed_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error processing order response: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/forecasts/{supplier_id}")
async def get_supplier_forecasts(
    supplier_id: str,
    time_period: str = "30d"
):
    """
    Get forecasts shared with a supplier
    """
    try:
        forecasts = await supplier_service.get_supplier_forecasts(
            supplier_id=supplier_id,
            time_period=time_period
        )
        return {
            "supplier_id": supplier_id,
            "forecasts": forecasts,
            "total_forecasts": len(forecasts),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching supplier forecasts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/commitment/pre-commit")
async def request_pre_commitment(
    supplier_id: str,
    product_ids: List[str],
    quantities: List[int],
    commitment_date: str
):
    """
    Request pre-commitment from supplier for future orders
    """
    try:
        commitment = await supplier_service.request_pre_commitment(
            supplier_id, product_ids, quantities, commitment_date
        )
        return {
            "message": "Pre-commitment request sent",
            "commitment_id": commitment["commitment_id"],
            "supplier_id": supplier_id,
            "requested_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error requesting pre-commitment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/commitments/{supplier_id}")
async def get_supplier_commitments(supplier_id: str):
    """
    Get pre-commitments for a supplier
    """
    try:
        commitments = await supplier_service.get_supplier_commitments(supplier_id)
        return {
            "supplier_id": supplier_id,
            "commitments": commitments,
            "total_commitments": len(commitments),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching commitments: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/notifications/send")
async def send_supplier_notification(
    supplier_id: str,
    message: str,
    notification_type: str,
    background_tasks: BackgroundTasks
):
    """
    Send notification to supplier
    """
    try:
        background_tasks.add_task(
            notification_service.send_supplier_notification,
            supplier_id,
            message,
            notification_type
        )
        
        return {
            "message": "Supplier notification sent",
            "supplier_id": supplier_id,
            "notification_type": notification_type,
            "sent_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error sending supplier notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance/metrics")
async def get_supplier_performance_metrics(
    supplier_id: Optional[str] = None,
    start_date: str = None,
    end_date: str = None
):
    """
    Get supplier performance metrics
    """
    try:
        metrics = await supplier_service.get_performance_metrics(
            supplier_id=supplier_id,
            start_date=start_date,
            end_date=end_date
        )
        return {
            "metrics": metrics,
            "period": f"{start_date} to {end_date}" if start_date and end_date else "All time",
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching performance metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/collaboration/insights")
async def get_collaboration_insights(
    supplier_id: Optional[str] = None
):
    """
    Get collaboration insights and recommendations
    """
    try:
        insights = await supplier_service.get_collaboration_insights(supplier_id)
        return {
            "insights": insights,
            "supplier_id": supplier_id,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching collaboration insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/blockchain/order-trace")
async def create_blockchain_order_trace(
    order_id: str,
    supplier_id: str,
    trace_data: Dict[str, Any]
):
    """
    Create blockchain trace for order transparency
    """
    try:
        trace = await supplier_service.create_blockchain_trace(
            order_id, supplier_id, trace_data
        )
        return {
            "message": "Blockchain trace created",
            "trace_id": trace["trace_id"],
            "order_id": order_id,
            "blockchain_hash": trace["hash"],
            "created_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error creating blockchain trace: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/blockchain/traces/{order_id}")
async def get_order_blockchain_traces(order_id: str):
    """
    Get blockchain traces for an order
    """
    try:
        traces = await supplier_service.get_order_traces(order_id)
        return {
            "order_id": order_id,
            "traces": traces,
            "total_traces": len(traces),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching blockchain traces: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 