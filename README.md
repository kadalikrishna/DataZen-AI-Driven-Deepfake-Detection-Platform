# DataZen - AI-Driven Deepfake Detection Platform

**IBM Z Datathon 2025**
video link : https://youtu.be/gVlY_-fKycs  

A full-stack web application for AI-driven deepfake detection and societal impact prediction, simulating the IBM Z/z/OS AI Framework.

## 🚀 Features


### Backend (Flask RESTful API)
- **POST /api/v1/scan** - Scan media for deepfakes with CNN detection and sentiment analysis
- **POST /api/v1/upload** - Upload files for deepfake analysis
- **POST /api/v1/batch/upload** - CSV batch processing for multiple URLs
- **GET /api/v1/batch/export** - Export all incidents to CSV
- **GET /api/v1/incidents** - Retrieve all logged incidents (with filtering support)
- **GET /api/v1/incidents/<id>** - Get detailed incident information
- **POST /api/v1/incidents/<id>/verify** - Expert verification and blockchain logging
- **POST /api/v1/notify** - Proactive notification of stakeholders
- **GET /api/v1/blockchain/audit** - Retrieve immutable blockchain audit trail
- **GET /api/v1/stats** - Platform statistics and KPIs
- **POST /api/v1/demo/populate** - Generate demo data for testing
- **POST /api/v1/demo/clear** - Clear all demo data

### Frontend (SPA)
- **Scan Media View** - File upload, URL scanning, CSV batch processing, and data export
- **Dashboard View** - Real-time KPIs, risk level monitoring, and top incidents
- **Simplified Interface** - Clean, focused user experience without complex review workflows

### Key Technologies
- **Backend:** Python/Flask with in-memory database simulation
- **Frontend:** Vanilla JavaScript (SPA), HTML5, CSS3
- **Blockchain Simulation:** Mock Ethereum transaction hashing
- **Styling:** Modern IBM Carbon-inspired design system

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🛠️ Installation

### 1. Clone or Navigate to the Project Directory

```bash
cd /home/p/dp/IBMZ
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment (if not already created)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

### Start the Flask Server

```bash
cd backend
python app.py
```

The application will start on `http://localhost:5000`

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### 1. Scan Media Tab
- **File Upload**: Drag & drop or browse for media files (images, videos, audio)
- **URL Scanning**: Enter media URLs with auto-channel detection
- **CSV Batch Processing**: Upload CSV files for bulk analysis (10-1000+ items)
- **Export Results**: Download complete datasets for analysis
- **View Results**: See deepfake scores, sentiment analysis, and risk levels

### 2. Dashboard Tab
- **Real-Time KPIs**: Total detections, risk levels, blockchain entries
- **Statistics**: High/Medium/Low risk breakdown
- **Top Incidents**: Table of highest-risk detections
- **Live Updates**: Automatic data refresh

### 3. Batch Testing with CSV
- **Sample Dataset**: Download included test_dataset.csv
- **Custom Datasets**: Create your own CSV with media URLs
- **Bulk Analysis**: Process multiple URLs simultaneously
- **Result Summary**: View processing statistics and individual results

## 🏗️ Project Structure

```
IBMZ/
├── backend/
│   └── app.py              # Flask API server with all endpoints
├── static/
│   ├── css/
│   │   └── main.css        # Modern styling (IBM Carbon-inspired)
│   └── js/
│       └── app.js          # Frontend SPA logic
├── templates/
│   └── index.html          # Single-page application HTML
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔌 API Endpoints

### Scan Media
```bash
POST /api/v1/scan
Content-Type: application/json

{
  "media_url": "https://example.com/video.mp4",
  "channel_id": "Channel_A"
}
```

**Response:**
```json
{
  "detection_id": "uuid",
  "deepfake_score": 0.85,
  "sentiment_score": -0.6,
  "risk_quantification": "High",
  "timestamp": "2025-10-11T...",
  "status": "Awaiting Expert Review"
}
```

### Get All Incidents
```bash
GET /api/v1/incidents
# Optional query params: ?status=Awaiting Expert Review&risk=High
```

### Verify Incident
```bash
POST /api/v1/incidents/{detection_id}/verify
```

### Send Notifications
```bash
POST /api/v1/notify
Content-Type: application/json

{
  "incident_id": "uuid"
}
```

### Get Statistics
```bash
GET /api/v1/stats
```

### Blockchain Audit Trail
```bash
GET /api/v1/blockchain/audit
```

## 🎨 Design Features

- **Modern IBM Carbon-Inspired UI** - Professional, clean interface
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Real-time Updates** - Dynamic data loading without page refresh
- **Color-Coded Risk Levels** - Visual indicators for threat levels
- **Modal Detail Views** - In-depth forensic analysis
- **Toast Notifications** - User feedback for actions
- **Search & Filter** - Easy data navigation

## 🔒 Security Note

This is a **mock-up demonstration application** for the IBM Z Datathon 2025. In a production environment:
- Implement proper authentication and authorization
- Use secure database systems (IBM Db2, PostgreSQL)
- Implement real blockchain integration (Hyperledger, Ethereum)
- Add rate limiting and input validation
- Use HTTPS and secure API keys
- Implement proper error handling and logging

## 📊 Mock Data & Simulation

The application includes:
- **In-memory database** - Simulates data persistence
- **Mock blockchain** - Generates fake Ethereum transaction hashes
- **Random AI scores** - Simulates CNN and NLP model outputs
- **Demo data generator** - Quickly populate system for testing

## 🤝 IBM Z Integration Notes

This application simulates functionality that would run on:
- **IBM z/OS AI Framework** - For deep learning inference
- **IBM Db2 for z/OS** - For enterprise-grade data storage
- **IBM Blockchain Platform** - For immutable audit trails
- **IBM Z Security** - For cryptographic operations and access control

## 📝 License

This project is created for the IBM Z Datathon 2025.

## 👥 Support

For questions or issues:
1. Check the console output for error messages
2. Ensure Flask server is running on port 5000
3. Verify all dependencies are installed
4. Check browser console for JavaScript errors

## 🎯 Future Enhancements

- Real AI model integration (CNN for deepfake detection)
- Actual blockchain implementation
- User authentication system
- Database persistence (PostgreSQL/Db2)
- Real-time WebSocket updates
- Advanced analytics and reporting
- Export functionality for reports
- Multi-language support

---

**Built for IBM Z Datathon 2025** | Simulating IBM Z/z/OS AI Framework Capabilities
