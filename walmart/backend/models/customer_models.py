from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum

class NotificationType(str, Enum):
    PREORDER_CONFIRMATION = "preorder_confirmation"
    COMING_SOON = "coming_soon"
    AVAILABILITY_ALERT = "availability_alert"
    MARKDOWN_ALERT = "markdown_alert"
    GENERAL = "general"

class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"

class PreOrderRequest(BaseModel):
    customer_id: str = Field(..., description="Customer ID")
    product_id: str = Field(..., description="Product ID")
    store_id: str = Field(..., description="Store ID")
    quantity: int = Field(..., ge=1, description="Quantity to pre-order")
    expected_availability: date = Field(..., description="Expected availability date")

class NotificationRequest(BaseModel):
    customer_ids: List[str] = Field(..., description="List of customer IDs")
    message: str = Field(..., min_length=1, description="Notification message")
    notification_type: NotificationType = Field(..., description="Type of notification")
    channel: NotificationChannel = Field(default=NotificationChannel.EMAIL, description="Notification channel")

class CustomerPreferences(BaseModel):
    email_notifications: bool = Field(default=True, description="Enable email notifications")
    sms_notifications: bool = Field(default=False, description="Enable SMS notifications")
    push_notifications: bool = Field(default=True, description="Enable push notifications")
    preorder_alerts: bool = Field(default=True, description="Enable pre-order alerts")
    coming_soon_alerts: bool = Field(default=True, description="Enable coming soon alerts")
    markdown_alerts: bool = Field(default=True, description="Enable markdown alerts")
    frequency: str = Field(default="daily", description="Notification frequency")

class PreOrder(BaseModel):
    preorder_id: str
    customer_id: str
    product_id: str
    store_id: str
    quantity: int
    status: str = Field(default="pending", description="Pre-order status")
    created_at: datetime
    expected_availability: date
    fulfilled_at: Optional[datetime] = None

class ComingSoonInterest(BaseModel):
    interest_id: str
    customer_id: str
    product_id: str
    store_id: str
    registered_at: datetime
    notified: bool = Field(default=False, description="Whether customer has been notified")

class DemandLock(BaseModel):
    lock_id: str
    customer_id: str
    product_id: str
    quantity: int
    created_at: datetime
    expires_at: datetime
    status: str = Field(default="active", description="Lock status")

class CustomerEngagementMetrics(BaseModel):
    customer_id: str
    total_preorders: int
    total_notifications_received: int
    notification_open_rate: float = Field(..., ge=0.0, le=1.0)
    engagement_score: float = Field(..., ge=0.0, le=1.0)
    last_activity: datetime
    preferences: CustomerPreferences 