#!/usr/bin/env python3
"""
FestAI Prototype Demo Script
This script demonstrates the key features of the FestAI system.
"""

import asyncio
import requests
import json
from datetime import datetime, timedelta
import time

# API base URL
API_BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Print a step description"""
    print(f"\n📋 Step {step}: {description}")

async def demo_forecasting():
    """Demo forecasting capabilities"""
    print_section("DEMO: Multi-Signal Demand Forecasting")
    
    print_step(1, "Generate demand forecast for seasonal products")
    
    # Mock forecast request
    forecast_request = {
        "product_ids": ["PROD_001", "PROD_002", "PROD_003"],
        "forecast_period": "month",
        "include_external_signals": True,
        "confidence_level": 0.95
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/forecast/generate", json=forecast_request)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Forecast generation started: {result['forecast_id']}")
            print(f"   Status: {result['status']}")
            print(f"   Estimated completion: {result['estimated_completion']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print_step(2, "Get forecast for specific product")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/forecast/PROD_001?days=30")
        if response.status_code == 200:
            forecast_data = response.json()
            print(f"✅ Forecast retrieved for PROD_001")
            print(f"   Forecast period: {forecast_data['forecast_period']} days")
            print(f"   Predictions: {len(forecast_data['predictions'])} data points")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print_step(3, "Get social media signals")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/forecast/signals/social?product_id=PROD_001")
        if response.status_code == 200:
            signals = response.json()
            print(f"✅ Social signals retrieved")
            print(f"   Sentiment score: {signals['sentiment_score']:.3f}")
            print(f"   Trending score: {signals['trending_score']:.3f}")
            print(f"   Mentions count: {signals['mentions_count']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

async def demo_inventory():
    """Demo inventory management"""
    print_section("DEMO: Dynamic Inventory Management")
    
    print_step(1, "Get current inventory status")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/inventory/status?critical_only=true")
        if response.status_code == 200:
            inventory_data = response.json()
            print(f"✅ Inventory status retrieved")
            print(f"   Critical items: {len(inventory_data)}")
            
            for item in inventory_data[:3]:  # Show first 3 items
                print(f"   - {item['product_id']}: {item['status']} (Qty: {item['current_quantity']})")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print_step(2, "Get dynamic thresholds")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/inventory/thresholds")
        if response.status_code == 200:
            thresholds = response.json()
            print(f"✅ Dynamic thresholds retrieved")
            print(f"   Thresholds calculated: {len(thresholds)}")
            
            for threshold in thresholds[:2]:  # Show first 2 thresholds
                print(f"   - {threshold['product_id']}: {threshold['calculated_value']} (Confidence: {threshold['confidence_score']:.2f})")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print_step(3, "Get perishable monitoring")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/inventory/perishable/monitoring")
        if response.status_code == 200:
            perishable_data = response.json()
            print(f"✅ Perishable monitoring data retrieved")
            print(f"   Total perishable items: {len(perishable_data['perishable_items'])}")
            print(f"   Expiring soon: {len(perishable_data['expiring_soon'])}")
            print(f"   Markdown candidates: {len(perishable_data['markdown_candidates'])}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

async def demo_customer_engagement():
    """Demo customer engagement features"""
    print_section("DEMO: Customer Engagement & Pre-Orders")
    
    print_step(1, "Create customer pre-order")
    
    preorder_request = {
        "customer_id": "CUST_001",
        "product_id": "PROD_001",
        "store_id": "STORE_001",
        "quantity": 2,
        "expected_availability": (datetime.now() + timedelta(days=7)).date().isoformat()
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/customers/preorder", json=preorder_request)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Pre-order created successfully")
            print(f"   Pre-order ID: {result['preorder_id']}")
            print(f"   Status: {result['status']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print_step(2, "Register coming soon interest")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/customers/coming-soon/register",
            params={
                "customer_id": "CUST_001",
                "product_id": "PROD_101",
                "store_id": "STORE_001"
            }
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Coming soon interest registered")
            print(f"   Customer: {result['customer_id']}")
            print(f"   Product: {result['product_id']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print_step(3, "Send customer notification")
    
    notification_request = {
        "customer_ids": ["CUST_001", "CUST_002", "CUST_003"],
        "message": "New seasonal products are now available for pre-order!",
        "notification_type": "coming_soon",
        "channel": "email"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/customers/notify", json=notification_request)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Notifications sent successfully")
            print(f"   Notification ID: {result['notification_id']}")
            print(f"   Recipients: {result['recipient_count']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

async def demo_supplier_management():
    """Demo supplier management features"""
    print_section("DEMO: Supplier Management & Collaboration")
    
    print_step(1, "Create supplier order")
    
    supplier_order = {
        "supplier_id": "SUP_001",
        "product_ids": ["PROD_001", "PROD_002"],
        "quantities": [50, 30],
        "store_id": "STORE_001",
        "expected_delivery_date": (datetime.now() + timedelta(days=14)).date().isoformat(),
        "priority": "medium",
        "auto_generated": True
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/suppliers/orders/create", json=supplier_order)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Supplier order created")
            print(f"   Order ID: {result['order_id']}")
            print(f"   Status: {result['status']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print_step(2, "Share forecast with supplier")
    
    forecast_share = {
        "supplier_id": "SUP_001",
        "product_ids": ["PROD_001", "PROD_002", "PROD_003"],
        "forecast_period": "30d",
        "forecast_data": {
            "demand_forecast": [100, 120, 150],
            "confidence_intervals": {"lower": [80, 100, 120], "upper": [120, 140, 180]}
        }
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/suppliers/forecast/share", json=forecast_share)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Forecast shared with supplier")
            print(f"   Forecast ID: {result['forecast_id']}")
            print(f"   Supplier: {result['supplier_id']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print_step(3, "Get supplier performance metrics")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/suppliers/performance/metrics?supplier_id=SUP_001")
        if response.status_code == 200:
            metrics = response.json()
            print(f"✅ Supplier performance metrics retrieved")
            print(f"   On-time delivery: {metrics['metrics']['on_time_delivery_rate']:.1%}")
            print(f"   Quality score: {metrics['metrics']['quality_score']:.1%}")
            print(f"   Cost efficiency: {metrics['metrics']['cost_efficiency']:.1%}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

async def demo_sustainability():
    """Demo sustainability features"""
    print_section("DEMO: Sustainability & Waste Reduction")
    
    print_step(1, "Get waste reduction analytics")
    
    start_date = (datetime.now() - timedelta(days=30)).date().isoformat()
    end_date = datetime.now().date().isoformat()
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/inventory/analytics/waste-reduction",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "store_id": "STORE_001"
            }
        )
        if response.status_code == 200:
            analytics = response.json()
            print(f"✅ Waste reduction analytics retrieved")
            print(f"   Period: {analytics['period']}")
            print(f"   Waste reduced: {analytics['waste_reduced']:.1f}%")
            print(f"   Cost savings: ${analytics['cost_savings']:,.0f}")
            print(f"   Sustainability score: {analytics['sustainability_score']:.1%}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print_step(2, "Trigger automated markdown")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/inventory/perishable/markdown",
            params={
                "product_id": "PROD_001",
                "store_id": "STORE_001",
                "markdown_percentage": 0.3
            }
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Markdown triggered successfully")
            print(f"   Product: {result['product_id']}")
            print(f"   Markdown: {result['markdown_percentage']:.1%}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

async def demo_dashboard():
    """Demo dashboard overview"""
    print_section("DEMO: Dashboard Overview")
    
    print_step(1, "Get dashboard data")
    
    try:
        response = requests.get(f"{API_BASE_URL}/dashboard")
        if response.status_code == 200:
            dashboard_data = response.json()
            print(f"✅ Dashboard data retrieved")
            print(f"   System status: {dashboard_data['system_status']}")
            print(f"   Recent forecasts: {len(dashboard_data['forecasts'])}")
            print(f"   Critical alerts: {len(dashboard_data['inventory_alerts'])}")
            print(f"   Pending notifications: {dashboard_data['pending_notifications']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print_step(2, "Health check")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ System health check")
            print(f"   Status: {health_data['status']}")
            print(f"   Service: {health_data['service']}")
            print(f"   Version: {health_data['version']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

async def main():
    """Main demo function"""
    print("🎯 FestAI Prototype Demo")
    print("This demo showcases the key features of the FestAI system.")
    print("\n⚠️  Make sure the FestAI backend is running on http://localhost:8000")
    print("   You can start it using: python run_prototype.py")
    
    # Wait for user confirmation
    input("\nPress Enter to start the demo...")
    
    try:
        # Run all demos
        await demo_dashboard()
        await demo_forecasting()
        await demo_inventory()
        await demo_customer_engagement()
        await demo_supplier_management()
        await demo_sustainability()
        
        print_section("DEMO COMPLETED")
        print("🎉 All FestAI features have been demonstrated!")
        print("\n📊 To explore the full interface, visit:")
        print("   Dashboard: http://localhost:8501")
        print("   API Docs: http://localhost:8000/docs")
        
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 