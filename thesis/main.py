from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
import cv2
import mediapipe as mp
from os import path


# Window.size = (dp(720), dp(1600))
Window.maximize()
PATH = path.abspath('.')+'/'


class MyMainApp(MDApp):
  def build(self):
    scrollview = MDScrollView()
    
    layout = MDBoxLayout(
      orientation = 'vertical',
      md_bg_color = (0, 0, 0, 1)
      )
    scrollview.add_widget(layout)

    self.image = Image()
    layout.add_widget(self.image)

    self.label_lbl = MDLabel(
      text = 'Label',
      halign = 'center',
      size_hint = ( .5, .25 ),
      pos_hint = { 'center_x': .5 },
      theme_text_color = 'Custom',
      text_color = (0, 0, 1, 1)
    )
    layout.add_widget(self.label_lbl)

    self.capture = 'Play'
    self.start_btn = MDRaisedButton(
      text = self.capture,
      size_hint = ( .5, None ),
      pos_hint = { 'center_x': .5 },
      on_release = self.on_press_btn
    )
    layout.add_widget(self.start_btn)

    self.cap = cv2.VideoCapture(0)
    Clock.schedule_interval(self.load_video, 1.0/5.0)
    return scrollview


  def on_press_btn(self, *args):
    if self.capture == 'Play':
      self.capture = 'Stop'
    else:
      self.capture = 'Play'
    self.start_btn.text = self.capture


  def load_video(self, *args):
    if self.capture == 'Stop':
      self.frame = self.get_keypoints()
    else:
      self.frame = cv2.imread(PATH+'stop.jpg')
    buffer = cv2.flip(self.frame, 0).tostring()
    texture = Texture.create(
      size = ( self.frame.shape[1], self.frame.shape[0] ),
      colorfmt = 'bgr'
    )
    texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
    self.image.texture = texture


  def get_keypoints(self):
    success, frame = self.cap.read()
    mp_drawing = mp.solutions.drawing_utils
    mp_holistic = mp.solutions.holistic
    with mp_holistic.Holistic(
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5
      ) as holistic:
      image_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      results = holistic.process(image_RGB)
      image = cv2.cvtColor(image_RGB, cv2.COLOR_RGB2BGR)
      mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    return image


MyMainApp().run()