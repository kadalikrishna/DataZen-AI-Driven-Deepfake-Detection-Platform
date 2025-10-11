#!/usr/bin/env python3
"""
DataZen - AI-Driven Deepfake Detection Platform
Flask Backend Application

IBM Z Datathon 2025
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import random
import hashlib
import csv
import io
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'wav', 'mp3'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory storage (simulating database)
incidents = []
blockchain_ledger = []
block_number = 1

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    """Determine file type from extension"""
    ext = filename.rsplit('.', 1)[1].lower()
    if ext in ['jpg', 'jpeg', 'png', 'gif']:
        return 'image'
    elif ext in ['mp4', 'avi', 'mov']:
        return 'video'
    elif ext in ['wav', 'mp3']:
        return 'audio'
    return 'unknown'

def generate_mock_ethereum_hash():
    """Generate a mock Ethereum transaction hash"""
    return hashlib.sha256(f"mock_tx_{random.random()}_{datetime.now().timestamp()}".encode()).hexdigest()

def calculate_risk_level(deepfake_score, sentiment_score):
    """Calculate risk level based on scores"""
    if deepfake_score > 0.8 or sentiment_score < -0.6:
        return "High"
    elif deepfake_score > 0.6 or sentiment_score < -0.3:
        return "Medium"
    else:
        return "Low"

@app.route('/')
def index():
    """Serve the main application"""
    return render_template('index.html')

@app.route('/api/v1/scan', methods=['POST'])
def scan_media():
    """Scan media URL for deepfake detection"""
    try:
        data = request.get_json()
        media_url = data.get('media_url')
        channel_id = data.get('channel_id', 'Unknown_Source')
        
        if not media_url:
            return jsonify({'error': 'media_url is required'}), 400
        
        # Auto-detect channel if not provided
        if channel_id == 'Unknown_Source':
            if 'youtube.com' in media_url or 'youtu.be' in media_url:
                channel_id = 'YouTube'
            elif 'twitter.com' in media_url or 'x.com' in media_url:
                channel_id = 'Twitter/X'
            elif 'facebook.com' in media_url:
                channel_id = 'Facebook'
            elif 'instagram.com' in media_url:
                channel_id = 'Instagram'
            elif 'tiktok.com' in media_url:
                channel_id = 'TikTok'
        
        # Mock AI analysis
        deepfake_score = round(random.uniform(0.1, 0.95), 3)
        sentiment_score = round(random.uniform(-1.0, 1.0), 3)
        risk_level = calculate_risk_level(deepfake_score, sentiment_score)
        
        # Create incident
        detection_id = f"det_{len(incidents) + 1}_{int(datetime.now().timestamp())}"
        incident = {
            'detection_id': detection_id,
            'media_url': media_url,
            'channel_id': channel_id,
            'deepfake_score': deepfake_score,
            'sentiment_score': sentiment_score,
            'risk_quantification': risk_level,
            'status': 'Awaiting Expert Review',
            'timestamp': datetime.now().isoformat(),
            'blockchain_hash': None
        }
        
        # Add to blockchain if high risk
        if risk_level == "High":
            blockchain_hash = generate_mock_ethereum_hash()
            incident['blockchain_hash'] = blockchain_hash
            
            # Add to blockchain ledger
            global block_number
            blockchain_entry = {
                'block_number': block_number,
                'transaction_hash': blockchain_hash,
                'action': 'Detection Created',
                'detection_id': detection_id,
                'timestamp': datetime.now().isoformat()
            }
            blockchain_ledger.append(blockchain_entry)
            block_number += 1
        
        incidents.append(incident)
        
        response_data = {
            'detection_id': detection_id,
            'deepfake_score': deepfake_score,
            'sentiment_score': sentiment_score,
            'risk_quantification': risk_level,
            'timestamp': incident['timestamp'],
            'blockchain_hash': incident['blockchain_hash']
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/incidents', methods=['GET'])
def get_incidents():
    """Get all incidents"""
    try:
        return jsonify(incidents), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/incidents/<incident_id>', methods=['GET'])
def get_incident_detail(incident_id):
    """Get detailed information about a specific incident"""
    try:
        incident = next((i for i in incidents if i['detection_id'] == incident_id), None)
        if not incident:
            return jsonify({'error': 'Incident not found'}), 404
        
        return jsonify(incident), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/incidents/<incident_id>/verify', methods=['POST'])
def verify_incident(incident_id):
    """Verify an incident as harmful or safe"""
    try:
        data = request.get_json()
        verification_status = data.get('status')
        
        if verification_status not in ['Verified Harmful', 'Verified Safe', 'False Positive']:
            return jsonify({'error': 'Invalid verification status'}), 400
        
        incident = next((i for i in incidents if i['detection_id'] == incident_id), None)
        if not incident:
            return jsonify({'error': 'Incident not found'}), 404
        
        incident['status'] = verification_status
        incident['verified_at'] = datetime.now().isoformat()
        
        # Add to blockchain
        global block_number
        blockchain_entry = {
            'block_number': block_number,
            'transaction_hash': generate_mock_ethereum_hash(),
            'action': 'Incident Verified',
            'detection_id': incident_id,
            'timestamp': datetime.now().isoformat()
        }
        blockchain_ledger.append(blockchain_entry)
        block_number += 1
        
        return jsonify({'message': f'Incident {incident_id} verified as {verification_status}'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/notify/<incident_id>', methods=['POST'])
def notify_stakeholders(incident_id):
    """Notify stakeholders about an incident"""
    try:
        incident = next((i for i in incidents if i['detection_id'] == incident_id), None)
        if not incident:
            return jsonify({'error': 'Incident not found'}), 404
        
        # Mock notification
        notification_data = {
            'incident_id': incident_id,
            'risk_level': incident['risk_quantification'],
            'notification_sent': True,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add to blockchain
        global block_number
        blockchain_entry = {
            'block_number': block_number,
            'transaction_hash': generate_mock_ethereum_hash(),
            'action': 'Stakeholder Notified',
            'detection_id': incident_id,
            'timestamp': datetime.now().isoformat()
        }
        blockchain_ledger.append(blockchain_entry)
        block_number += 1
        
        return jsonify(notification_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/blockchain/audit', methods=['GET'])
def get_blockchain_audit():
    """Get blockchain audit trail"""
    try:
        return jsonify(blockchain_ledger), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        total_detections = len(incidents)
        high_risk_count = len([i for i in incidents if i['risk_quantification'] == 'High'])
        verified_count = len([i for i in incidents if i['status'] != 'Awaiting Expert Review'])
        
        stats = {
            'total_detections': total_detections,
            'high_risk_incidents': high_risk_count,
            'verified_incidents': verified_count,
            'blockchain_entries': len(blockchain_ledger),
            'current_risk_level': 'Elevated' if high_risk_count > 0 else 'Normal'
        }
        
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/upload', methods=['POST'])
def upload_file():
    """Handle file upload for deepfake detection"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Mock AI analysis
        deepfake_score = round(random.uniform(0.1, 0.95), 3)
        sentiment_score = round(random.uniform(-1.0, 1.0), 3)
        risk_level = calculate_risk_level(deepfake_score, sentiment_score)
        
        # Create incident
        detection_id = f"upload_{len(incidents) + 1}_{int(datetime.now().timestamp())}"
        incident = {
            'detection_id': detection_id,
            'media_url': f"uploaded_file_{filename}",
            'channel_id': 'File Upload',
            'deepfake_score': deepfake_score,
            'sentiment_score': sentiment_score,
            'risk_quantification': risk_level,
            'status': 'Awaiting Expert Review',
            'timestamp': datetime.now().isoformat(),
            'blockchain_hash': None,
            'filename': filename,
            'file_type': get_file_type(filename),
            'file_size': os.path.getsize(filepath)
        }
        
        # Add to blockchain if high risk
        if risk_level == "High":
            blockchain_hash = generate_mock_ethereum_hash()
            incident['blockchain_hash'] = blockchain_hash
            
            global block_number
            blockchain_entry = {
                'block_number': block_number,
                'transaction_hash': blockchain_hash,
                'action': 'Detection Created',
                'detection_id': detection_id,
                'timestamp': datetime.now().isoformat()
            }
            blockchain_ledger.append(blockchain_entry)
            block_number += 1
        
        incidents.append(incident)
        
        response_data = {
            'detection_id': detection_id,
            'filename': filename,
            'file_type': incident['file_type'],
            'file_size': incident['file_size'],
            'deepfake_score': deepfake_score,
            'sentiment_score': sentiment_score,
            'risk_quantification': risk_level,
            'timestamp': incident['timestamp'],
            'blockchain_hash': incident['blockchain_hash']
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/batch/upload', methods=['POST'])
def batch_upload():
    """Handle CSV batch upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No CSV file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read CSV
        csv_content = file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        results = []
        success_count = 0
        error_count = 0
        
        for row in csv_reader:
            try:
                media_url = row.get('media_url', '').strip()
                if not media_url:
                    continue
                
                # Mock analysis
                deepfake_score = round(random.uniform(0.1, 0.95), 3)
                sentiment_score = round(random.uniform(-1.0, 1.0), 3)
                risk_level = calculate_risk_level(deepfake_score, sentiment_score)
                
                detection_id = f"batch_{len(incidents) + 1}_{int(datetime.now().timestamp())}"
                incident = {
                    'detection_id': detection_id,
                    'media_url': media_url,
                    'channel_id': row.get('channel_id', 'CSV Import'),
                    'deepfake_score': deepfake_score,
                    'sentiment_score': sentiment_score,
                    'risk_quantification': risk_level,
                    'status': 'Awaiting Expert Review',
                    'timestamp': datetime.now().isoformat(),
                    'blockchain_hash': None
                }
                
                incidents.append(incident)
                
                results.append({
                    'media_url': media_url,
                    'detection_id': detection_id,
                    'risk_level': risk_level,
                    'status': 'success'
                })
                success_count += 1
                
            except Exception as e:
                results.append({
                    'media_url': media_url,
                    'error': str(e),
                    'status': 'error'
                })
                error_count += 1
        
        return jsonify({
            'summary': {
                'total_processed': len(results),
                'successful': success_count,
                'errors': error_count
            },
            'results': results
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/batch/export', methods=['GET'])
def export_incidents():
    """Export all incidents to CSV"""
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Detection ID', 'Media URL', 'Channel ID', 'Deepfake Score', 'Sentiment Score', 'Risk Level', 'Status', 'Created At', 'Blockchain Hash'])
        
        # Write data
        for incident in incidents:
            writer.writerow([
                incident['detection_id'],
                incident['media_url'],
                incident['channel_id'],
                incident['deepfake_score'],
                incident['sentiment_score'],
                incident['risk_quantification'],
                incident['status'],
                incident['timestamp'],
                incident.get('blockchain_hash', '')
            ])
        
        output.seek(0)
        return output.getvalue(), 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename=incidents_export.csv'
        }
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/demo/clear', methods=['POST'])
def clear_demo_data():
    """Clear all demo data"""
    try:
        global incidents, blockchain_ledger, block_number
        incidents.clear()
        blockchain_ledger.clear()
        block_number = 1
        
        return jsonify({'message': 'All demo data cleared successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test_dataset.csv')
def serve_test_dataset():
    """Serve the test dataset CSV file"""
    return send_from_directory('.', 'test_dataset.csv')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render uses PORT env variable
    app.run(debug=False, host='0.0.0.0', port=port)  # 0.0.0.0 for external access
