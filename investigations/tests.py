from django.contrib.auth.models import User
from django.test import SimpleTestCase,TestCase
from django.urls import reverse
from .analyzers import text_analysis,correlate
class AnalyzerTests(SimpleTestCase):
 def test_reference_overlap(self):
  result=text_analysis('the quick brown fox','the quick brown fox')
  self.assertEqual(result['metrics']['reference_token_jaccard'],1.0)
 def test_no_fabricated_risk_score(self):
  result=correlate([])
  self.assertIsNone(result['risk_score'])
  self.assertIn('Inconclusive',result['verdict'])

class AdvancedImageTests(SimpleTestCase):
 def test_optional_model_off_by_default(self):
  from unittest.mock import patch
  from .analyzers import optional_image_model
  with patch.dict('os.environ',{},clear=True):
   self.assertIsNone(optional_image_model('not-an-image.jpg'))
 def test_image_visualization(self):
  import tempfile
  from pathlib import Path
  from django.test import override_settings
  from PIL import Image
  from .analyzers import image_analysis
  with tempfile.TemporaryDirectory() as temp:
   src=Path(temp)/'test.jpg'
   Image.new('RGB',(300,200),(80,100,120)).save(src)
   with override_settings(MEDIA_ROOT=temp,MEDIA_URL='/media/'):
    result=image_analysis(src)
   self.assertNotIn('error',result)
   self.assertEqual(len(result.get('visualizations',[])),1)
   self.assertTrue(list((Path(temp)/'derived').glob('*.png')))

class VisualEvidenceTests(SimpleTestCase):
 def test_audio_waveform(self):
  import tempfile,wave,struct,math
  from pathlib import Path
  from django.test import override_settings
  from .analyzers import audio_analysis
  with tempfile.TemporaryDirectory() as folder:
   source=Path(folder)/'tone.wav'
   with wave.open(str(source),'wb') as wf:
    wf.setnchannels(1);wf.setsampwidth(2);wf.setframerate(16000)
    wf.writeframes(b''.join(struct.pack('<h',int(9000*math.sin(2*math.pi*440*i/16000))) for i in range(16000)))
   with override_settings(MEDIA_ROOT=folder,MEDIA_URL='/media/'):
    result=audio_analysis(source)
   if 'error' in result and 'not installed' in result['error']:
    self.skipTest('Audio optional dependencies not installed')
   self.assertNotIn('error',result)
   self.assertTrue(result.get('visualizations'))

 def test_video_frames(self):
  import tempfile
  from pathlib import Path
  from django.test import override_settings
  from .analyzers import video_analysis
  try:
   import cv2,numpy as np
  except ImportError:
   self.skipTest('OpenCV unavailable')
  with tempfile.TemporaryDirectory() as folder:
   source=Path(folder)/'sample.avi'
   writer=cv2.VideoWriter(str(source),cv2.VideoWriter_fourcc(*'MJPG'),10,(160,90))
   if not writer.isOpened():self.skipTest('Video writer codec unavailable')
   for i in range(12):writer.write(np.full((90,160,3),i*10,dtype=np.uint8))
   writer.release()
   with override_settings(MEDIA_ROOT=folder,MEDIA_URL='/media/'):
    result=video_analysis(source)
   self.assertNotIn('error',result)
   self.assertTrue(result.get('visualizations'))

class ModelInferenceTests(SimpleTestCase):
 def test_image_classifier_with_mock(self):
  import tempfile
  from pathlib import Path
  from PIL import Image
  from unittest.mock import patch
  from .analyzers import optional_image_model
  with tempfile.TemporaryDirectory() as folder:
   source=Path(folder)/'test.png'
   Image.new('RGB',(64,64),'red').save(source)
   with patch.dict('os.environ',{'TRUTHLENS_IMAGE_MODEL':'trusted/local-model'}):
    with patch('investigations.analyzers._load_classifier',return_value=lambda *a,**k:[{'label':'fake','score':0.8},{'label':'real','score':0.2}]):
     result=optional_image_model(source)
   self.assertEqual(result['labels'][0]['label'],'fake')
   self.assertIn('Experimental',result['warning'])


class AIReanalysisTests(SimpleTestCase):
 def test_rerun_requires_post(self):
  from django.urls import reverse
  import uuid
  response=self.client.get(reverse('rerun_ai',args=[uuid.uuid4()]))
  self.assertEqual(response.status_code,405)

class AnalystProfileTests(TestCase):
 def test_authenticated_analyst_sees_own_profile(self):
  user=User.objects.create_user(username='analyst01',email='analyst@example.com')
  self.client.force_login(user)

  response=self.client.get(reverse('profile'))

  self.assertEqual(response.status_code,200)
  self.assertContains(response,'analyst01')
  self.assertContains(response,'analyst@example.com')

 def test_guest_profile_offers_sign_in_and_registration(self):
  response=self.client.get(reverse('profile'))

  self.assertEqual(response.status_code,200)
  self.assertContains(response,'Sign in to view your account details.')
  self.assertContains(response,reverse('login'))
  self.assertContains(response,reverse('register'))
