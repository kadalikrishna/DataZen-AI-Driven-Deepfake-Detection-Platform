'''Canonical Flask application for DataZen.'''
import os,tempfile,time,uuid
from collections import deque
from datetime import datetime,timezone
from pathlib import Path
from flask import Flask,jsonify,render_template,request
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
try: from .detector import DeepfakeDetector,DetectionError
except ImportError: from detector import DeepfakeDetector,DetectionError

ROOT=Path(__file__).resolve().parent.parent
app=Flask(__name__,template_folder=str(ROOT/'templates'),static_folder=str(ROOT/'static')); CORS(app)
app.config['MAX_CONTENT_LENGTH']=20*1024*1024
detector=DeepfakeDetector(); history=deque(maxlen=100)
FORMATS={'image':{'jpg','jpeg','png','webp'},'video':{'mp4','mov','avi','webm'}}

def media_type(filename):
    ext=filename.rsplit('.',1)[-1].lower() if '.' in filename else ''
    return next((kind for kind,exts in FORMATS.items() if ext in exts),None)

@app.get('/')
def index(): return render_template('index.html')

@app.get('/api/v1/health')
def health(): return jsonify({'status':'ok','service':'DataZen'})

@app.get('/api/v1/model/status')
def model_status():
    return jsonify({**detector.status(),'supported_formats':{k:sorted(v) for k,v in FORMATS.items()},
      'max_upload_mb':20,'max_video_seconds':30,'max_video_frames':4})

@app.post('/api/v1/upload')
def upload():
    item=request.files.get('file')
    if item is None: return jsonify({'error':'No file was provided.'}),400
    if not item.filename: return jsonify({'error':'Select a file before analyzing.'}),400
    name=secure_filename(item.filename); kind=media_type(name)
    if kind is None:
        supported=', '.join(sorted({ext for values in FORMATS.values() for ext in values}))
        return jsonify({'error':f'Unsupported format. Use: {supported}.'}),415
    temp_path=None; started=time.perf_counter()
    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=Path(name).suffix.lower()) as temp:
            item.save(temp); temp_path=Path(temp.name)
        result=detector.analyze(temp_path,kind)
        result.update({'detection_id':f'dz_{uuid.uuid4().hex[:12]}','filename':name,'file_size':temp_path.stat().st_size,
          'timestamp':datetime.now(timezone.utc).isoformat(),'total_request_time_ms':round((time.perf_counter()-started)*1000)})
        history.appendleft(result); return jsonify(result)
    except DetectionError as exc: return jsonify({'error':str(exc)}),422
    finally:
        if temp_path: temp_path.unlink(missing_ok=True)

@app.get('/api/v1/incidents')
def incidents(): return jsonify(list(history))

@app.get('/api/v1/stats')
def stats():
    items=list(history)
    return jsonify({'total_analyses':len(items),'likely_fake':sum(x['verdict']=='likely_fake' for x in items),
      'inconclusive':sum(x['verdict']=='inconclusive' for x in items),'likely_real':sum(x['verdict']=='likely_real' for x in items)})

@app.post('/api/v1/clear')
def clear(): history.clear(); return jsonify({'message':'Analysis history cleared.'})

@app.errorhandler(RequestEntityTooLarge)
def too_large(_): return jsonify({'error':'File is larger than the 20 MB limit.'}),413

application=app
if __name__=='__main__': app.run(host='0.0.0.0',port=int(os.getenv('PORT','5000')),debug=False)
