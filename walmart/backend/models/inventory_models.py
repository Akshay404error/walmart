from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum

class InventoryStatus(str, Enum):
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    OVERSTOCKED = "overstocked"

class ReorderPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThresholdType(str, Enum):
    REORDER_POINT = "reorder_point"
    SAFETY_STOCK = "safety_stock"
    MAX_STOCK = "max_stock"

class InventoryStatus(BaseModel):
    product_id: str
    store_id: str
    current_quantity: int = Field(..., ge=0)
    available_quantity: int = Field(..., ge=0)
    reserved_quantity: int = Field(..., ge=0)
    status: InventoryStatus
    last_updated: datetime
    days_of_inventory: float
    reorder_point: int
    safety_stock: int
    max_stock: int

class ReorderRequest(BaseModel):
    product_ids: List[str] = Field(..., description="List of product IDs to reorder")
    store_id: str = Field(..., description="Store ID")
    priority: ReorderPriority = Field(default=ReorderPriority.MEDIUM, description="Reorder priority")
    auto_approve: bool = Field(default=False, description="Auto-approve reorder")
    supplier_id: Optional[str] = Field(None, description="Preferred supplier ID")

class ThresholdUpdate(BaseModel):
    product_id: str
    store_id: str
    new_threshold: int = Field(..., ge=0)
    threshold_type: ThresholdType
    reason: str = Field(..., min_length=1)
    effective_date: datetime = Field(default_factory=datetime.now)

class PerishableItem(BaseModel):
    product_id: str
    store_id: str
    current_quantity: int
    expiry_date: date
    days_until_expiry: int
    markdown_percentage: Optional[float] = Field(None, ge=0.0, le=1.0)
    is_markdown_eligible: bool
    last_updated: datetime

class MarkdownTrigger(BaseModel):
    product_id: str
    store_id: str
    current_percentage: float = Field(..., ge=0.0, le=1.0)
    suggested_percentage: float = Field(..., ge=0.0, le=1.0)
    days_until_expiry: int
    expected_sales_boost: float
    risk_level: str
    triggered_at: datetime

class WasteReductionMetrics(BaseModel):
    period_start: date
    period_end: date
    store_id: Optional[str]
    total_waste_reduced: float
    cost_savings: float
    sustainability_score: float = Field(..., ge=0.0, le=1.0)
    items_saved: int
    carbon_footprint_reduction: float
    details: Dict[str, Any]

class SupplierOrder(BaseModel):
    supplier_id: str
    product_ids: List[str]
    quantities: List[int] = Field(..., description="Quantities for each product")
    store_id: str
    expected_delivery_date: date
    priority: ReorderPriority = Field(default=ReorderPriority.MEDIUM)
    special_instructions: Optional[str] = None
    auto_generated: bool = Field(default=True)

class InventoryAlert(BaseModel):
    alert_id: str
    product_id: str
    store_id: str
    alert_type: str
    severity: str
    message: str
    current_value: float
    threshold_value: float
    created_at: datetime
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None

class DynamicThreshold(BaseModel):
    product_id: str
    store_id: str
    threshold_type: ThresholdType
    current_value: int
    calculated_value: int
    factors: Dict[str, float]
    last_calculation: datetime
    next_calculation: datetime
    confidence_score: float = Field(..., ge=0.0, le=1.0)

class InventoryAnalytics(BaseModel):
    product_id: str
    store_id: str
    period: str
    turnover_rate: float
    stockout_frequency: float
    overstock_frequency: float
    forecast_accuracy: float = Field(..., ge=0.0, le=1.0)
    cost_of_carrying: float
    cost_of_stockout: float
    total_cost: float
    generated_at: datetime

class PerishableAnalytics(BaseModel):
    store_id: str
    period: str
    total_perishable_items: int
    expired_items: int
    markdown_items: int
    waste_percentage: float = Field(..., ge=0.0, le=1.0)
    revenue_recovery: float
    sustainability_score: float = Field(..., ge=0.0, le=1.0)
    top_perishable_categories: List[Dict[str, Any]]
    generated_at: datetime 