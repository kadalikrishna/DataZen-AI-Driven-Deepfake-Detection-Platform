/**
 * DataZen - AI Deepfake Detection Platform
 * Frontend Application Logic
 */

// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// Global state
let currentView = 'scan';
let incidents = [];
let blockchainData = [];

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeFileUpload();
    // Set Scan Media as default home page
    switchView('scan');
});

/**
 * Navigation Management
 */
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Update active link
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Switch view
            const view = this.getAttribute('data-view');
            switchView(view);
        });
    });
}

function switchView(viewName) {
    // Get current active view
    const currentActiveView = document.querySelector('.view.active');
    
    // Add exit animation to current view
    if (currentActiveView) {
        currentActiveView.classList.add('exit');
        
        // Wait for exit animation to complete
        setTimeout(() => {
            currentActiveView.classList.remove('active', 'exit');
        }, 400);
    }
    
    // Show new view after a slight delay for smooth transition
    setTimeout(() => {
        const targetView = document.getElementById(`${viewName}-view`);
        if (targetView) {
            targetView.classList.add('active');
            currentView = viewName;
            
            // Smooth scroll to top
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
            
            // Load data for the view
            switch(viewName) {
                case 'dashboard':
                    loadDashboard();
                    break;
                case 'scan':
                    // Scan view is static, no loading needed
                    break;
            }
        }
    }, 200);
}

/**
 * Dashboard Functions
 */
async function loadDashboard() {
    try {
        // Load statistics
        const stats = await fetchAPI('/api/v1/stats');
        updateKPIs(stats);
        updateRiskBanner(stats.overall_risk_level);
        
        // Load incidents
        const incidentsData = await fetchAPI('/api/v1/incidents?risk=High');
        incidents = incidentsData.incidents || [];
        displayTopIncidents(incidents.slice(0, 5));
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showToast('Failed to load dashboard data', 'error');
    }
}

function updateKPIs(stats) {
    document.getElementById('total-detections').textContent = stats.total_detections || 0;
    document.getElementById('high-risk-count').textContent = stats.high_risk_incidents || 0;
    document.getElementById('verified-count').textContent = stats.verified_incidents || 0;
    document.getElementById('blockchain-count').textContent = stats.blockchain_entries || 0;
}

function updateRiskBanner(riskLevel) {
    const banner = document.getElementById('risk-banner');
    const riskLevelSpan = document.getElementById('risk-level');
    
    // Remove all risk classes
    banner.classList.remove('elevated', 'high');
    
    // Add appropriate class
    if (riskLevel === 'Elevated') {
        banner.classList.add('elevated');
    } else if (riskLevel === 'High') {
        banner.classList.add('high');
    }
    
    riskLevelSpan.textContent = riskLevel;
}

function displayTopIncidents(incidentsList) {
    const tbody = document.getElementById('top-incidents-tbody');
    
    if (incidentsList.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="no-data">No high-risk incidents detected</td></tr>';
        return;
    }
    
    tbody.innerHTML = incidentsList.map(incident => `
        <tr>
            <td><code>${incident.detection_id.substring(0, 8)}...</code></td>
            <td>${truncateUrl(incident.media_url)}</td>
            <td>
                ${createScoreBar(incident.deepfake_score, 'deepfake')}
                <small>${(incident.deepfake_score * 100).toFixed(0)}%</small>
            </td>
            <td>
                ${createScoreBar((incident.sentiment_score + 1) / 2, 'sentiment')}
                <small>${incident.sentiment_score.toFixed(2)}</small>
            </td>
            <td><span class="badge ${incident.risk_quantification.toLowerCase()}">${incident.risk_quantification}</span></td>
            <td><span class="badge ${incident.verified ? 'verified' : 'pending'}">${incident.status}</span></td>
            <td>${formatTimestamp(incident.timestamp)}</td>
        </tr>
    `).join('');
}

function createScoreBar(score, type) {
    let riskClass = 'low';
    
    if (type === 'deepfake') {
        if (score > 0.7) riskClass = 'high';
        else if (score > 0.5) riskClass = 'medium';
    } else if (type === 'sentiment') {
        // Sentiment score is normalized between 0 and 1
        if (score < 0.3) riskClass = 'high';
        else if (score < 0.5) riskClass = 'medium';
    }
    
    const percentage = (score * 100).toFixed(0);
    
    return `
        <div class="score-bar">
            <div class="score-fill ${riskClass}" style="width: ${percentage}%"></div>
        </div>
    `;
}

function refreshDashboard() {
    showToast('Refreshing dashboard...', 'info');
    loadDashboard();
}


// Search functionality for audit trail
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('audit-search');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            if (blockchainData.length === 0) return;
            
            const filtered = blockchainData.filter(entry => {
                return entry.transaction_hash.toLowerCase().includes(searchTerm) ||
                       (entry.data.detection_id && entry.data.detection_id.toLowerCase().includes(searchTerm)) ||
                       (entry.data.action && entry.data.action.toLowerCase().includes(searchTerm));
            });
            
            displayAuditTrail(filtered);
        });
    }
});

/**
 * Scan Media Functions
 */
function detectChannelFromUrl(url) {
    // Auto-detect platform from URL
    try {
        const urlLower = url.toLowerCase();
        
        if (urlLower.includes('youtube.com') || urlLower.includes('youtu.be')) {
            return 'YouTube';
        } else if (urlLower.includes('twitter.com') || urlLower.includes('x.com')) {
            return 'Twitter';
        } else if (urlLower.includes('facebook.com') || urlLower.includes('fb.com')) {
            return 'Facebook';
        } else if (urlLower.includes('instagram.com')) {
            return 'Instagram';
        } else if (urlLower.includes('tiktok.com')) {
            return 'TikTok';
        } else if (urlLower.includes('linkedin.com')) {
            return 'LinkedIn';
        } else if (urlLower.includes('reddit.com')) {
            return 'Reddit';
        } else if (urlLower.includes('vimeo.com')) {
            return 'Vimeo';
        } else {
            // Extract domain name as fallback
            const hostname = new URL(url).hostname.replace('www.', '');
            return hostname.split('.')[0].charAt(0).toUpperCase() + hostname.split('.')[0].slice(1);
        }
    } catch (e) {
        return 'Unknown_Source';
    }
}

async function submitScan(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = document.getElementById('scan-submit-btn');
    const resultDiv = document.getElementById('scan-result');
    const resultContent = document.getElementById('result-content');
    
    // Get form data
    const mediaUrl = document.getElementById('media-url').value;
    let channelId = document.getElementById('channel-id').value;
    
    // Auto-detect channel from URL if not provided
    if (!channelId || channelId.trim() === '') {
        channelId = detectChannelFromUrl(mediaUrl);
    }
    
    // Disable button
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scanning...';
    
    try {
        const result = await fetchAPI('/api/v1/scan', 'POST', {
            media_url: mediaUrl,
            channel_id: channelId
        });
        
        // Display results
        resultContent.innerHTML = `
            <div class="detail-item">
                <label>Detection ID</label>
                <div class="value"><code>${result.detection_id.substring(0, 16)}...</code></div>
            </div>
            <div class="detail-item">
                <label>Deepfake Score</label>
                <div class="value">${(result.deepfake_score * 100).toFixed(0)}%</div>
            </div>
            <div class="detail-item">
                <label>Sentiment Score</label>
                <div class="value">${result.sentiment_score.toFixed(2)}</div>
            </div>
            <div class="detail-item">
                <label>Risk Level</label>
                <div class="value">
                    <span class="badge ${result.risk_quantification.toLowerCase()}">${result.risk_quantification}</span>
                </div>
            </div>
            <div class="detail-item">
                <label>Status</label>
                <div class="value">
                    <span class="badge ${result.status.includes('Review') ? 'pending' : 'verified'}">${result.status}</span>
                </div>
            </div>
            <div class="detail-item">
                <label>Timestamp</label>
                <div class="value">${formatTimestamp(result.timestamp)}</div>
            </div>
        `;
        
        resultDiv.classList.remove('hidden');
        showToast('Media scan completed successfully', 'success');
        
    } catch (error) {
        console.error('Error scanning media:', error);
        showToast('Failed to scan media', 'error');
    } finally {
        // Re-enable button
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-scan"></i> Scan Media';
    }
}

/**
 * File Upload Functions
 */
function initializeFileUpload() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    
    if (!uploadArea || !fileInput) return;
    
    // Click to upload
    uploadArea.addEventListener('click', function(e) {
        if (e.target.tagName !== 'BUTTON') {
            fileInput.click();
        }
    });
    
    // File selection
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });
}

function handleFileSelection(file) {
    const filePreview = document.getElementById('file-preview');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const fileType = document.getElementById('file-type');
    const fileIcon = document.getElementById('file-icon');
    const uploadResult = document.getElementById('upload-result');
    
    // Hide previous results when selecting new file
    if (uploadResult) {
        uploadResult.classList.add('hidden');
    }
    
    // Show preview
    filePreview.classList.remove('hidden');
    
    // Set file details
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    
    // Determine file type and icon
    const ext = file.name.split('.').pop().toLowerCase();
    let type = 'file';
    let iconClass = 'fa-file';
    
    if (['png', 'jpg', 'jpeg', 'gif'].includes(ext)) {
        type = 'image';
        iconClass = 'fa-file-image';
        fileType.textContent = 'Image File';
    } else if (['mp4', 'avi', 'mov', 'wmv', 'webm'].includes(ext)) {
        type = 'video';
        iconClass = 'fa-file-video';
        fileType.textContent = 'Video File';
    } else if (['mp3', 'wav', 'ogg'].includes(ext)) {
        type = 'audio';
        iconClass = 'fa-file-audio';
        fileType.textContent = 'Audio File';
    }
    
    // Update icon
    fileIcon.className = `fas ${iconClass} ${type}`;
}

function clearFileSelection() {
    const fileInput = document.getElementById('file-input');
    const filePreview = document.getElementById('file-preview');
    const uploadResult = document.getElementById('upload-result');
    
    fileInput.value = '';
    filePreview.classList.add('hidden');
    uploadResult.classList.add('hidden');
}

function clearUploadResults() {
    const uploadResult = document.getElementById('upload-result');
    const fileInput = document.getElementById('file-input');
    const filePreview = document.getElementById('file-preview');
    const uploadForm = document.getElementById('upload-form');
    
    // Hide results
    uploadResult.classList.add('hidden');
    
    // Clear file selection
    fileInput.value = '';
    filePreview.classList.add('hidden');
    
    // Reset form
    if (uploadForm) {
        uploadForm.reset();
    }
    
    showToast('Ready for new upload', 'info');
}

function clearScanResults() {
    const scanResult = document.getElementById('scan-result');
    const scanForm = document.getElementById('scan-form');
    
    // Hide results
    if (scanResult) {
        scanResult.classList.add('hidden');
    }
    
    // Reset form
    if (scanForm) {
        scanForm.reset();
    }
    
    showToast('Ready for new scan', 'info');
}

async function submitFileUpload(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = document.getElementById('upload-submit-btn');
    const resultDiv = document.getElementById('upload-result');
    const resultContent = document.getElementById('upload-result-content');
    const fileInput = document.getElementById('file-input');
    const channelId = document.getElementById('upload-channel-id').value || 'Upload_Channel';
    
    // Check if file is selected
    if (!fileInput.files || fileInput.files.length === 0) {
        showToast('Please select a file to upload', 'error');
        return;
    }
    
    const file = fileInput.files[0];
    
    // Disable button
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing File...';
    
    try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', file);
        formData.append('channel_id', channelId);
        
        // Upload file
        const response = await fetch(`${API_BASE_URL}/api/v1/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Upload failed');
        }
        
        const result = await response.json();
        
        // Display results
        resultContent.innerHTML = `
            <div class="detail-item">
                <label>Filename</label>
                <div class="value">${result.filename}</div>
            </div>
            <div class="detail-item">
                <label>File Type</label>
                <div class="value">${result.file_type.toUpperCase()}</div>
            </div>
            <div class="detail-item">
                <label>File Size</label>
                <div class="value">${formatFileSize(result.file_size)}</div>
            </div>
            <div class="detail-item">
                <label>Detection ID</label>
                <div class="value"><code>${result.detection_id.substring(0, 16)}...</code></div>
            </div>
            <div class="detail-item">
                <label>Deepfake Score</label>
                <div class="value">${(result.deepfake_score * 100).toFixed(0)}%</div>
                ${createScoreBar(result.deepfake_score, 'deepfake')}
            </div>
            <div class="detail-item">
                <label>Sentiment Score</label>
                <div class="value">${result.sentiment_score.toFixed(2)}</div>
                ${createScoreBar((result.sentiment_score + 1) / 2, 'sentiment')}
            </div>
            <div class="detail-item">
                <label>Risk Level</label>
                <div class="value">
                    <span class="badge ${result.risk_quantification.toLowerCase()}">${result.risk_quantification}</span>
                </div>
            </div>
            <div class="detail-item">
                <label>Status</label>
                <div class="value">
                    <span class="badge ${result.status.includes('Review') ? 'pending' : 'verified'}">${result.status}</span>
                </div>
            </div>
        `;
        
        resultDiv.classList.remove('hidden');
        showToast('File analyzed successfully!', 'success');
        
        // Don't auto-clear - let user review results
        // User can upload another file or manually clear
        
    } catch (error) {
        console.error('Error uploading file:', error);
        showToast(error.message || 'Failed to analyze file', 'error');
    } finally {
        // Re-enable button
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-check-circle"></i> Analyze Uploaded File';
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Batch CSV Processing Functions
 */
async function submitCSVBatch(event) {
    event.preventDefault();
    
    const form = event.target;
    const submitBtn = document.getElementById('csv-submit-btn');
    const resultDiv = document.getElementById('batch-result');
    const summaryDiv = document.getElementById('batch-summary');
    const detailsDiv = document.getElementById('batch-details');
    const fileInput = document.getElementById('csv-file');
    
    // Check if file is selected
    if (!fileInput.files || fileInput.files.length === 0) {
        showToast('Please select a CSV file', 'error');
        return;
    }
    
    const file = fileInput.files[0];
    
    // Disable button
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing Batch...';
    
    try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', file);
        
        // Upload CSV
        const response = await fetch(`${API_BASE_URL}/api/v1/batch/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Batch upload failed');
        }
        
        const result = await response.json();
        
        // Display summary
        summaryDiv.innerHTML = `
            <div class="batch-summary-grid">
                <div class="summary-item success">
                    <i class="fas fa-check-circle"></i>
                    <div>
                        <strong>${result.total_processed}</strong>
                        <span>Items Processed</span>
                    </div>
                </div>
                <div class="summary-item danger">
                    <i class="fas fa-exclamation-triangle"></i>
                    <div>
                        <strong>${result.high_risk_detected}</strong>
                        <span>High-Risk Detected</span>
                    </div>
                </div>
            </div>
        `;
        
        // Display individual results
        detailsDiv.innerHTML = result.results.map((item, index) => `
            <div class="detail-item">
                <label>#${index + 1} - ${truncateUrl(item.media_url, 40)}</label>
                <div class="value">
                    ${item.error ? 
                        `<span class="badge" style="background: #fee2e2; color: #dc2626;">Error: ${item.error}</span>` :
                        `
                        <span class="badge ${item.risk.toLowerCase()}">${item.risk}</span>
                        <small style="margin-left: 10px;">Deepfake: ${(item.deepfake_score * 100).toFixed(0)}%</small>
                        `
                    }
                </div>
            </div>
        `).join('');
        
        resultDiv.classList.remove('hidden');
        showToast(`Batch processed: ${result.total_processed} items, ${result.high_risk_detected} high-risk`, 'success');
        
        // Reset form
        form.reset();
        
    } catch (error) {
        console.error('Error processing CSV batch:', error);
        showToast(error.message || 'Failed to process CSV batch', 'error');
    } finally {
        // Re-enable button
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-rocket"></i> Process Batch';
    }
}

function clearBatchResults() {
    const batchResult = document.getElementById('batch-result');
    const csvForm = document.getElementById('csv-upload-form');
    
    batchResult.classList.add('hidden');
    
    if (csvForm) {
        csvForm.reset();
    }
    
    showToast('Ready for new batch', 'info');
}

async function exportToCSV() {
    try {
        showToast('Generating CSV export...', 'info');
        
        // Download the CSV file
        const response = await fetch(`${API_BASE_URL}/api/v1/batch/export`);
        
        if (!response.ok) {
            throw new Error('Export failed');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `deepfake_incidents_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        showToast('CSV exported successfully!', 'success');
        
    } catch (error) {
        console.error('Error exporting CSV:', error);
        showToast('Failed to export CSV', 'error');
    }
}


/**
 * Utility Functions
 */
async function fetchAPI(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    
    if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
    }
    
    return await response.json();
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    
    // Remove previous type classes
    toast.classList.remove('success', 'error', 'warning', 'info');
    
    // Add new type class
    toast.classList.add(type);
    
    // Set message
    toastMessage.textContent = message;
    
    // Show toast
    toast.classList.remove('hidden');
    
    // Hide after 3 seconds
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    // If less than 1 minute
    if (diff < 60000) {
        return 'Just now';
    }
    // If less than 1 hour
    else if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    }
    // If less than 24 hours
    else if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    }
    // Otherwise show date
    else {
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

function truncateUrl(url, maxLength = 50) {
    if (url.length <= maxLength) return url;
    return url.substring(0, maxLength) + '...';
}

// Close modal when clicking outside
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('incident-modal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }
});

