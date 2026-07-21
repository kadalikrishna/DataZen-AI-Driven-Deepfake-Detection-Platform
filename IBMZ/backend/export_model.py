'''Export and dynamically quantize the visual classifier.'''
import argparse, json
from pathlib import Path
import torch
from onnxruntime.quantization import QuantType,quantize_dynamic
from transformers import AutoImageProcessor,AutoModelForImageClassification

class LogitsOnly(torch.nn.Module):
    def __init__(self,model):
        super().__init__(); self.model=model
    def forward(self,pixel_values):
        return self.model(pixel_values=pixel_values).logits

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',default='dima806/deepfake_vs_real_image_detection')
    parser.add_argument('--output',default='models')
    args=parser.parse_args(); output=Path(args.output); output.mkdir(parents=True,exist_ok=True)
    processor=AutoImageProcessor.from_pretrained(args.model)
    model=AutoModelForImageClassification.from_pretrained(args.model,use_safetensors=True).eval()
    size=processor.size
    height=int(size.get('height',size.get('shortest_edge',224)))
    width=int(size.get('width',size.get('shortest_edge',224)))
    source=output/'model.onnx'; target=output/'model_int8.onnx'
    torch.onnx.export(LogitsOnly(model),torch.zeros(1,3,height,width),source,input_names=['pixel_values'],
      output_names=['logits'],opset_version=17,do_constant_folding=True)
    quantize_dynamic(source,target,weight_type=QuantType.QInt8)
    labels={int(key):str(value) for key,value in model.config.id2label.items()}
    terms=('fake','spoof','synthetic','generated','deepfake','ai')
    fake_indices=[key for key,label in labels.items() if any(term in label.lower() for term in terms)]
    if not fake_indices and len(labels)==2: fake_indices=[1]
    if not fake_indices: raise RuntimeError('Model has no fake/spoof label.')
    (output/'model_config.json').write_text(json.dumps({'model_id':args.model,'size':[height,width],
      'image_mean':processor.image_mean,'image_std':processor.image_std,'id2label':labels,
      'fake_indices':fake_indices}),encoding='utf-8')
    source.unlink()

if __name__=='__main__': main()
