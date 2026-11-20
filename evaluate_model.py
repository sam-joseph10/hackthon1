"""Evaluate a configured binary real/fake image model on held-out labeled files.
Usage: python evaluate_model.py labels.csv --fake-label fake
CSV: path,truth (truth values: real or fake). No files are uploaded.
"""
import argparse,csv,json,os,sys
from pathlib import Path
from PIL import Image
from investigations.analyzers import _load_classifier

def evaluate(manifest,fake_label):
 model=os.getenv('TRUTHLENS_IMAGE_MODEL','').strip()
 if not model:raise ValueError('Set TRUTHLENS_IMAGE_MODEL to a trusted real/fake image classifier.')
 classifier=_load_classifier(model)
 rows=list(csv.DictReader(open(manifest,encoding='utf-8-sig',newline='')))
 if not rows:raise ValueError('Empty manifest')
 counts={'TP':0,'TN':0,'FP':0,'FN':0};errors=[]
 for row in rows:
  path=(Path(manifest).resolve().parent / row['path']).resolve()
  truth=row['truth'].strip().lower()
  if truth not in ('real','fake'):raise ValueError(f'Invalid truth label: {truth}')
  try:
   with Image.open(path) as image:
    results=classifier(image.convert('RGB'),top_k=20)
   if not any(v['label'].lower()==fake_label.lower() for v in results):
    raise ValueError(f'Configured fake label {fake_label!r} missing from model output')
   predicted='fake' if max(results,key=lambda v:v['score'])['label'].lower()==fake_label.lower() else 'real'
   counts[('T' if truth==predicted else 'F')+('P' if predicted=='fake' else 'N')]+=1
  except Exception as exc:errors.append({'path':str(path),'error':str(exc)})
 tp,tn,fp,fn=(counts[k] for k in ('TP','TN','FP','FN'))
 def div(a,b):return round(a/b,4) if b else None
 return {'model':model,'fake_label':fake_label,'evaluated':sum(counts.values()),'errors':errors,'confusion_matrix':counts,'precision_fake':div(tp,tp+fp),'recall_fake':div(tp,tp+fn),'specificity_real':div(tn,tn+fp),'accuracy':div(tp+tn,tp+tn+fp+fn),'warning':'Only reflects the supplied evaluation set. Check dataset provenance, class balance and domain shift.'}

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('manifest');parser.add_argument('--fake-label',required=True)
 args=parser.parse_args()
 try:print(json.dumps(evaluate(args.manifest,args.fake_label),indent=2))
 except Exception as exc:print(f'Evaluation failed: {exc}',file=sys.stderr);sys.exit(1)
