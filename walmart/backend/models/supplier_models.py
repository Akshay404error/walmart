from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class SupplierOrder(BaseModel):
    supplier_id: str = Field(..., description="Supplier ID")
    product_ids: List[str] = Field(..., description="List of product IDs")
    quantities: List[int] = Field(..., description="Quantities for each product")
    store_id: str = Field(..., description="Store ID")
    expected_delivery_date: date = Field(..., description="Expected delivery date")
    priority: str = Field(default="medium", description="Order priority")
    special_instructions: Optional[str] = Field(None, description="Special instructions")
    auto_generated: bool = Field(default=True, description="Whether order was auto-generated")

class ForecastShare(BaseModel):
    supplier_id: str = Field(..., description="Supplier ID")
    product_ids: List[str] = Field(..., description="List of product IDs")
    forecast_period: str = Field(..., description="Forecast period")
    forecast_data: Dict[str, Any] = Field(..., description="Forecast data")
    shared_at: datetime = Field(default_factory=datetime.now, description="When forecast was shared")

class SupplierResponse(BaseModel):
    order_id: str = Field(..., description="Order ID")
    status: OrderStatus = Field(..., description="Response status")
    message: Optional[str] = Field(None, description="Response message")
    expected_delivery_date: Optional[date] = Field(None, description="Updated delivery date")
    partial_fulfillment: Optional[Dict[str, int]] = Field(None, description="Partial fulfillment quantities")

class PreCommitment(BaseModel):
    commitment_id: str
    supplier_id: str
    product_ids: List[str]
    quantities: List[int]
    commitment_date: date
    status: str = Field(default="pending", description="Commitment status")
    created_at: datetime
    confirmed_at: Optional[datetime] = None

class SupplierPerformance(BaseModel):
    supplier_id: str
    on_time_delivery_rate: float = Field(..., ge=0.0, le=1.0)
    quality_score: float = Field(..., ge=0.0, le=1.0)
    cost_efficiency: float = Field(..., ge=0.0, le=1.0)
    collaboration_score: float = Field(..., ge=0.0, le=1.0)
    total_orders: int
    average_response_time: float  # in hours
    last_updated: datetime

class BlockchainTrace(BaseModel):
    trace_id: str
    order_id: str
    supplier_id: str
    block_hash: str
    transaction_data: Dict[str, Any]
    created_at: datetime
    verified: bool = Field(default=False, description="Whether trace has been verified")

class CollaborationInsight(BaseModel):
    insight_id: str
    supplier_id: str
    insight_type: str
    description: str
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    recommended_action: str
    generated_at: datetime 