# Quick Start Guide

## 🚀 Launch the Application (Easy Way)

```bash
cd /home/p/dp/IBMZ
./start.sh
```

The script will:
1. Activate the virtual environment
2. Install dependencies
3. Start the Flask server

## 🚀 Manual Launch

```bash
# Navigate to project
cd /home/p/dp/IBMZ

# Activate virtual environment
source ../venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start server
cd backend
python app.py
```

## 🌐 Access the Application

Open your browser and go to:
```
http://localhost:5000
```

## 📝 First Steps

1. **Generate Demo Data**
   - Click "Scan Media" tab
   - Scroll down to "Demo Data" section
   - Click "Generate Demo Data"
   - This creates 8 sample deepfake incidents

2. **View Dashboard**
   - Click "Dashboard" tab
   - See statistics and KPIs
   - View top 5 high-risk incidents

3. **Review Incidents**
   - Click "Expert Review" tab
   - Click on any incident card
   - Review forensic analysis
   - Click "Verify Harmful / Log to Blockchain"

4. **Check Audit Trail**
   - Click "Audit Trail" tab
   - View blockchain ledger
   - Search entries
   - See immutable records

## 🔧 Scan Your Own Media

1. Click "Scan Media" tab
2. Enter a media URL (e.g., `https://example.com/video.mp4`)
3. Enter a channel ID (e.g., `Channel_A`)
4. Click "Scan Media"
5. View the results

## 🛑 Stop the Server

Press `CTRL+C` in the terminal

## 📋 API Endpoints (for testing with curl/Postman)

### Scan Media
```bash
curl -X POST http://localhost:5000/api/v1/scan \
  -H "Content-Type: application/json" \
  -d '{"media_url":"https://example.com/video.mp4","channel_id":"Channel_A"}'
```

### Get All Incidents
```bash
curl http://localhost:5000/api/v1/incidents
```

### Get Statistics
```bash
curl http://localhost:5000/api/v1/stats
```

### Generate Demo Data
```bash
curl -X POST http://localhost:5000/api/v1/demo/populate
```

## ❓ Troubleshooting

**Port 5000 already in use?**
```bash
# Find and kill the process
lsof -ti:5000 | xargs kill -9
```

**Module not found error?**
```bash
# Ensure virtual environment is activated
source ../venv/bin/activate
pip install -r requirements.txt
```

**Browser shows "Connection Refused"?**
- Check that Flask server is running
- Check console output for errors
- Try accessing http://127.0.0.1:5000 instead

## 🎯 Key Features to Demonstrate

- ✅ Real-time deepfake detection simulation
- ✅ Risk-based incident classification
- ✅ Expert review and verification workflow
- ✅ Blockchain audit trail (mock Ethereum)
- ✅ Stakeholder notification system
- ✅ RESTful API architecture
- ✅ Modern, responsive UI
- ✅ In-memory database simulation

---

**Built for IBM Z Datathon 2025**

