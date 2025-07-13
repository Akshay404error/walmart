import asyncio
import logging
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
import numpy as np

from models.supplier_models import (
    SupplierOrder, ForecastShare, SupplierResponse, PreCommitment,
    SupplierPerformance, BlockchainTrace, CollaborationInsight
)

logger = logging.getLogger(__name__)

class SupplierService:
    def __init__(self):
        self.orders = []
        self.forecasts = []
        self.commitments = []
        self.blockchain_traces = []
        
    async def create_order(self, order: SupplierOrder) -> Dict[str, Any]:
        """Create a new supplier order"""
        try:
            logger.info(f"Creating order for supplier {order.supplier_id}")
            
            # Generate order ID
            order_id = f"ORD_{len(self.orders):06d}"
            
            # Create order record
            order_record = {
                "order_id": order_id,
                "supplier_id": order.supplier_id,
                "product_ids": order.product_ids,
                "quantities": order.quantities,
                "store_id": order.store_id,
                "expected_delivery_date": order.expected_delivery_date,
                "priority": order.priority,
                "special_instructions": order.special_instructions,
                "auto_generated": order.auto_generated,
                "status": "pending",
                "created_at": datetime.now(),
                "total_value": sum(q * np.random.uniform(10, 50) for q in order.quantities)
            }
            
            self.orders.append(order_record)
            
            return {
                "order_id": order_id,
                "status": "created",
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating supplier order: {e}")
            raise
    
    async def get_supplier_orders(
        self,
        supplier_id: str,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get orders for a specific supplier"""
        try:
            supplier_orders = [
                o for o in self.orders if o["supplier_id"] == supplier_id
            ]
            
            if status:
                supplier_orders = [o for o in supplier_orders if o["status"] == status]
            
            # Return limited results
            return supplier_orders[-limit:]
            
        except Exception as e:
            logger.error(f"Error getting supplier orders: {e}")
            raise
    
    async def share_forecast(self, forecast: ForecastShare) -> Dict[str, Any]:
        """Share demand forecast with suppliers for early planning"""
        try:
            logger.info(f"Sharing forecast with supplier {forecast.supplier_id}")
            
            # Generate forecast ID
            forecast_id = f"FCST_{len(self.forecasts):06d}"
            
            # Create forecast record
            forecast_record = {
                "forecast_id": forecast_id,
                "supplier_id": forecast.supplier_id,
                "product_ids": forecast.product_ids,
                "forecast_period": forecast.forecast_period,
                "forecast_data": forecast.forecast_data,
                "shared_at": forecast.shared_at,
                "status": "shared"
            }
            
            self.forecasts.append(forecast_record)
            
            return {
                "forecast_id": forecast_id,
                "status": "shared",
                "shared_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error sharing forecast: {e}")
            raise
    
    async def process_order_response(self, order_id: str, response: SupplierResponse):
        """Handle supplier response to an order"""
        try:
            logger.info(f"Processing response for order {order_id}")
            
            # Find the order
            order = next((o for o in self.orders if o["order_id"] == order_id), None)
            
            if not order:
                raise ValueError(f"Order {order_id} not found")
            
            # Update order status
            order["status"] = response.status
            order["response_message"] = response.message
            order["updated_delivery_date"] = response.expected_delivery_date
            order["partial_fulfillment"] = response.partial_fulfillment
            order["responded_at"] = datetime.now()
            
        except Exception as e:
            logger.error(f"Error processing order response: {e}")
            raise
    
    async def get_supplier_forecasts(
        self,
        supplier_id: str,
        time_period: str = "30d"
    ) -> List[Dict[str, Any]]:
        """Get forecasts shared with a supplier"""
        try:
            supplier_forecasts = [
                f for f in self.forecasts if f["supplier_id"] == supplier_id
            ]
            
            # Filter by time period if needed
            if time_period:
                cutoff_date = datetime.now() - timedelta(days=int(time_period[:-1]))
                supplier_forecasts = [
                    f for f in supplier_forecasts 
                    if f["shared_at"] >= cutoff_date
                ]
            
            return supplier_forecasts
            
        except Exception as e:
            logger.error(f"Error getting supplier forecasts: {e}")
            raise
    
    async def request_pre_commitment(
        self,
        supplier_id: str,
        product_ids: List[str],
        quantities: List[int],
        commitment_date: str
    ) -> Dict[str, Any]:
        """Request pre-commitment from supplier for future orders"""
        try:
            logger.info(f"Requesting pre-commitment from supplier {supplier_id}")
            
            # Generate commitment ID
            commitment_id = f"COMM_{len(self.commitments):06d}"
            
            # Create commitment record
            commitment = PreCommitment(
                commitment_id=commitment_id,
                supplier_id=supplier_id,
                product_ids=product_ids,
                quantities=quantities,
                commitment_date=datetime.strptime(commitment_date, "%Y-%m-%d").date(),
                status="pending",
                created_at=datetime.now()
            )
            
            self.commitments.append(commitment)
            
            return {
                "commitment_id": commitment_id,
                "status": "requested",
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error requesting pre-commitment: {e}")
            raise
    
    async def get_supplier_commitments(self, supplier_id: str) -> List[Dict[str, Any]]:
        """Get pre-commitments for a supplier"""
        try:
            supplier_commitments = [
                c for c in self.commitments if c.supplier_id == supplier_id
            ]
            
            return [
                {
                    "commitment_id": c.commitment_id,
                    "product_ids": c.product_ids,
                    "quantities": c.quantities,
                    "commitment_date": c.commitment_date.isoformat(),
                    "status": c.status,
                    "created_at": c.created_at.isoformat(),
                    "confirmed_at": c.confirmed_at.isoformat() if c.confirmed_at else None
                }
                for c in supplier_commitments
            ]
            
        except Exception as e:
            logger.error(f"Error getting supplier commitments: {e}")
            raise
    
    async def get_performance_metrics(
        self,
        supplier_id: Optional[str] = None,
        start_date: str = None,
        end_date: str = None
    ) -> Dict[str, Any]:
        """Get supplier performance metrics"""
        try:
            # Mock performance metrics
            metrics = {
                "on_time_delivery_rate": np.random.uniform(0.85, 0.98),
                "quality_score": np.random.uniform(0.8, 0.95),
                "cost_efficiency": np.random.uniform(0.75, 0.92),
                "collaboration_score": np.random.uniform(0.7, 0.9),
                "total_orders": np.random.randint(50, 200),
                "average_response_time": np.random.uniform(2, 8),  # hours
                "last_updated": datetime.now()
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting performance metrics: {e}")
            raise
    
    async def get_collaboration_insights(self, supplier_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get collaboration insights and recommendations"""
        try:
            # Mock collaboration insights
            insights = []
            
            insight_types = [
                "delivery_optimization",
                "cost_reduction",
                "quality_improvement",
                "communication_enhancement"
            ]
            
            for i, insight_type in enumerate(insight_types):
                insights.append({
                    "insight_id": f"INS_{i:03d}",
                    "supplier_id": supplier_id or f"SUP_{np.random.randint(1, 4):03d}",
                    "insight_type": insight_type,
                    "description": f"Recommendation for {insight_type.replace('_', ' ')}",
                    "confidence_score": np.random.uniform(0.7, 0.95),
                    "recommended_action": f"Implement {insight_type} strategy",
                    "generated_at": datetime.now().isoformat()
                })
            
            return insights
            
        except Exception as e:
            logger.error(f"Error getting collaboration insights: {e}")
            raise
    
    async def create_blockchain_trace(
        self,
        order_id: str,
        supplier_id: str,
        trace_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create blockchain trace for order transparency"""
        try:
            logger.info(f"Creating blockchain trace for order {order_id}")
            
            # Generate trace ID
            trace_id = f"TRACE_{len(self.blockchain_traces):06d}"
            
            # Mock blockchain hash
            block_hash = f"0x{np.random.bytes(16).hex()}"
            
            # Create trace record
            trace = BlockchainTrace(
                trace_id=trace_id,
                order_id=order_id,
                supplier_id=supplier_id,
                block_hash=block_hash,
                transaction_data=trace_data,
                created_at=datetime.now(),
                verified=True
            )
            
            self.blockchain_traces.append(trace)
            
            return {
                "trace_id": trace_id,
                "hash": block_hash,
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating blockchain trace: {e}")
            raise
    
    async def get_order_traces(self, order_id: str) -> List[Dict[str, Any]]:
        """Get blockchain traces for an order"""
        try:
            order_traces = [
                t for t in self.blockchain_traces if t.order_id == order_id
            ]
            
            return [
                {
                    "trace_id": t.trace_id,
                    "supplier_id": t.supplier_id,
                    "block_hash": t.block_hash,
                    "transaction_data": t.transaction_data,
                    "created_at": t.created_at.isoformat(),
                    "verified": t.verified
                }
                for t in order_traces
            ]
            
        except Exception as e:
            logger.error(f"Error getting order traces: {e}")
            raise 