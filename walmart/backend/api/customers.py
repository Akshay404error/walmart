from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from services.customer_service import CustomerService
from services.notification_service import NotificationService
from models.customer_models import PreOrderRequest, NotificationRequest, CustomerPreferences

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
customer_service = CustomerService()
notification_service = NotificationService()

@router.post("/preorder", response_model=Dict[str, Any])
async def create_preorder(
    request: PreOrderRequest,
    background_tasks: BackgroundTasks
):
    """
    Create a pre-order for seasonal products
    """
    try:
        logger.info(f"Creating pre-order for customer {request.customer_id}")
        
        # Create pre-order
        preorder = await customer_service.create_preorder(
            customer_id=request.customer_id,
            product_id=request.product_id,
            store_id=request.store_id,
            quantity=request.quantity,
            expected_availability=request.expected_availability
        )
        
        # Add notification task
        background_tasks.add_task(
            notification_service.send_preorder_confirmation,
            request.customer_id,
            preorder["preorder_id"]
        )
        
        return {
            "message": "Pre-order created successfully",
            "preorder_id": preorder["preorder_id"],
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error creating pre-order: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preorders/{customer_id}")
async def get_customer_preorders(customer_id: str):
    """
    Get all pre-orders for a customer
    """
    try:
        preorders = await customer_service.get_customer_preorders(customer_id)
        return {
            "customer_id": customer_id,
            "preorders": preorders,
            "total_preorders": len(preorders),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching pre-orders: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/notify", response_model=Dict[str, Any])
async def send_notification(
    request: NotificationRequest,
    background_tasks: BackgroundTasks
):
    """
    Send notification to customers
    """
    try:
        logger.info(f"Sending notification to {len(request.customer_ids)} customers")
        
        # Add to background tasks for processing
        background_tasks.add_task(
            notification_service.send_bulk_notifications,
            request.customer_ids,
            request.message,
            request.notification_type,
            request.channel
        )
        
        return {
            "message": "Notifications queued for sending",
            "notification_id": f"not_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "recipient_count": len(request.customer_ids),
            "status": "queued",
            "estimated_completion": datetime.now() + timedelta(minutes=1)
        }
    except Exception as e:
        logger.error(f"Error sending notifications: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/notifications/history")
async def get_notification_history(
    customer_id: Optional[str] = None,
    notification_type: Optional[str] = None,
    limit: int = 50
):
    """
    Get notification history
    """
    try:
        history = await notification_service.get_notification_history(
            customer_id=customer_id,
            notification_type=notification_type,
            limit=limit
        )
        return {
            "notifications": history,
            "total_count": len(history),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching notification history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/preferences/update")
async def update_customer_preferences(
    customer_id: str,
    preferences: CustomerPreferences
):
    """
    Update customer notification preferences
    """
    try:
        await customer_service.update_preferences(customer_id, preferences)
        return {
            "message": "Preferences updated successfully",
            "customer_id": customer_id,
            "updated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error updating preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preferences/{customer_id}")
async def get_customer_preferences(customer_id: str):
    """
    Get customer notification preferences
    """
    try:
        preferences = await customer_service.get_preferences(customer_id)
        return {
            "customer_id": customer_id,
            "preferences": preferences,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/coming-soon/register")
async def register_coming_soon_interest(
    customer_id: str,
    product_id: str,
    store_id: str
):
    """
    Register customer interest in coming soon products
    """
    try:
        await customer_service.register_coming_soon_interest(
            customer_id, product_id, store_id
        )
        return {
            "message": "Interest registered successfully",
            "customer_id": customer_id,
            "product_id": product_id,
            "store_id": store_id,
            "registered_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error registering interest: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/coming-soon/interests")
async def get_coming_soon_interests(
    product_id: Optional[str] = None,
    store_id: Optional[str] = None
):
    """
    Get customer interests for coming soon products
    """
    try:
        interests = await customer_service.get_coming_soon_interests(
            product_id=product_id,
            store_id=store_id
        )
        return {
            "interests": interests,
            "total_interests": len(interests),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching interests: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/demand-lock")
async def lock_customer_demand(
    customer_id: str,
    product_id: str,
    quantity: int,
    lock_duration_days: int = 7
):
    """
    Lock customer demand for a specific period
    """
    try:
        lock_info = await customer_service.lock_demand(
            customer_id, product_id, quantity, lock_duration_days
        )
        return {
            "message": "Demand locked successfully",
            "lock_id": lock_info["lock_id"],
            "expires_at": lock_info["expires_at"],
            "quantity": quantity
        }
    except Exception as e:
        logger.error(f"Error locking demand: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/engagement")
async def get_customer_engagement_analytics(
    start_date: str,
    end_date: str,
    store_id: Optional[str] = None
):
    """
    Get customer engagement analytics
    """
    try:
        analytics = await customer_service.get_engagement_analytics(
            start_date, end_date, store_id
        )
        return {
            "period": f"{start_date} to {end_date}",
            "total_preorders": analytics["total_preorders"],
            "active_customers": analytics["active_customers"],
            "engagement_rate": analytics["engagement_rate"],
            "conversion_rate": analytics["conversion_rate"],
            "details": analytics["details"]
        }
    except Exception as e:
        logger.error(f"Error fetching engagement analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 