'''Low-memory ONNX screening for images and sampled video frames.'''
import json, math, os, subprocess, tempfile, threading, time
from pathlib import Path
import numpy as np
from PIL import Image, UnidentifiedImageError

VISUAL_MODEL_ID=os.getenv('DATAZEN_VISUAL_MODEL','dima806/deepfake_vs_real_image_detection')
MODEL_PATH=Path(os.getenv('DATAZEN_MODEL_PATH',Path(__file__).resolve().parent.parent/'models'/'model_int8.onnx'))
MODEL_CONFIG_PATH=Path(os.getenv('DATAZEN_MODEL_CONFIG',MODEL_PATH.with_name('model_config.json')))
MAX_IMAGE_PIXELS=25_000_000
MAX_VIDEO_SECONDS=30.0
MAX_VIDEO_FRAMES=4

class DetectionError(RuntimeError): pass

class DeepfakeDetector:
    def __init__(self):
        self._session=self._config=None
        self._lock=threading.Lock()

    def _bundle(self):
        if self._session is None:
            with self._lock:
                if self._session is None:
                    try:
                        import onnxruntime as ort
                        if not MODEL_PATH.is_file() or not MODEL_CONFIG_PATH.is_file():
                            raise FileNotFoundError('Optimized model files are missing.')
                        options=ort.SessionOptions()
                        options.intra_op_num_threads=options.inter_op_num_threads=1
                        options.enable_mem_pattern=False
                        self._session=ort.InferenceSession(str(MODEL_PATH),sess_options=options,providers=['CPUExecutionProvider'])
                        self._config=json.loads(MODEL_CONFIG_PATH.read_text(encoding='utf-8'))
                    except Exception as exc:
                        self._session=None
                        raise DetectionError('The optimized detection model could not be loaded.') from exc
        return self._session,self._config

    @staticmethod
    def _open_image(path):
        try:
            with Image.open(path) as source:
                width,height=source.size
                if width*height>MAX_IMAGE_PIXELS:
                    raise DetectionError('Image dimensions are too large. Use an image under 25 megapixels.')
                return source.convert('RGB')
        except DetectionError: raise
        except (UnidentifiedImageError,OSError,Image.DecompressionBombError) as exc:
            raise DetectionError('Image is corrupt or unreadable.') from exc

    def _score_image(self,image):
        session,config=self._bundle()
        height,width=config.get('size',[224,224])
        values=np.asarray(image.resize((int(width),int(height)),Image.Resampling.BILINEAR),dtype=np.float32)/255.0
        mean=np.asarray(config.get('image_mean',[0.5]*3),dtype=np.float32)
        std=np.asarray(config.get('image_std',[0.5]*3),dtype=np.float32)
        values=((values-mean)/std).transpose(2,0,1)[None,...]
        logits=session.run([session.get_outputs()[0].name],{session.get_inputs()[0].name:values})[0][0].astype(np.float64)
        probabilities=np.exp(logits-logits.max()); probabilities/=probabilities.sum()
        return float(probabilities[config['fake_indices']].sum())

    @staticmethod
    def _result(kind,score,started,evidence):
        verdict,label=('likely_fake','Likely synthetic or manipulated') if score>.65 else (('likely_real','Likely authentic') if score<.35 else ('inconclusive','Inconclusive - review recommended'))
        return {'media_type':kind,'verdict':verdict,'verdict_label':label,'fake_probability':round(score,4),
          'real_probability':round(1-score,4),'model':f'{VISUAL_MODEL_ID} (INT8 ONNX)',
          'processing_time_ms':round((time.perf_counter()-started)*1000),'evidence':evidence,
          'limitations':'Research screening result, not proof. Video results use sampled frames and may miss manipulations between samples.'}

    def analyze_image(self,path):
        started=time.perf_counter(); score=self._score_image(self._open_image(path))
        return self._result('image',score,started,[{'sample':1,'fake_probability':round(score,4)}])

    @staticmethod
    def _video_duration(path):
        try:
            completed=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(path)],
              capture_output=True,text=True,timeout=20,check=True)
            duration=float(json.loads(completed.stdout)['format']['duration'])
            if not math.isfinite(duration) or duration<=0: raise ValueError
            return duration
        except (subprocess.SubprocessError,OSError,ValueError,KeyError,json.JSONDecodeError) as exc:
            raise DetectionError('Video is corrupt or unsupported.') from exc

    @staticmethod
    def _extract_frame(video_path,timestamp,output_path):
        try:
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-ss',f'{timestamp:.3f}','-i',str(video_path),
              '-frames:v','1','-an','-y',str(output_path)],capture_output=True,timeout=45,check=True)
        except (subprocess.SubprocessError,OSError) as exc:
            raise DetectionError('A video frame could not be decoded.') from exc

    def analyze_video(self,path):
        started=time.perf_counter(); duration=self._video_duration(path)
        if duration>MAX_VIDEO_SECONDS: raise DetectionError('Videos must be 30 seconds or shorter.')
        count=min(MAX_VIDEO_FRAMES,max(1,math.ceil(duration/5)))
        timestamps=[duration*(index+1)/(count+1) for index in range(count)]
        evidence=[]
        with tempfile.TemporaryDirectory(prefix='datazen_frames_') as directory:
            for index,timestamp in enumerate(timestamps,start=1):
                frame=Path(directory)/f'frame_{index}.jpg'; self._extract_frame(path,timestamp,frame)
                score=self._score_image(self._open_image(frame))
                evidence.append({'sample':index,'timestamp_seconds':round(timestamp,2),'fake_probability':round(score,4)})
        score=sum(item['fake_probability'] for item in evidence)/len(evidence)
        result=self._result('video',score,started,evidence)
        result.update({'frames_analyzed':len(evidence),'duration_seconds':round(duration,2)}); return result

    def analyze(self,path,media_type):
        methods={'image':self.analyze_image,'video':self.analyze_video}
        if media_type not in methods: raise DetectionError('Unsupported media type.')
        return methods[media_type](Path(path))

    def status(self):
        return {'engine':'quantized_onnx','device':'cpu','visual_model':VISUAL_MODEL_ID,'visual_loaded':self._session is not None}
