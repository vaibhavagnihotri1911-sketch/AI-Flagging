#!/bin/bash

set -e

clear
echo "╔══════════════════════════════════════════════════════════════════════════╗"
echo "║    🛡️ 🇮🇳 CyberShield Indian Fraud Detection System                      ║"
echo "║    Network-Safe Deployment                                               ║"
echo "╚══════════════════════════════════════════════════════════════════════════╝"

echo "🚀 Starting CyberShield deployment..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

echo "✅ Docker found"

# Stop existing
echo "🛑 Stopping existing containers..."
docker-compose down &> /dev/null || true

# Build and start
echo "🔧 Building system (2-3 minutes)..."
docker-compose up -d --build

echo "⏳ Waiting for services (60 seconds)..."
sleep 60

echo "🧪 Testing connectivity..."

# Test API
API_READY=false
for i in {1..6}; do
    echo "Testing API attempt $i..."
    if curl -s http://localhost:5000/ > /dev/null 2>&1; then
        API_READY=true
        break
    fi
    sleep 10
done

# Test Dashboard  
DASHBOARD_READY=false
for i in {1..6}; do
    echo "Testing Dashboard attempt $i..."
    if curl -s http://localhost:8501/ > /dev/null 2>&1; then
        DASHBOARD_READY=true
        break
    fi
    sleep 10
done

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "🎯 CyberShield System Status"
echo "════════════════════════════════════════════════════════════════════════════"

if [ "$API_READY" = true ]; then
    echo "✅ API Ready: http://localhost:5000"
else
    echo "⚠️ API may still be starting..."
fi

if [ "$DASHBOARD_READY" = true ]; then
    echo "✅ Dashboard Ready: http://localhost:8501"
else
    echo "⚠️ Dashboard may still be starting..."
fi

echo ""
echo "🌐 Access Your System:"
echo "  📊 Dashboard: http://localhost:8501"
echo "  🔗 API: http://localhost:5000"
echo ""
echo "🧪 Quick Test:"
echo "  curl http://localhost:5000/api/v1/model_info"
echo ""
echo "🛠️ Management Commands:"
echo "  📊 Logs: docker-compose logs cybershield-india"
echo "  🔄 Restart: docker-compose restart"
echo "  🛑 Stop: docker-compose down"
echo ""

if [ "$API_READY" = true ] && [ "$DASHBOARD_READY" = true ]; then
    echo "✅ System fully operational!"
    echo "🇮🇳 भारतीय धोखाधड़ी तंत्र तैयार है!"
    echo "🏆 Ready for CyberShield Hackathon 2025!"
else
    echo "⏳ If services aren't ready, wait 2-3 more minutes"
    echo "📊 Check logs: docker-compose logs cybershield-india"
fi

echo ""
