"""Local pretrained deepfake detection for visual and speech media."""
import os, threading, time
from pathlib import Path

VISUAL_MODEL_ID=os.getenv("DATAZEN_VISUAL_MODEL","dima806/deepfake_vs_real_image_detection")
AUDIO_MODEL_ID=os.getenv("DATAZEN_AUDIO_MODEL","Vansh180/deepfake-audio-wav2vec2")

class DetectionError(RuntimeError): pass

class DeepfakeDetector:
    def __init__(self):
        self._visual=self._audio=None
        self._vlock,self._alock=threading.Lock(),threading.Lock()

    def _load(self, model_id, audio=False):
        try:
            import torch
            from transformers import AutoImageProcessor,AutoFeatureExtractor
            from transformers import AutoModelForImageClassification,AutoModelForAudioClassification
            if audio:
                processor=AutoFeatureExtractor.from_pretrained(model_id)
                model=AutoModelForAudioClassification.from_pretrained(model_id,use_safetensors=True)
            else:
                processor=AutoImageProcessor.from_pretrained(model_id)
                model=AutoModelForImageClassification.from_pretrained(model_id,use_safetensors=True)
            model.to("cpu").eval(); return processor,model,torch
        except Exception as exc:
            raise DetectionError(f"Could not load {model_id}. Run setup_models.py while online.") from exc

    def _bundle(self,audio=False):
        attr,lock,mid=("_audio",self._alock,AUDIO_MODEL_ID) if audio else ("_visual",self._vlock,VISUAL_MODEL_ID)
        if getattr(self,attr) is None:
            with lock:
                if getattr(self,attr) is None: setattr(self,attr,self._load(mid,audio))
        return getattr(self,attr)

    def _scores(self,bundle,inputs):
        _,model,torch=bundle
        with torch.inference_mode(): probs=torch.softmax(model(**inputs).logits,dim=-1)
        terms=("fake","spoof","synthetic","generated","deepfake","ai")
        indices=[int(i) for i,label in model.config.id2label.items() if any(t in str(label).lower() for t in terms)]
        if not indices and len(model.config.id2label)==2: indices=[1]
        if not indices: raise DetectionError("Model has no fake/spoof label.")
        return [float(row[indices].sum().item()) for row in probs]

    def _result(self,kind,score,model,started,evidence):
        verdict,label=("likely_fake","Likely synthetic or manipulated") if score>.65 else (("likely_real","Likely authentic") if score<.35 else ("inconclusive","Inconclusive — review recommended"))
        return {"media_type":kind,"verdict":verdict,"verdict_label":label,"fake_probability":round(score,4),
          "real_probability":round(1-score,4),"model":model,"processing_time_ms":round((time.perf_counter()-started)*1000),
          "evidence":evidence,"limitations":"Research screening result, not proof. Accuracy can drop for unseen generators, compression, noise, crops, or non-speech audio."}

    def analyze_image(self,path):
        from PIL import Image,UnidentifiedImageError
        started=time.perf_counter()
        try:
            with Image.open(path) as source: image=source.convert("RGB")
        except (UnidentifiedImageError,OSError) as exc: raise DetectionError("Image is corrupt or unreadable.") from exc
        bundle=self._bundle(); score=self._scores(bundle,bundle[0](images=[image],return_tensors="pt"))[0]
        return self._result("image",score,VISUAL_MODEL_ID,started,[{"sample":1,"fake_probability":round(score,4)}])

    def analyze_video(self,path,max_frames=12):
        import cv2
        from PIL import Image
        started=time.perf_counter(); cap=cv2.VideoCapture(str(path))
        if not cap.isOpened(): raise DetectionError("Video is corrupt or unsupported.")
        try:
            total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); fps=float(cap.get(cv2.CAP_PROP_FPS) or 0)
            if total<=0 or fps<=0: raise DetectionError("Video frames could not be read.")
            duration=total/fps
            if duration>120: raise DetectionError("Videos must be 120 seconds or shorter.")
            count=min(max_frames,total)
            positions=[0] if count==1 else [round(i*(total-1)/(count-1)) for i in range(count)]
            frames,times=[],[]
            for pos in positions:
                cap.set(cv2.CAP_PROP_POS_FRAMES,pos); ok,frame=cap.read()
                if ok:
                    frames.append(Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))); times.append(pos/fps)
        finally: cap.release()
        if not frames: raise DetectionError("No readable video frames were found.")
        bundle=self._bundle(); scores=self._scores(bundle,bundle[0](images=frames,return_tensors="pt"))
        evidence=[{"sample":i+1,"timestamp_seconds":round(t,2),"fake_probability":round(s,4)} for i,(t,s) in enumerate(zip(times,scores))]
        result=self._result("video",sum(scores)/len(scores),VISUAL_MODEL_ID,started,evidence)
        result.update({"frames_analyzed":len(frames),"duration_seconds":round(duration,2)}); return result

    def analyze_audio(self,path,max_windows=8):
        import librosa,numpy as np
        started=time.perf_counter()
        try: waveform,sr=librosa.load(path,sr=16000,mono=True)
        except Exception as exc: raise DetectionError("Audio is corrupt or unsupported.") from exc
        if waveform.size<1600: raise DetectionError("Audio must contain at least 0.1 seconds of sound.")
        duration=waveform.size/sr
        if duration>300: raise DetectionError("Audio must be 5 minutes or shorter.")
        size=sr*4
        starts=[0] if waveform.size<=size else np.linspace(0,waveform.size-size,min(max_windows,max(2,int(duration//4))),dtype=int).tolist()
        windows=[]
        for start in starts:
            window=waveform[start:start+size]
            if window.size<size: window=np.pad(window,(0,size-window.size))
            windows.append(window.astype("float32"))
        bundle=self._bundle(True); inputs=bundle[0](windows,sampling_rate=sr,return_tensors="pt",padding=True)
        scores=self._scores(bundle,inputs)
        evidence=[{"sample":i+1,"timestamp_seconds":round(start/sr,2),"fake_probability":round(score,4)} for i,(start,score) in enumerate(zip(starts,scores))]
        result=self._result("audio",sum(scores)/len(scores),AUDIO_MODEL_ID,started,evidence)
        result.update({"segments_analyzed":len(windows),"duration_seconds":round(duration,2)}); return result

    def analyze(self,path,media_type):
        try: method={"image":self.analyze_image,"video":self.analyze_video,"audio":self.analyze_audio}[media_type]
        except KeyError as exc: raise DetectionError("Unsupported media type.") from exc
        return method(Path(path))

    def status(self):
        return {"engine":"local_pretrained_models","device":"cpu","visual_model":VISUAL_MODEL_ID,
          "visual_loaded":self._visual is not None,"audio_model":AUDIO_MODEL_ID,"audio_loaded":self._audio is not None}
