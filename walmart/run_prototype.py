#!/usr/bin/env python3
"""
FestAI Prototype Startup Script
This script starts all components of the FestAI prototype system.
"""

import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path

def print_banner():
    """Print the FestAI banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║  🎯 FestAI - Intelligent Seasonal Demand Management         ║
    ║                                                              ║
    ║  Powered by AI • Built for Sustainability •                 ║
    ║  Designed for Efficiency                                    ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        "fastapi", "uvicorn", "pandas", "numpy", "streamlit", 
        "plotly", "prophet", "xgboost", "scikit-learn"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages using:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting FestAI Backend...")
    
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Start the FastAPI server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Backend server started on http://localhost:8000")
        print("📚 API Documentation: http://localhost:8000/docs")
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def start_dashboard():
    """Start the Streamlit dashboard"""
    print("📊 Starting FestAI Dashboard...")
    
    try:
        # Change to dashboard directory
        os.chdir("dashboard")
        
        # Start the Streamlit dashboard
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.port", "8501", "--server.address", "0.0.0.0"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Dashboard started on http://localhost:8501")
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start dashboard: {e}")
        return None

def start_ml_pipeline():
    """Start the ML pipeline (mock)"""
    print("🤖 Starting ML Pipeline...")
    
    try:
        # Mock ML pipeline - in real implementation, this would start actual ML services
        print("✅ ML Pipeline started (mock)")
        return None
        
    except Exception as e:
        print(f"❌ Failed to start ML pipeline: {e}")
        return None

def monitor_processes(processes):
    """Monitor running processes"""
    try:
        while True:
            time.sleep(5)
            
            # Check if any process has stopped
            for name, process in processes.items():
                if process and process.poll() is not None:
                    print(f"⚠️ {name} has stopped unexpectedly")
                    
    except KeyboardInterrupt:
        print("\n🛑 Shutting down FestAI...")
        stop_all_processes(processes)

def stop_all_processes(processes):
    """Stop all running processes"""
    print("🛑 Stopping all processes...")
    
    for name, process in processes.items():
        if process:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"⚠️ {name} force killed")
            except Exception as e:
                print(f"❌ Error stopping {name}: {e}")

def main():
    """Main function to start the FestAI prototype"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🎯 Starting FestAI Prototype System")
    print("="*60)
    
    # Store original directory
    original_dir = os.getcwd()
    
    # Start all components
    processes = {}
    
    try:
        # Start backend
        backend_process = start_backend()
        if backend_process:
            processes["Backend"] = backend_process
        
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Start dashboard
        os.chdir(original_dir)  # Return to original directory
        dashboard_process = start_dashboard()
        if dashboard_process:
            processes["Dashboard"] = dashboard_process
        
        # Start ML pipeline
        os.chdir(original_dir)  # Return to original directory
        ml_process = start_ml_pipeline()
        if ml_process:
            processes["ML Pipeline"] = ml_process
        
        # Print access information
        print("\n" + "="*60)
        print("🎉 FestAI Prototype is now running!")
        print("="*60)
        print("📊 Dashboard: http://localhost:8501")
        print("🔧 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("🔍 Health Check: http://localhost:8000/health")
        print("\n💡 Press Ctrl+C to stop all services")
        print("="*60)
        
        # Monitor processes
        monitor_processes(processes)
        
    except KeyboardInterrupt:
        print("\n🛑 Received interrupt signal")
    except Exception as e:
        print(f"❌ Error starting FestAI: {e}")
    finally:
        # Clean up
        stop_all_processes(processes)
        os.chdir(original_dir)  # Return to original directory
        print("👋 FestAI Prototype stopped")

if __name__ == "__main__":
    main() 