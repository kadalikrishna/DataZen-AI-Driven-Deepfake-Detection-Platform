"""
Vercel entry point for Flask application
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import hashlib
import csv
import io
from datetime import datetime

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['JSON_SORT_KEYS'] = False

# In-memory storage (simulating database)
incidents = []
blockchain_ledger = []
block_number = 1

# Helper functions
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
    """Serve the complete DataZen dashboard with all features"""
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DataZen - AI Deepfake Detection Platform | Created by Kadali Krishna</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Inter', sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                min-height: 100vh;
                color: #333;
                overflow-x: hidden;
            }
            .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
            .header { 
                text-align: center; 
                margin-bottom: 40px; 
                color: white; 
                animation: slideDown 1s ease-out;
            }
            .header h1 { 
                font-size: 3.5rem; 
                margin-bottom: 15px; 
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                background: linear-gradient(45deg, #fff, #f0f8ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: glow 2s ease-in-out infinite alternate;
            }
            .header p { 
                font-size: 1.3rem; 
                opacity: 0.95; 
                font-weight: 300;
                letter-spacing: 0.5px;
            }
            .creator-info {
                margin-top: 20px;
                padding: 15px 25px;
                background: rgba(255,255,255,0.1);
                border-radius: 15px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
                display: inline-block;
                animation: slideUp 1s ease-out 0.6s both;
            }
            .creator-info p {
                font-size: 1.1rem;
                margin: 0;
                color: white;
                font-weight: 500;
            }
            .creator-info strong {
                color: #f0f8ff;
                font-weight: 700;
                text-shadow: 0 0 10px rgba(255,255,255,0.5);
            }
            .creator-info i {
                margin-right: 8px;
                color: #f0f8ff;
            }
            
            @keyframes slideDown {
                from { opacity: 0; transform: translateY(-50px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            @keyframes glow {
                from { text-shadow: 0 0 20px rgba(255,255,255,0.5); }
                to { text-shadow: 0 0 30px rgba(255,255,255,0.8), 0 0 40px rgba(102,126,234,0.3); }
            }
            
            /* Navigation Tabs */
            .nav-tabs { 
                display: flex; 
                background: rgba(255,255,255,0.15); 
                border-radius: 20px; 
                padding: 8px; 
                margin-bottom: 40px; 
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255,255,255,0.2);
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                animation: slideUp 1s ease-out 0.3s both;
            }
            .nav-tab { 
                flex: 1; 
                padding: 18px 25px; 
                text-align: center; 
                color: white; 
                cursor: pointer; 
                border-radius: 15px; 
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); 
                font-weight: 600;
                position: relative;
                overflow: hidden;
            }
            .nav-tab::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }
            .nav-tab:hover::before {
                left: 100%;
            }
            .nav-tab.active { 
                background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(255,255,255,0.8)); 
                color: #667eea; 
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                transform: translateY(-2px);
            }
            .nav-tab:hover:not(.active) { 
                background: rgba(255,255,255,0.25); 
                transform: translateY(-1px);
            }
            
            @keyframes slideUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            /* Content Sections */
            .content-section { 
                display: none; 
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            .content-section.active { 
                display: block; 
                opacity: 1;
            }
            
            @keyframes slideInRight {
                from { opacity: 0; transform: translateX(50px); }
                to { opacity: 1; transform: translateX(0); }
            }
            
            .dashboard { 
                background: rgba(255,255,255,0.95); 
                border-radius: 25px; 
                padding: 50px; 
                box-shadow: 0 25px 50px rgba(0,0,0,0.1);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255,255,255,0.2);
                animation: fadeInUp 0.8s ease-out 0.2s both;
            }
            
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            /* Statistics Grid */
            .stats-grid { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
                gap: 25px; 
                margin-bottom: 50px; 
            }
            .stat-card { 
                background: linear-gradient(135deg, #667eea, #764ba2, #f093fb); 
                color: white; 
                padding: 35px; 
                border-radius: 20px; 
                text-align: center; 
                box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
                border: 1px solid rgba(255,255,255,0.1);
            }
            .stat-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
                transform: translateX(-100%);
                transition: transform 0.6s;
            }
            .stat-card:hover::before {
                transform: translateX(100%);
            }
            .stat-card:hover { 
                transform: translateY(-8px) scale(1.02); 
                box-shadow: 0 25px 50px rgba(0,0,0,0.2);
            }
            .stat-card h3 { 
                font-size: 3rem; 
                margin-bottom: 15px; 
                font-weight: 700;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                animation: countUp 1s ease-out;
            }
            .stat-card p { 
                font-size: 1.2rem; 
                opacity: 0.95; 
                font-weight: 500;
                letter-spacing: 0.5px;
            }
            
            @keyframes countUp {
                from { opacity: 0; transform: scale(0.5); }
                to { opacity: 1; transform: scale(1); }
            }
            
            /* File Upload Section */
            .upload-section { 
                background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(248,249,250,0.8)); 
                padding: 40px; 
                border-radius: 20px; 
                margin-bottom: 40px; 
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.3);
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            .upload-section h2 { 
                margin-bottom: 25px; 
                color: #333; 
                font-size: 1.8rem;
                font-weight: 600;
                text-align: center;
            }
            
            .upload-area { 
                border: 3px dashed #667eea; 
                border-radius: 20px; 
                padding: 50px; 
                text-align: center; 
                background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(248,249,250,0.6)); 
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); 
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }
            .upload-area::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, transparent, rgba(102,126,234,0.1), transparent);
                transform: translateX(-100%);
                transition: transform 0.6s;
            }
            .upload-area:hover::before {
                transform: translateX(100%);
            }
            .upload-area:hover { 
                border-color: #764ba2; 
                background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1)); 
                transform: translateY(-2px);
                box-shadow: 0 15px 35px rgba(102,126,234,0.2);
            }
            .upload-area.dragover { 
                border-color: #28a745; 
                background: linear-gradient(135deg, rgba(40,167,69,0.1), rgba(32,201,151,0.1)); 
                transform: scale(1.02);
            }
            .upload-icon { 
                font-size: 4rem; 
                color: #667eea; 
                margin-bottom: 20px; 
                animation: bounce 2s infinite;
            }
            .upload-text { 
                font-size: 1.4rem; 
                color: #555; 
                margin-bottom: 15px; 
                font-weight: 500;
            }
            .upload-subtext { 
                color: #777; 
                font-size: 1rem; 
                font-weight: 400;
            }
            
            @keyframes bounce {
                0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                40% { transform: translateY(-10px); }
                60% { transform: translateY(-5px); }
            }
            
            .file-preview { 
                margin-top: 20px; 
                padding: 15px; 
                background: #e8f5e8; 
                border-radius: 10px; 
                display: none; 
                transition: all 0.3s ease;
            }
            .file-info { display: flex; align-items: center; gap: 15px; }
            .file-icon { font-size: 2rem; color: #28a745; }
            .file-details h4 { margin-bottom: 5px; color: #333; }
            .file-details p { color: #666; font-size: 0.9rem; }
            
            /* Form Styles */
            .form-group { 
                margin-bottom: 25px; 
                animation: slideInLeft 0.6s ease-out;
            }
            .form-group label { 
                display: block; 
                margin-bottom: 10px; 
                font-weight: 600; 
                color: #555; 
                font-size: 1.1rem;
            }
            .form-group input, .form-group select { 
                width: 100%; 
                padding: 15px 20px; 
                border: 2px solid #e1e5e9; 
                border-radius: 15px; 
                font-size: 16px; 
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); 
                background: rgba(255,255,255,0.9);
                backdrop-filter: blur(10px);
            }
            .form-group input:focus, .form-group select:focus { 
                outline: none; 
                border-color: #667eea; 
                box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
                transform: translateY(-2px);
            }
            .form-group input:hover, .form-group select:hover {
                border-color: #764ba2;
                transform: translateY(-1px);
            }
            
            @keyframes slideInLeft {
                from { opacity: 0; transform: translateX(-30px); }
                to { opacity: 1; transform: translateX(0); }
            }
            
            /* Buttons */
            .btn { 
                background: linear-gradient(135deg, #667eea, #764ba2); 
                color: white; 
                padding: 15px 35px; 
                border: none; 
                border-radius: 15px; 
                font-size: 16px; 
                font-weight: 600; 
                cursor: pointer; 
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); 
                margin: 8px;
                position: relative;
                overflow: hidden;
                box-shadow: 0 8px 25px rgba(102,126,234,0.3);
            }
            .btn::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }
            .btn:hover::before {
                left: 100%;
            }
            .btn:hover { 
                transform: translateY(-3px) scale(1.05); 
                box-shadow: 0 15px 35px rgba(102,126,234,0.4);
            }
            .btn:active {
                transform: translateY(-1px) scale(1.02);
            }
            .btn:disabled { 
                opacity: 0.6; 
                cursor: not-allowed; 
                transform: none; 
                box-shadow: 0 4px 15px rgba(102,126,234,0.2);
            }
            .btn-success { 
                background: linear-gradient(135deg, #28a745, #20c997); 
                box-shadow: 0 8px 25px rgba(40,167,69,0.3);
            }
            .btn-success:hover {
                box-shadow: 0 15px 35px rgba(40,167,69,0.4);
            }
            .btn-danger { 
                background: linear-gradient(135deg, #dc3545, #e74c3c); 
                box-shadow: 0 8px 25px rgba(220,53,69,0.3);
            }
            .btn-danger:hover {
                box-shadow: 0 15px 35px rgba(220,53,69,0.4);
            }
            .btn-warning { 
                background: linear-gradient(135deg, #ffc107, #fd7e14); 
                box-shadow: 0 8px 25px rgba(255,193,7,0.3);
            }
            .btn-warning:hover {
                box-shadow: 0 15px 35px rgba(255,193,7,0.4);
            }
            
            /* Results */
            .result { 
                margin-top: 20px; 
                padding: 20px; 
                background: #e8f5e8; 
                border-radius: 10px; 
                border-left: 4px solid #28a745; 
                display: none; 
                transition: all 0.3s ease;
            }
            .result.error { background: #f8d7da; border-left-color: #dc3545; }
            .result.warning { background: #fff3cd; border-left-color: #ffc107; }
            
            
            @keyframes slideInUp {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            /* Tables */
            .table-container { 
                background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,249,250,0.8)); 
                border-radius: 20px; 
                overflow: hidden; 
                box-shadow: 0 15px 35px rgba(0,0,0,0.1); 
                margin-bottom: 40px; 
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.3);
                animation: slideInUp 0.8s ease-out 0.2s both;
            }
            .table-container.compact { 
                margin-bottom: 20px; 
            }
            .table { width: 100%; border-collapse: collapse; }
            .table th, .table td { 
                padding: 18px; 
                text-align: left; 
                border-bottom: 1px solid rgba(238,238,238,0.5); 
                transition: all 0.3s ease;
            }
            .table.compact th, .table.compact td { 
                padding: 12px 15px; 
                font-size: 0.9rem;
            }
            .table th { 
                background: linear-gradient(135deg, #f8f9fa, #e9ecef); 
                font-weight: 700; 
                color: #333; 
                font-size: 1.1rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .table.compact th { 
                font-size: 0.9rem;
                letter-spacing: 0.3px;
            }
            .table tr { 
                transition: all 0.3s ease;
            }
            .table tr:hover { 
                background: linear-gradient(135deg, rgba(102,126,234,0.05), rgba(118,75,162,0.05)); 
                transform: scale(1.01);
            }
            
            /* Risk Level Badges */
            .risk-badge { 
                padding: 5px 12px; 
                border-radius: 20px; 
                font-size: 0.8rem; 
                font-weight: 600; 
                text-transform: uppercase; 
            }
            .risk-high { background: #f8d7da; color: #721c24; }
            .risk-medium { background: #fff3cd; color: #856404; }
            .risk-low { background: #d4edda; color: #155724; }
            
            /* Loading Spinner */
            .spinner { 
                display: inline-block; 
                width: 20px; 
                height: 20px; 
                border: 3px solid #f3f3f3; 
                border-top: 3px solid #667eea; 
                border-radius: 50%; 
                animation: spin 1s linear infinite; 
            }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            
            /* Footer */
            .footer {
                background: linear-gradient(135deg, rgba(102,126,234,0.9), rgba(118,75,162,0.9));
                color: white;
                padding: 30px 0;
                margin-top: 50px;
                backdrop-filter: blur(20px);
                border-top: 1px solid rgba(255,255,255,0.2);
                box-shadow: 0 -10px 30px rgba(0,0,0,0.1);
            }
            .footer-content {
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 20px;
            }
            .footer-left p, .footer-right p {
                margin: 5px 0;
                font-size: 0.95rem;
                opacity: 0.9;
            }
            .footer-right {
                text-align: right;
            }
            .footer-right strong {
                color: #f0f8ff;
                font-weight: 700;
                text-shadow: 0 0 10px rgba(255,255,255,0.5);
            }
            .footer i {
                margin-right: 8px;
                color: #f0f8ff;
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .header h1 { font-size: 2.5rem; }
                .header p { font-size: 1.1rem; }
                .nav-tabs { flex-direction: column; gap: 5px; }
                .nav-tab { margin-bottom: 5px; padding: 15px 20px; }
                .stats-grid { grid-template-columns: 1fr; gap: 15px; }
                .container { padding: 10px; }
                .dashboard { padding: 20px; }
                .upload-area { padding: 30px 20px; }
                .upload-text { font-size: 1.2rem; }
                .upload-subtext { font-size: 0.9rem; }
                .footer-content {
                    flex-direction: column;
                    text-align: center;
                }
                .footer-right {
                    text-align: center;
                }
                .footer {
                    padding: 20px 0;
                    margin-top: 30px;
                }
            }
            
            @media (max-width: 480px) {
                .header h1 { font-size: 2rem; }
                .header p { font-size: 1rem; }
                .nav-tab { padding: 12px 15px; font-size: 0.9rem; }
                .dashboard { padding: 15px; }
                .upload-area { padding: 20px 15px; }
                .upload-text { font-size: 1.1rem; }
                .upload-subtext { font-size: 0.8rem; }
                .stat-card { padding: 25px; }
                .stat-card h3 { font-size: 2.5rem; }
                .stat-card p { font-size: 1rem; }
                .form-group input, .form-group select { 
                    padding: 12px 15px; 
                    font-size: 16px; /* Prevent zoom on iOS */
                }
                .btn { 
                    padding: 12px 25px; 
                    font-size: 14px; 
                    margin: 5px;
                }
                .result { 
                    padding: 15px; 
                    margin-top: 15px; 
                }
                .file-info { 
                    flex-direction: column; 
                    text-align: center; 
                    gap: 10px; 
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-shield-alt"></i> DataZen</h1>
                <p>AI-Driven Deepfake Detection Platform - IBM Z Datathon 2025</p>
                <div class="creator-info">
                    <p><i class="fas fa-user"></i> Created by <strong>Kadali Krishna</strong></p>
                </div>
            </div>
            
            <!-- Navigation Tabs -->
            <div class="nav-tabs">
                <div class="nav-tab active" onclick="showSection('scan-media')">
                    <i class="fas fa-upload"></i> Scan Media
                </div>
                <div class="nav-tab" onclick="showSection('url-scan')">
                    <i class="fas fa-link"></i> Scan by URL
                </div>
                <div class="nav-tab" onclick="showSection('batch-process')">
                    <i class="fas fa-file-csv"></i> Batch Process
                </div>
            </div>
            
            <!-- Scan Media Section -->
            <div id="scan-media" class="content-section active">
                <div class="dashboard">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h3 id="total-detections">0</h3>
                            <p>Total Detections</p>
                        </div>
                        <div class="stat-card">
                            <h3 id="high-risk">0</h3>
                            <p>High-Risk Incidents</p>
                        </div>
                        <div class="stat-card">
                            <h3 id="verified">0</h3>
                            <p>Verified Threats</p>
                        </div>
                        <div class="stat-card">
                            <h3 id="blockchain">0</h3>
                            <p>Blockchain Entries</p>
                        </div>
                    </div>
                    
                    <div class="upload-section">
                        <h2><i class="fas fa-upload"></i> Upload Media Files</h2>
                        <div class="upload-area" id="uploadArea">
                            <div class="upload-icon">
                                <i class="fas fa-cloud-upload-alt"></i>
                            </div>
                            <div class="upload-text">Drag & Drop files here or click to browse</div>
                            <div class="upload-subtext">Supports: Images (JPG, PNG, GIF), Videos (MP4, AVI, MOV), Audio (WAV, MP3)</div>
                            <input type="file" id="fileInput" multiple accept=".jpg,.jpeg,.png,.gif,.mp4,.avi,.mov,.wav,.mp3" style="display: none;">
                        </div>
                        
                        <div class="file-preview" id="filePreview">
                            <div class="file-info">
                                <div class="file-icon">
                                    <i class="fas fa-file"></i>
                                </div>
                                <div class="file-details">
                                    <h4 id="fileName"></h4>
                                    <p id="fileSize"></p>
                                </div>
                            </div>
                            <button class="btn btn-success" onclick="uploadFile()">
                                <i class="fas fa-upload"></i> Upload & Analyze
                            </button>
                            <button class="btn btn-danger" onclick="clearUpload()">
                                <i class="fas fa-times"></i> Clear
                            </button>
                        </div>
                        
                        <div id="uploadResult" class="result">
                            <h3>Analysis Results</h3>
                            <div id="uploadResultContent"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- URL Scan Section -->
            <div id="url-scan" class="content-section">
                <div class="dashboard">
                    <div class="upload-section">
                        <h2><i class="fas fa-link"></i> Scan Media by URL</h2>
                        <form id="urlScanForm">
                            <div class="form-group">
                                <label for="mediaUrl">Media URL</label>
                                <input type="url" id="mediaUrl" placeholder="https://example.com/video.mp4" required>
                            </div>
                            <div class="form-group">
                                <label for="channelId">Channel ID (Optional - Auto-detected)</label>
                                <input type="text" id="channelId" placeholder="e.g., YouTube, Twitter, Facebook">
                            </div>
                            <button type="submit" class="btn">
                                <i class="fas fa-search"></i> Scan Media
                            </button>
                            <button type="button" class="btn btn-warning" onclick="clearScanResults()">
                                <i class="fas fa-times"></i> Clear Results
                            </button>
                        </form>
                        <div id="urlScanResult" class="result">
                            <h3>Analysis Results</h3>
                            <div id="urlScanResultContent"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Batch Process Section -->
            <div id="batch-process" class="content-section">
                <div class="dashboard">
                    <div class="upload-section">
                        <h2><i class="fas fa-file-csv"></i> Batch Process CSV Files</h2>
                        <div class="upload-area" id="csvUploadArea">
                            <div class="upload-icon">
                                <i class="fas fa-file-csv"></i>
                            </div>
                            <div class="upload-text">Upload CSV file with media URLs</div>
                            <div class="upload-subtext">CSV should have columns: media_url, channel_id (optional)</div>
                            <input type="file" id="csvInput" accept=".csv" style="display: none;">
                        </div>
                        
                        <div class="file-preview" id="csvPreview" style="display: none;">
                            <div class="file-info">
                                <div class="file-icon">
                                    <i class="fas fa-file-csv"></i>
                                </div>
                                <div class="file-details">
                                    <h4 id="csvFileName"></h4>
                                    <p id="csvFileSize"></p>
                                </div>
                            </div>
                            <button class="btn btn-success" onclick="processCSV()">
                                <i class="fas fa-play"></i> Process CSV
                            </button>
                            <button class="btn btn-danger" onclick="clearCSV()">
                                <i class="fas fa-times"></i> Clear
                            </button>
                        </div>
                        
                        <div id="csvResult" class="result">
                            <h3>Batch Processing Results</h3>
                            <div id="csvResultContent"></div>
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
        
        <!-- Footer -->
        <footer class="footer">
            <div class="footer-content">
                <div class="footer-left">
                    <p>&copy; 2025 DataZen - AI-Driven Deepfake Detection Platform</p>
                    <p>IBM Z Datathon 2025</p>
                </div>
                <div class="footer-right">
                    <p><i class="fas fa-user"></i> Created by <strong>Kadali Krishna</strong></p>
                    <p><i class="fas fa-code"></i> Full-Stack Developer</p>
                </div>
            </div>
        </footer>
        
        <script>
            // Global variables
            let selectedFile = null;
            let selectedCSV = null;
            
            // Initialize the application
            document.addEventListener('DOMContentLoaded', function() {
                loadStats();
                setupFileUpload();
                setupCSVUpload();
                setupURLScanForm();
                // Don't initialize charts immediately - wait for analytics section
            });
            
            // Navigation functions
            function showSection(sectionId) {
                // Simple and stable transition
                const currentActive = document.querySelector('.content-section.active');
                const targetSection = document.getElementById(sectionId);
                
                // If clicking the same section, do nothing
                if (currentActive === targetSection) {
                    return;
                }
                
                // Hide all sections
                document.querySelectorAll('.content-section').forEach(section => {
                    section.classList.remove('active');
                });
                
                // Remove active class from all tabs
                document.querySelectorAll('.nav-tab').forEach(tab => {
                    tab.classList.remove('active');
                });
                
                // Show selected section
                targetSection.classList.add('active');
                
                // Add active class to clicked tab
                const clickedTab = document.querySelector(`[onclick*="${sectionId}"]`);
                if (clickedTab) {
                    clickedTab.classList.add('active');
                }
            }
            
            // File upload setup
            function setupFileUpload() {
                const uploadArea = document.getElementById('uploadArea');
                const fileInput = document.getElementById('fileInput');
                
                if (uploadArea && fileInput) {
                    uploadArea.addEventListener('click', () => fileInput.click());
                    uploadArea.addEventListener('dragover', handleDragOver);
                    uploadArea.addEventListener('dragleave', handleDragLeave);
                    uploadArea.addEventListener('drop', handleDrop);
                    fileInput.addEventListener('change', handleFileSelect);
                }
            }
            
            function handleDragOver(e) {
                e.preventDefault();
                e.currentTarget.classList.add('dragover');
            }
            
            function handleDragLeave(e) {
                e.preventDefault();
                e.currentTarget.classList.remove('dragover');
            }
            
            function handleDrop(e) {
                e.preventDefault();
                e.currentTarget.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    handleFile(files[0]);
                }
            }
            
            function handleFileSelect(e) {
                const files = e.target.files;
                if (files.length > 0) {
                    handleFile(files[0]);
                }
            }
            
            function handleFile(file) {
                selectedFile = file;
                const preview = document.getElementById('filePreview');
                const fileName = document.getElementById('fileName');
                const fileSize = document.getElementById('fileSize');
                
                fileName.textContent = file.name;
                fileSize.textContent = formatFileSize(file.size);
                preview.style.display = 'block';
            }
            
            function formatFileSize(bytes) {
                if (bytes === 0) return '0 Bytes';
                const k = 1024;
                const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
            }
            
            async function uploadFile() {
                if (!selectedFile) {
                    alert('Please select a file first');
                    return;
                }
                
                // Check file size (16MB limit)
                if (selectedFile.size > 16 * 1024 * 1024) {
                    alert('File size too large. Maximum size is 16MB.');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', selectedFile);
                
                const resultDiv = document.getElementById('uploadResult');
                const contentDiv = document.getElementById('uploadResultContent');
                
                try {
                    contentDiv.innerHTML = '<div class="spinner"></div> Analyzing file...';
                    resultDiv.style.display = 'block';
                    resultDiv.className = 'result';
                    
                    const response = await fetch('/api/v1/upload', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    
                    contentDiv.innerHTML = `
                        <div class="file-info">
                            <div class="file-icon">
                                <i class="fas fa-file-${getFileTypeIcon(selectedFile.name)}"></i>
                            </div>
                            <div class="file-details">
                                <h4>${selectedFile.name}</h4>
                                <p><strong>Detection ID:</strong> ${data.detection_id || 'N/A'}</p>
                                <p><strong>Deepfake Score:</strong> ${data.deepfake_score || 'N/A'}</p>
                                <p><strong>Sentiment Score:</strong> ${data.sentiment_score || 'N/A'}</p>
                                <p><strong>Risk Level:</strong> <span class="risk-badge risk-${(data.risk_quantification || 'low').toLowerCase()}">${data.risk_quantification || 'Low'}</span></p>
                                <p><strong>Status:</strong> ${data.status || 'Completed'}</p>
                            </div>
                        </div>
                    `;
                    
                    loadStats();
                    
                } catch (error) {
                    contentDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
                    resultDiv.className = 'result error';
                }
            }
            
            function getFileTypeIcon(filename) {
                const ext = filename.split('.').pop().toLowerCase();
                if (['jpg', 'jpeg', 'png', 'gif'].includes(ext)) return 'image';
                if (['mp4', 'avi', 'mov'].includes(ext)) return 'video';
                if (['wav', 'mp3'].includes(ext)) return 'audio';
                return 'file';
            }
            
            function clearUpload() {
                selectedFile = null;
                const filePreview = document.getElementById('filePreview');
                const uploadResult = document.getElementById('uploadResult');
                const fileInput = document.getElementById('fileInput');
                
                if (filePreview) filePreview.style.display = 'none';
                if (uploadResult) uploadResult.style.display = 'none';
                if (fileInput) fileInput.value = '';
            }
            
            // CSV upload setup
            function setupCSVUpload() {
                const csvUploadArea = document.getElementById('csvUploadArea');
                const csvInput = document.getElementById('csvInput');
                
                if (csvUploadArea && csvInput) {
                    csvUploadArea.addEventListener('click', () => csvInput.click());
                    csvInput.addEventListener('change', handleCSVSelect);
                }
            }
            
            function handleCSVSelect(e) {
                const files = e.target.files;
                if (files.length > 0) {
                    selectedCSV = files[0];
                    const preview = document.getElementById('csvPreview');
                    const fileName = document.getElementById('csvFileName');
                    const fileSize = document.getElementById('csvFileSize');
                    
                    fileName.textContent = files[0].name;
                    fileSize.textContent = formatFileSize(files[0].size);
                    preview.style.display = 'block';
                }
            }
            
            async function processCSV() {
                if (!selectedCSV) return;
                
                const formData = new FormData();
                formData.append('csv', selectedCSV);
                
                const resultDiv = document.getElementById('csvResult');
                const contentDiv = document.getElementById('csvResultContent');
                
                try {
                    contentDiv.innerHTML = '<div class="spinner"></div> Processing CSV file...';
                    resultDiv.style.display = 'block';
                    resultDiv.className = 'result';
                    
                    const response = await fetch('/api/v1/batch', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    
                    contentDiv.innerHTML = `
                        <div class="file-info">
                            <div class="file-icon">
                                <i class="fas fa-file-csv"></i>
                            </div>
                            <div class="file-details">
                                <h4>${selectedCSV.name}</h4>
                                <p><strong>Total URLs:</strong> ${data.total_urls || 0}</p>
                                <p><strong>Processed:</strong> ${data.processed || 0}</p>
                                <p><strong>High Risk:</strong> ${data.high_risk || 0}</p>
                                <p><strong>Medium Risk:</strong> ${data.medium_risk || 0}</p>
                                <p><strong>Low Risk:</strong> ${data.low_risk || 0}</p>
                            </div>
                        </div>
                    `;
                    
                    loadStats();
                    
                } catch (error) {
                    contentDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
                    resultDiv.className = 'result error';
                }
            }
            
            function clearCSV() {
                selectedCSV = null;
                const csvPreview = document.getElementById('csvPreview');
                const csvResult = document.getElementById('csvResult');
                const csvInput = document.getElementById('csvInput');
                
                if (csvPreview) csvPreview.style.display = 'none';
                if (csvResult) csvResult.style.display = 'none';
                if (csvInput) csvInput.value = '';
            }
            
            // URL scan functions
            function setupURLScanForm() {
                const form = document.getElementById('urlScanForm');
                if (form) {
                    form.addEventListener('submit', async function(e) {
                        e.preventDefault();
                        
                        const mediaUrl = document.getElementById('mediaUrl').value.trim();
                        const channelId = document.getElementById('channelId').value.trim();
                        
                        // Validate URL
                        if (!mediaUrl) {
                            alert('Please enter a media URL');
                            return;
                        }
                        
                        try {
                            new URL(mediaUrl);
                        } catch (e) {
                            alert('Please enter a valid URL');
                            return;
                        }
                        
                        const resultDiv = document.getElementById('urlScanResult');
                        const contentDiv = document.getElementById('urlScanResultContent');
                        
                        try {
                            contentDiv.innerHTML = '<div class="spinner"></div> Analyzing URL...';
                            resultDiv.style.display = 'block';
                            resultDiv.className = 'result';
                            
                            const response = await fetch('/api/v1/scan', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    media_url: mediaUrl,
                                    channel_id: channelId || 'Unknown_Source'
                                })
                            });
                            
                            if (!response.ok) {
                                throw new Error(`HTTP error! status: ${response.status}`);
                            }
                            
                            const data = await response.json();
                            
                            if (data.error) {
                                throw new Error(data.error);
                            }
                            
                            contentDiv.innerHTML = `
                                <div class="file-info">
                                    <div class="file-icon">
                                        <i class="fas fa-link"></i>
                                    </div>
                                    <div class="file-details">
                                        <h4>${mediaUrl}</h4>
                                        <p><strong>Detection ID:</strong> ${data.detection_id || 'N/A'}</p>
                                        <p><strong>Deepfake Score:</strong> ${data.deepfake_score || 'N/A'}</p>
                                        <p><strong>Sentiment Score:</strong> ${data.sentiment_score || 'N/A'}</p>
                                        <p><strong>Risk Level:</strong> <span class="risk-badge risk-${(data.risk_quantification || 'low').toLowerCase()}">${data.risk_quantification || 'Low'}</span></p>
                                        <p><strong>Status:</strong> ${data.status || 'Completed'}</p>
                                    </div>
                                </div>
                            `;
                            
                            loadStats();
                            
                        } catch (error) {
                            contentDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
                            resultDiv.className = 'result error';
                        }
                    });
                }
            }
            
            function clearScanResults() {
                const urlScanResult = document.getElementById('urlScanResult');
                const mediaUrl = document.getElementById('mediaUrl');
                const channelId = document.getElementById('channelId');
                
                if (urlScanResult) urlScanResult.style.display = 'none';
                if (mediaUrl) mediaUrl.value = '';
                if (channelId) channelId.value = '';
            }
            
            // Statistics and analytics
            async function loadStats() {
                try {
                    const response = await fetch('/api/v1/stats');
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    
                    if (data.error) {
                        throw new Error(data.error);
                    }
                    
                    const totalEl = document.getElementById('total-detections');
                    const highRiskEl = document.getElementById('high-risk');
                    const verifiedEl = document.getElementById('verified');
                    const blockchainEl = document.getElementById('blockchain');
                    
                    if (totalEl) totalEl.textContent = data.total_detections || 0;
                    if (highRiskEl) highRiskEl.textContent = data.high_risk_incidents || 0;
                    if (verifiedEl) verifiedEl.textContent = data.verified_incidents || 0;
                    if (blockchainEl) blockchainEl.textContent = data.blockchain_entries || 0;
                } catch (error) {
                    console.error('Error loading stats:', error);
                    // Set fallback values
                    const totalEl = document.getElementById('total-detections');
                    const highRiskEl = document.getElementById('high-risk');
                    const verifiedEl = document.getElementById('verified');
                    const blockchainEl = document.getElementById('blockchain');
                    
                    if (totalEl) totalEl.textContent = '0';
                    if (highRiskEl) highRiskEl.textContent = '0';
                    if (verifiedEl) verifiedEl.textContent = '0';
                    if (blockchainEl) blockchainEl.textContent = '0';
                }
            }
            
            
            
            
            
        </script>
    </body>
    </html>
    '''

@app.route('/api/v1/scan', methods=['POST'])
def scan_media():
    """Scan media URL for deepfake detection"""
    try:
        # Add to incidents for tracking
        global incidents, blockchain_ledger, block_number
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
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
        
        # Simulate AI analysis
        deepfake_score = round(random.uniform(0.1, 0.95), 3)
        sentiment_score = round(random.uniform(-1.0, 1.0), 3)
        risk_level = calculate_risk_level(deepfake_score, sentiment_score)
        
        # Create detection ID
        detection_id = f"scan_{len(incidents) + 1}_{int(datetime.now().timestamp())}"
        incident = {
            'detection_id': detection_id,
            'media_url': media_url,
            'channel_id': channel_id,
            'deepfake_score': deepfake_score,
            'sentiment_score': sentiment_score,
            'risk_quantification': risk_level,
            'timestamp': datetime.now().isoformat(),
            'blockchain_hash': None,
            'status': 'Analysis completed'
        }
        
        # Add to blockchain if high risk
        if risk_level == "High":
            blockchain_hash = generate_mock_ethereum_hash()
            incident['blockchain_hash'] = blockchain_hash
            
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
        
        return jsonify({
            'detection_id': detection_id,
            'deepfake_score': deepfake_score,
            'sentiment_score': sentiment_score,
            'risk_quantification': risk_level,
            'timestamp': incident['timestamp'],
            'blockchain_hash': incident['blockchain_hash'],
            'status': 'Analysis completed'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/upload', methods=['POST'])
def upload_file():
    """Upload and analyze media file"""
    try:
        # Add to incidents for tracking
        global incidents, blockchain_ledger, block_number
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Simulate file upload processing
        deepfake_score = round(random.uniform(0.1, 0.9), 2)
        sentiment_score = round(random.uniform(-0.8, 0.8), 2)
        risk_level = calculate_risk_level(deepfake_score, sentiment_score)
        
        # Create detection ID
        detection_id = f'file_{random.randint(1000, 9999)}'
        incident = {
            'detection_id': detection_id,
            'filename': file.filename,
            'deepfake_score': deepfake_score,
            'sentiment_score': sentiment_score,
            'risk_quantification': risk_level,
            'timestamp': datetime.now().isoformat(),
            'blockchain_hash': generate_mock_ethereum_hash() if risk_level == 'High' else None,
            'status': 'File analysis completed successfully'
        }
        incidents.append(incident)
        
        return jsonify({
            'detection_id': detection_id,
            'filename': file.filename,
            'deepfake_score': deepfake_score,
            'sentiment_score': sentiment_score,
            'risk_quantification': risk_level,
            'timestamp': incident['timestamp'],
            'blockchain_hash': incident['blockchain_hash'],
            'status': 'File analysis completed successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/batch', methods=['POST'])
def batch_process():
    """Process CSV file with multiple media URLs"""
    try:
        # Add to incidents for tracking
        global incidents, blockchain_ledger, block_number
        
        # Check if CSV file was uploaded
        if 'csv' not in request.files:
            return jsonify({'error': 'No CSV file provided'}), 400
        
        file = request.files['csv']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read CSV content
        csv_content = file.read().decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        # Process each row
        processed_count = 0
        high_risk_count = 0
        medium_risk_count = 0
        low_risk_count = 0
        
        for row in csv_reader:
            try:
                media_url = row.get('media_url', '').strip()
                if not media_url:
                    continue
                
                # Simulate analysis
                deepfake_score = round(random.uniform(0.1, 0.9), 2)
                sentiment_score = round(random.uniform(-0.8, 0.8), 2)
                risk_level = calculate_risk_level(deepfake_score, sentiment_score)
                
                # Count by risk level
                if risk_level == 'High':
                    high_risk_count += 1
                elif risk_level == 'Medium':
                    medium_risk_count += 1
                else:
                    low_risk_count += 1
                
                processed_count += 1
                
            except Exception as e:
                continue
        
        return jsonify({
            'total_urls': processed_count,
            'processed': processed_count,
            'high_risk': high_risk_count,
            'medium_risk': medium_risk_count,
            'low_risk': low_risk_count,
            'status': 'Batch processing completed successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        global incidents, blockchain_ledger
        
        total_detections = len(incidents)
        high_risk_count = len([i for i in incidents if i.get('risk_quantification') == 'High'])
        medium_risk_count = len([i for i in incidents if i.get('risk_quantification') == 'Medium'])
        low_risk_count = len([i for i in incidents if i.get('risk_quantification') == 'Low'])
        
        # Determine current risk level
        if high_risk_count > 0:
            current_risk_level = 'Elevated'
        elif medium_risk_count > 2:
            current_risk_level = 'Moderate'
        else:
            current_risk_level = 'Normal'
        
        return jsonify({
            'total_detections': total_detections,
            'high_risk_incidents': high_risk_count,
            'medium_risk_incidents': medium_risk_count,
            'low_risk_incidents': low_risk_count,
            'verified_incidents': len([i for i in incidents if i.get('status', '').startswith('Verified')]),
            'blockchain_entries': len(blockchain_ledger),
            'current_risk_level': current_risk_level,
            'status': 'API working correctly'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/incidents', methods=['GET'])
def get_incidents():
    """Get all incidents"""
    try:
        global incidents
        return jsonify(incidents), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/blockchain', methods=['GET'])
def get_blockchain():
    """Get blockchain ledger"""
    try:
        global blockchain_ledger
        return jsonify(blockchain_ledger), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/clear', methods=['POST'])
def clear_data():
    """Clear all data (for testing)"""
    try:
        global incidents, blockchain_ledger, block_number
        incidents.clear()
        blockchain_ledger.clear()
        block_number = 1
        return jsonify({'message': 'All data cleared successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# For Vercel deployment
application = app

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
