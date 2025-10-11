# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Browser (Client)                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │Dashboard │ │  Expert  │ │  Audit   │ │   Scan   │  │
│  │   View   │ │  Review  │ │  Trail   │ │   Media  │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│                     ↕ (HTTP/JSON)                        │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│              Flask RESTful API (Backend)                │
│  ┌──────────────────────────────────────────────────┐  │
│  │            API Endpoint Router                   │  │
│  │  /scan  /incidents  /verify  /notify  /audit    │  │
│  └──────────────────────────────────────────────────┘  │
│                            ↓                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Business Logic Layer                     │  │
│  │  - Deepfake Detection Simulation                │  │
│  │  - Sentiment Analysis Simulation                │  │
│  │  - Risk Quantification                          │  │
│  │  - Expert Verification Workflow                 │  │
│  └──────────────────────────────────────────────────┘  │
│                            ↓                             │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Data Persistence Layer                 │  │
│  │  - In-Memory Incidents Database                 │  │
│  │  - Blockchain Ledger Simulation                 │  │
│  │  - Notifications Log                            │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Component Breakdown

### Frontend (SPA)

**Technology:** HTML5, CSS3, Vanilla JavaScript

**Files:**
- `templates/index.html` - Single-page application structure
- `static/css/main.css` - Modern IBM Carbon-inspired styling
- `static/js/app.js` - Frontend logic and API integration

**Key Features:**
- View management (Dashboard, Review, Audit, Scan)
- Real-time data updates
- Modal dialogs for detailed views
- Toast notifications
- Search and filter functionality

### Backend (Flask API)

**Technology:** Python, Flask, Flask-CORS

**Files:**
- `backend/app.py` - Complete API server

**Key Features:**
- RESTful API design
- In-memory data storage
- Blockchain simulation
- CORS-enabled for development

## Data Flow

### 1. Media Scan Flow
```
User Input → /api/v1/scan → AI Simulation → Risk Assessment → 
Database Storage → Blockchain Logging (if high-risk) → Response
```

### 2. Expert Review Flow
```
Load Queue → /api/v1/incidents → Display Incidents → 
Expert Review → /api/v1/verify → Update Status → 
Blockchain Logging → Refresh Views
```

### 3. Notification Flow
```
Incident Detected → /api/v1/notify → Generate Notification → 
Log to Blockchain → Send to Stakeholders → Store in Log
```

### 4. Audit Trail Flow
```
Any Action → Blockchain Entry → /api/v1/blockchain/audit → 
Display Immutable Records → Search/Filter
```

## API Endpoints

| Endpoint | Method | Purpose | Request | Response |
|----------|--------|---------|---------|----------|
| `/api/v1/scan` | POST | Scan media | `{media_url, channel_id}` | Detection results |
| `/api/v1/incidents` | GET | List incidents | Query params | Incidents array |
| `/api/v1/incidents/<id>` | GET | Get incident | - | Incident details |
| `/api/v1/incidents/<id>/verify` | POST | Verify incident | - | Updated incident |
| `/api/v1/notify` | POST | Send notifications | `{incident_id}` | Notification details |
| `/api/v1/blockchain/audit` | GET | Get audit trail | - | Blockchain entries |
| `/api/v1/stats` | GET | Get statistics | - | KPIs and metrics |
| `/api/v1/demo/populate` | POST | Generate demo data | - | Created incidents |

## Data Models

### Incident
```javascript
{
  detection_id: string (UUID),
  media_url: string,
  channel_id: string,
  deepfake_score: float (0.0-1.0),
  sentiment_score: float (-1.0 to 1.0),
  risk_quantification: enum (High, Medium, Low),
  timestamp: ISO datetime,
  status: string,
  verified: boolean,
  blockchain_hash: string (nullable)
}
```

### Blockchain Entry
```javascript
{
  transaction_hash: string (0x...),
  timestamp: ISO datetime,
  block_number: integer,
  data: {
    detection_id: string,
    action: string,
    ...additional fields
  },
  immutable: boolean (always true)
}
```

### Notification
```javascript
{
  notification_id: string (UUID),
  incident_id: string,
  recipients: array,
  notification_type: string,
  sent_at: ISO datetime,
  status: string
}
```

## Simulation Components

### 1. Deepfake Detection (Mock CNN)
- Generates random score between 0.1 and 0.95
- Simulates convolutional neural network analysis
- In production: Would use actual CNN model

### 2. Sentiment Analysis (Mock NLP)
- Generates random score between -0.9 and 0.5
- Simulates natural language processing
- In production: Would use transformer models (BERT, etc.)

### 3. Blockchain (Mock Ethereum)
- Generates SHA-256 hash with "0x" prefix
- Assigns mock block numbers
- Stores in in-memory ledger
- In production: Would use Hyperledger or Ethereum

### 4. Risk Quantification
```python
if deepfake_score > 0.7 and sentiment_score < -0.3:
    return "High"
elif deepfake_score > 0.5 or sentiment_score < -0.5:
    return "Medium"
else:
    return "Low"
```

## Security Considerations

### Current Implementation (Demo)
- No authentication
- No authorization
- In-memory data (lost on restart)
- No input validation
- HTTP only (no HTTPS)

### Production Requirements
- JWT-based authentication
- Role-based access control (RBAC)
- Database persistence (IBM Db2, PostgreSQL)
- Input validation and sanitization
- Rate limiting
- HTTPS/TLS encryption
- API key management
- Audit logging
- GDPR compliance

## IBM Z Integration Points

### z/OS AI Framework
- CNN model inference on IBM Z processors
- Parallel processing for batch analysis
- z/OS Unix System Services integration

### IBM Db2 for z/OS
- Replace in-memory storage
- Enterprise-grade transactions
- High availability and disaster recovery

### IBM Blockchain Platform
- Replace mock blockchain
- Hyperledger Fabric on IBM Z
- Smart contracts for verification workflows

### IBM Z Security
- Pervasive encryption
- Crypto Express cards for hashing
- RACF integration for access control

## Performance Considerations

### Current Limitations
- In-memory storage (limited by RAM)
- Single-threaded Flask (development server)
- No caching layer
- No load balancing

### Production Optimizations
- Database indexing
- Redis caching layer
- Gunicorn/uWSGI multi-worker setup
- CDN for static assets
- API response pagination
- WebSocket for real-time updates

## Scalability Path

```
Development (Current)
  ↓
Single Server Deployment
  ↓
Load Balanced Multi-Instance
  ↓
Microservices Architecture
  ↓
IBM Z Enterprise Platform
```

---

**Built for IBM Z Datathon 2025** | Simulating Enterprise-Grade Architecture

