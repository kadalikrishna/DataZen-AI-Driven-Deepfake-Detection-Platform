"""Download and validate models before running offline."""
import struct,sys
from backend.detector import AUDIO_MODEL_ID,VISUAL_MODEL_ID,DeepfakeDetector
if __name__=="__main__":
    if struct.calcsize("P")*8!=64: raise SystemExit("DataZen requires 64-bit Python.")
    engine=DeepfakeDetector()
    print("Loading",VISUAL_MODEL_ID); engine._bundle()
    print("Loading",AUDIO_MODEL_ID); engine._bundle(True)
    print("Models are downloaded and ready for offline inference.")
