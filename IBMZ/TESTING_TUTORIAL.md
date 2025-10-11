# 🧪 Complete Testing Tutorial

## How to Test Your Deepfake Detection Platform

---

## 📚 **Table of Contents**

1. [Single File Testing](#single-file-testing)
2. [URL Testing](#url-testing)
3. [CSV Batch Testing](#csv-batch-testing)
4. [Creating Test Datasets](#creating-test-datasets)
5. [Analyzing Results](#analyzing-results)
6. [Export & Reporting](#export-reporting)

---

## 🎯 **Testing Methods Overview:**

```
┌─────────────────────────────────────────────┐
│            TESTING METHODS                  │
├─────────────────────────────────────────────┤
│                                             │
│  1. SINGLE FILE UPLOAD                      │
│     📤 Upload one image/video/audio        │
│     ⚡ Quick individual tests              │
│     Use: Testing specific files            │
│                                             │
│  2. URL SCANNING                            │
│     🔗 Enter media URL                     │
│     ⚡ Fast remote content check           │
│     Use: Checking online content           │
│                                             │
│  3. CSV BATCH TESTING ⭐                   │
│     📊 Upload CSV with multiple URLs       │
│     ⚡ Process 10-1000+ at once           │
│     Use: Bulk testing, demos, research     │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 1. 📤 Single File Testing

### **When to Use:**
- Testing specific suspicious files
- Demonstrating file upload feature
- Analyzing individual media items

### **How to Test:**

**Step 1: Prepare Test Files**

Create test images, videos, or audio files:

```bash
# Create a test image
echo "Test image data" > test.jpg

# Or use existing files from your computer
# Photos, screenshots, videos, audio recordings
```

**Step 2: Upload via Web Interface**

1. Open: http://localhost:5000
2. Go to: "Scan Media" tab
3. Section: "Upload File for Analysis"
4. **Drag & drop** or click "Select File"
5. Choose your test file
6. Click "Analyze Uploaded File"

**Step 3: View Results**

```
Results Display:
┌─────────────────────────────────────┐
│ Filename: test.jpg                  │
│ File Type: IMAGE                    │
│ File Size: 125 KB                   │
│ Deepfake Score: 67% [████████▒▒▒] │
│ Sentiment Score: -0.42              │
│ Risk Level: [MEDIUM]                │
│ Status: Auto-Processed              │
└─────────────────────────────────────┘
```

**Supported Formats:**
- 🖼️ Images: PNG, JPG, GIF
- 🎥 Videos: MP4, AVI, MOV, WEBM
- 🎵 Audio: MP3, WAV, OGG

---

## 2. 🔗 URL Testing

### **When to Use:**
- Quick verification of online content
- Testing platform detection
- Checking social media posts

### **How to Test:**

**Step 1: Find Test URLs**

Use any of these:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://twitter.com/user/status/123456789
https://www.facebook.com/video/12345
https://example.com/media/video.mp4
```

**Step 2: Submit via Web Interface**

1. Go to: "Scan Media" tab
2. Section: "Scan by URL"
3. Paste URL
4. Leave Channel ID blank (auto-detects!)
5. Click "Scan Media"

**Step 3: View Results**

```
Scan Results:
┌─────────────────────────────────────┐
│ Detection ID: 8a233d29...           │
│ Deepfake Score: 21%                 │
│ Sentiment Score: 0.36               │
│ Risk Level: [LOW]                   │
│ Status: Auto-Processed              │
│ Channel: YouTube (auto-detected)    │
└─────────────────────────────────────┘
```

**Auto-Detected Platforms:**
- YouTube, Twitter, Facebook, Instagram
- TikTok, LinkedIn, Reddit, Vimeo
- Any domain name

---

## 3. 📊 CSV Batch Testing ⭐ **NEW!**

### **When to Use:**
- Testing multiple items quickly
- Demonstration purposes
- Research and analysis
- Performance benchmarking

### **How to Test:**

#### **Option A: Use Sample Dataset**

1. **Download Sample CSV:**
   - Open: http://localhost:5000
   - Go to: "Scan Media" tab
   - Find: "Batch Testing with CSV" section
   - Click: "Download Sample CSV"
   - Saves: `test_dataset.csv`

2. **Upload for Processing:**
   - In same section
   - Click "Choose File"
   - Select downloaded CSV
   - Click "Process Batch"

3. **View Results:**
   ```
   Summary:
   ┌─────────────────────┬─────────────────────┐
   │ ✅ 10 Items        │ ⚠️ 1 High-Risk    │
   │    Processed        │    Detected         │
   └─────────────────────┴─────────────────────┘
   
   Individual Results:
   #1 - youtube.com/... [LOW] 49%
   #2 - twitter.com/... [HIGH] 85% ⚠️
   #3 - facebook.com/... [MEDIUM] 40%
   ...
   ```

#### **Option B: Create Custom Dataset**

**Create CSV File:**

```bash
cd /home/p/dp/IBMZ

cat > custom_test.csv << 'EOF'
media_url,channel_id,description
https://youtube.com/political-fake,YouTube,Fake political speech
https://twitter.com/scam-celebrity,Twitter,Celebrity scam endorsement
https://facebook.com/health-misinfo,Facebook,Health misinformation
https://tiktok.com/financial-scam,TikTok,Financial advice scam
https://instagram.com/product-fake,Instagram,Fake product review
EOF
```

**Upload via Command Line:**

```bash
curl -X POST http://localhost:5000/api/v1/batch/upload \
  -F "file=@custom_test.csv" \
  | python3 -m json.tool
```

**Output:**
```json
{
  "message": "Batch processing completed",
  "total_processed": 5,
  "high_risk_detected": 2,
  "results": [
    {
      "detection_id": "uuid-1",
      "media_url": "https://youtube.com/political-fake",
      "risk": "High",
      "deepfake_score": 0.89
    },
    // ... more results
  ]
}
```

---

## 4. 📝 Creating Test Datasets

### **Template 1: Platform Comparison**

Test which platforms have more deepfakes:

```csv
media_url,channel_id,description
https://youtube.com/test1,YouTube,YouTube test 1
https://youtube.com/test2,YouTube,YouTube test 2
https://youtube.com/test3,YouTube,YouTube test 3
https://twitter.com/test1,Twitter,Twitter test 1
https://twitter.com/test2,Twitter,Twitter test 2
https://twitter.com/test3,Twitter,Twitter test 3
https://facebook.com/test1,Facebook,Facebook test 1
https://facebook.com/test2,Facebook,Facebook test 2
https://facebook.com/test3,Facebook,Facebook test 3
```

**Analysis:** Compare risk levels per platform

---

### **Template 2: Content Type Testing**

```csv
media_url,channel_id,description
https://site.com/political1,YouTube,Political speech
https://site.com/political2,YouTube,Political debate
https://site.com/celebrity1,Instagram,Celebrity endorsement
https://site.com/celebrity2,TikTok,Celebrity message
https://site.com/financial1,LinkedIn,Financial advice
https://site.com/financial2,YouTube,Investment tips
https://site.com/health1,Facebook,Health claims
https://site.com/health2,YouTube,Medical advice
```

**Analysis:** Which content types are most targeted

---

### **Template 3: Stress Test**

**Generate Large Dataset:**

```python
# generate_large_test.py
import csv

with open('stress_test_1000.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['media_url', 'channel_id', 'description'])
    
    for i in range(1000):
        writer.writerow([
            f'https://testsite.com/media/video_{i:04d}.mp4',
            'Test_Platform',
            f'Stress test item {i+1} of 1000'
        ])

print("✅ Created stress_test_1000.csv with 1000 test URLs")
```

**Run:**
```bash
python3 generate_large_test.py
curl -X POST http://localhost:5000/api/v1/batch/upload -F "file=@stress_test_1000.csv"
```

---

## 5. 📊 Analyzing Results

### **Method 1: Web Dashboard**

After batch upload:

1. **Click "Dashboard" tab**
   - View updated statistics
   - See total detections increase
   - Check risk distribution

2. **Click "Expert Review"**
   - See high-risk items from batch
   - Review each one
   - Verify threats

3. **Click "Audit Trail"**
   - View blockchain entries
   - Search by detection ID
   - Verify immutability

---

### **Method 2: Export to CSV**

**Steps:**

1. **Click "Scan Media" tab**
2. **Scroll to "Export Results"**
3. **Click "Export All Incidents to CSV"**
4. **File downloads:** `deepfake_incidents_2025-10-11.csv`

**Open in Excel/Google Sheets:**

```csv
detection_id,media_url,channel_id,deepfake_score,sentiment_score,risk_quantification,status,verified,blockchain_hash,timestamp
a21a7a23...,https://youtube.com/...,YouTube,0.49,-0.32,Low,Auto-Processed,False,,2025-10-11T16:05:23
e45c959d...,https://twitter.com/...,Twitter,0.85,-0.61,High,Awaiting Expert Review,False,0xb7409...,2025-10-11T16:05:23
```

**Create Pivot Tables:**
- Group by platform
- Average deepfake scores
- Risk level distribution
- Blockchain entry count

---

### **Method 3: API Analysis**

**Get Statistics:**
```bash
curl http://localhost:5000/api/v1/stats | python3 -m json.tool
```

**Get All High-Risk:**
```bash
curl "http://localhost:5000/api/v1/incidents?risk=High" | python3 -m json.tool
```

**Get Blockchain Audit:**
```bash
curl http://localhost:5000/api/v1/blockchain/audit | python3 -m json.tool
```

---

## 6. 📈 Export & Reporting

### **Export All Data:**

**Via Web Interface:**
1. Scan Media → Export Results
2. Click "Export All Incidents to CSV"
3. Opens in Excel/Sheets

**Via API:**
```bash
curl -o my_results.csv http://localhost:5000/api/v1/batch/export
```

### **Create Reports:**

**Example Python Script:**

```python
import csv
import json

# Read exported CSV
incidents = []
with open('deepfake_incidents_2025-10-11.csv', 'r') as f:
    reader = csv.DictReader(f)
    incidents = list(reader)

# Calculate statistics
total = len(incidents)
high_risk = len([i for i in incidents if i['risk_quantification'] == 'High'])
verified = len([i for i in incidents if i['verified'] == 'True'])

print(f"📊 ANALYSIS REPORT")
print(f"================")
print(f"Total Detections: {total}")
print(f"High-Risk: {high_risk} ({high_risk/total*100:.1f}%)")
print(f"Verified: {verified}")
print(f"\nPlatform Breakdown:")

# Group by platform
from collections import Counter
platforms = Counter([i['channel_id'] for i in incidents])
for platform, count in platforms.most_common():
    print(f"  {platform}: {count}")
```

---

## 🎬 **Complete Testing Walkthrough:**

### **Scenario: Test 10 Suspicious Videos**

**1. Create Dataset:**
```bash
cat > test_videos.csv << 'EOF'
media_url,channel_id,description
https://youtube.com/suspicious1,YouTube,Fake news video
https://twitter.com/scam1,Twitter,Celebrity scam
https://facebook.com/fake1,Facebook,Misleading ad
https://instagram.com/fraud1,Instagram,Product fraud
https://tiktok.com/fake1,TikTok,Deepfake dance
https://youtube.com/misinf1,YouTube,Health misinfo
https://twitter.com/fake2,Twitter,Political fake
https://linkedin.com/scam1,LinkedIn,Job scam
https://reddit.com/fake1,Reddit,Fake footage
https://vimeo.com/deep1,Vimeo,Synthetic video
EOF
```

**2. Upload & Process:**
```bash
curl -X POST http://localhost:5000/api/v1/batch/upload \
  -F "file=@test_videos.csv" \
  | python3 -m json.tool > batch_results.json
```

**3. View Summary:**
```bash
cat batch_results.json | jq '{
  total: .total_processed,
  high_risk: .high_risk_detected,
  message: .message
}'
```

**Output:**
```json
{
  "total": 10,
  "high_risk": 2,
  "message": "Batch processing completed"
}
```

**4. Check Dashboard:**
- Open: http://localhost:5000
- Click: "Dashboard"
- See: 10 new detections
- View: 2 high-risk incidents in table

**5. Review Threats:**
- Click: "Expert Review"
- See: 2 incidents awaiting review
- Click: Each incident card
- Review: Forensic analysis
- Action: "Verify Harmful / Log to Blockchain"

**6. Verify Blockchain:**
- Click: "Audit Trail"
- See: 2 blockchain entries (for high-risk items)
- Search: By detection ID
- Confirm: Transaction hashes present

**7. Export Results:**
- Click: "Scan Media"
- Scroll to: "Export Results"
- Click: "Export All Incidents to CSV"
- Download: `deepfake_incidents_2025-10-11.csv`
- Open in: Excel/Google Sheets for analysis

---

## 📊 **Sample Test Results:**

### **Batch Upload: test_dataset.csv**

**Input:** 10 URLs from various platforms

**Processing Time:** ~1 second

**Output:**
```
Total Processed: 10
High-Risk Detected: 1
Medium-Risk: 4
Low-Risk: 5

Blockchain Entries Created: 1
Expert Review Queue: 1 item
Auto-Processed: 9 items
```

**Individual Results:**

| # | Platform | URL | Deepfake | Risk | Blockchain |
|---|----------|-----|----------|------|------------|
| 1 | YouTube | youtube.com/... | 49% | Low | No |
| 2 | Twitter | twitter.com/... | **85%** | **High** | **Yes** ✓ |
| 3 | Facebook | facebook.com/... | 40% | Medium | No |
| 4 | Instagram | instagram.com/... | 11% | Low | No |
| 5 | TikTok | tiktok.com/... | 81% | Medium | No |
| 6 | News | example.com/... | 67% | Medium | No |
| 7 | LinkedIn | linkedin.com/... | 11% | Low | No |
| 8 | Vimeo | vimeo.com/... | 84% | Medium | No |
| 9 | Reddit | reddit.com/... | 27% | Low | No |
| 10 | Ad Network | example.com/... | 31% | Low | No |

---

## 🎯 **Testing Scenarios:**

### **Scenario 1: Conference Demo**

**Goal:** Quickly show the system working

**Steps:**
1. Click "Generate Demo Data" (creates 8 incidents)
2. Upload `test_dataset.csv` (adds 10 more)
3. Click "Dashboard" (shows 18 total)
4. Click "Expert Review" (shows high-risk queue)
5. Verify one incident (logs to blockchain)
6. Click "Audit Trail" (shows blockchain proof)
7. Export to CSV (download results)

**Time:** 2-3 minutes  
**Impact:** Complete demonstration

---

### **Scenario 2: Research Testing**

**Goal:** Test deepfake detection patterns

**Dataset:** 100 URLs across different platforms

**Steps:**
1. Create CSV with 100 test URLs
2. Upload via batch
3. Export results
4. Analyze in Python/Excel:
   - Average deepfake score per platform
   - Risk distribution
   - Sentiment patterns

---

### **Scenario 3: Stress Testing**

**Goal:** Test system performance

**Dataset:** 1000 URLs

**Steps:**
1. Generate large CSV (1000 rows)
2. Upload batch
3. Monitor processing time
4. Check memory usage
5. Verify all entries in database
6. Test dashboard performance

---

## 📁 **Test Data Repository:**

### **Included Test Files:**

**1. test_dataset.csv**
- 10 sample URLs
- Various platforms
- Different content types
- Location: `/home/p/dp/IBMZ/test_dataset.csv`

**2. Sample Uploaded Files:**
- Located in: `/home/p/dp/IBMZ/uploads/`
- Screenshots and images
- Used for file upload testing

---

## 🔍 **Verification Checklist:**

### **After Testing, Verify:**

- [ ] ✅ Files uploaded successfully
- [ ] ✅ URLs scanned without errors
- [ ] ✅ CSV batch processed all rows
- [ ] ✅ Dashboard shows correct totals
- [ ] ✅ High-risk items in review queue
- [ ] ✅ Blockchain entries created
- [ ] ✅ Export CSV works
- [ ] ✅ Search functionality works
- [ ] ✅ Modal details display correctly
- [ ] ✅ Verification creates 2nd blockchain entry

---

## 📈 **Performance Benchmarks:**

### **Expected Processing Times:**

| Test Size | Method | Time | Blockchain Entries |
|-----------|--------|------|-------------------|
| 1 file | Upload | < 1s | 0-1 |
| 1 URL | Scan | < 1s | 0-1 |
| 10 URLs | CSV Batch | ~1s | 1-3 |
| 50 URLs | CSV Batch | ~3s | 5-15 |
| 100 URLs | CSV Batch | ~5s | 10-30 |
| 1000 URLs | CSV Batch | ~30s | 100-300 |

**High-Risk Rate:** ~10-30% (random simulation)

---

## 🚀 **Quick Start Testing:**

### **5-Minute Test Sequence:**

```bash
# 1. Test single file
echo "test" > test.jpg
curl -X POST http://localhost:5000/api/v1/upload \
  -F "file=@test.jpg" \
  -F "channel_id=Test"

# 2. Test URL scan
curl -X POST http://localhost:5000/api/v1/scan \
  -H "Content-Type: application/json" \
  -d '{"media_url":"https://youtube.com/test"}'

# 3. Test CSV batch
curl -X POST http://localhost:5000/api/v1/batch/upload \
  -F "file=@test_dataset.csv"

# 4. Get statistics
curl http://localhost:5000/api/v1/stats

# 5. Get blockchain audit
curl http://localhost:5000/api/v1/blockchain/audit

# 6. Export results
curl -o results.csv http://localhost:5000/api/v1/batch/export
```

---

## 💡 **Pro Tips:**

### **1. Realistic Testing:**
- Use actual URLs (they won't be downloaded, just stored)
- Mix different platforms
- Vary content types
- Include edge cases

### **2. Data Preparation:**
- UTF-8 encoding for CSV
- No special characters in URLs
- Valid URL format
- Clear descriptions

### **3. Result Analysis:**
- Export after each test
- Compare results
- Track patterns
- Document findings

### **4. Demo Preparation:**
- Pre-load dataset CSV
- Test upload workflow
- Verify results display
- Practice walkthrough

---

## 🎉 **Summary:**

### **Your Platform Now Supports:**

✅ **3 Testing Methods:**
   - Single file upload
   - URL scanning
   - CSV batch processing

✅ **Multiple Data Sources:**
   - Local files (images, videos, audio)
   - Online URLs (any platform)
   - CSV datasets (bulk testing)

✅ **Complete Workflow:**
   - Upload → Analyze → Store → Blockchain → Review → Export

✅ **Export Capabilities:**
   - Download results as CSV
   - Ready for Excel/Python analysis
   - Generate reports

---

## 🚀 **Try It Now!**

1. **Refresh Chrome:** http://localhost:5000 (Ctrl + Shift + R)
2. **Go to:** "Scan Media" tab
3. **Scroll to:** "Batch Testing with CSV"
4. **Click:** "Download Sample CSV"
5. **Upload:** The CSV file
6. **Click:** "Process Batch"
7. **Watch:** 10 items analyzed instantly!

---

**🎯 Your platform is now ready for comprehensive testing with CSV datasets!**

Perfect for demonstrations, research, and the IBM Z Datathon 2025 presentation!

