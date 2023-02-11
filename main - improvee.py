from kivy.app import App
from kivy.lang.builder import Builder
from googletrans import Translator
import speech_recognition as sr
import os
from gtts import gTTS
from playsound import playsound


r = sr.Recognizer()
mic = sr.Microphone()
tr = Translator()

KV = """
<MyLabel@label>:
    size_hint : [None,None]
    size : self.texture_size

<MyTextField@TextInput>:
    size_hint : [0.3 , 0.4]
    font_size : '30sp'

<LangButton@Button>
    background_normal : ''
    background_color : [1,1,1,1]
    color : [0,0,0,1]
    bold : True
    font_size : '14sp'
    size_hint : [None,None]
    height : 50
    width : 100
    
FloatLayout:
    canvas.before:
        Color:
            rgba : rgba('#1877F2')
        Rectangle:
            pos : self.pos
            size: self.size

    Label:
        text: "Translated text"
        pos_hint: {'center_x':0.2,'center_y':0.7}
        font_size: '20sp'
        color : [0,0,0,1]
        bold: True
    
        
    Label:
        text: "Original text"
        pos_hint: {'center_x':0.8,'center_y':0.7}
        font_size: '20sp'
        color : [0,0,0,1]
        bold: True
    MyTextField:
        id : field1
        pos_hint: {'center_x':0.8,'center_y':0.4}
        font_size: '20sp'
    
    MyTextField:
        id : field2
        pos_hint: {'center_x':0.2,'center_y':0.4}
        font_size: '20sp'
    Button:
        id: language_id
        size_hint: .1, .1
        pos_hint:{'center_x':0.8, 'center_y': 0.1}
        on_press: app.record()
        Image:
			source: 'mic.png'
			pos: self.parent.pos
			size: self.parent.size
			allow_stretch: True
			
	Button:
        id: language
        size_hint: .1, .1
        pos_hint:{'center_x':0.2, 'center_y': 0.1}
        on_press: app.playysound()
        Image:
			source: 'loudspeaker.png'
			pos: self.parent.pos
			size: self.parent.size
			allow_stretch: True
			
			
	BoxLayout:
        pos_hint: {'center_x':0.5,'bottom':0.25}
        orientation: 'horizontal'
    
    Spinner:
		id: spinner_id
		pos_hint: {'center_x':0.2,'center_y':0.9}
		text: "Translated to "
		size_hint : [0.2 , 0.1 ]
		values: ["English", "Arabic", "German", "France", "Greece", "Indonesia"]
		on_text: app.convert_text_to_code(spinner_id.text) 

	Label:
		text: ''  
		
	    
    Spinner:
		id: spinner
		pos_hint: {'center_x':0.8,'center_y':0.9}
		text: "Select voice language"
		size_hint : [0.2 , 0.1 ]
		values: ["English", "Arabic", "German", "France", "Greece", "Indonesia"]
		on_text: app.voice_language(spinner.text) 

	Label:
		text: ''  


        
  
"""

class MyApp(App):
    def build(self):
        return Builder.load_string(KV)

    def convert_text_to_code(self, lang):

        global code_language_for_googletrans

        if (lang == "English"):
            code_language_for_googletrans = 'en'

        if (lang == "Arabic"):
            code_language_for_googletrans = 'ar'

        if (lang == "German"):
            code_language_for_googletrans = 'de'

        if (lang == "France"):
            code_language_for_googletrans = 'fr'

        if (lang == "Greece"):
            code_language_for_googletrans = 'el'

        if (lang == "Indonesia"):
            code_language_for_googletrans = 'id'


    def voice_language(self, lang_voice):

        global code_language_for_speech_recognition

        if (lang_voice == "English"):
            code_language_for_speech_recognition = 'en'

        if (lang_voice == "Arabic"):
            code_language_for_speech_recognition  = 'ar'

        if (lang_voice == "German"):
            code_language_for_speech_recognition  = 'de'

        if (lang_voice == "France"):
            code_language_for_speech_recognition = 'fr'

        if (lang_voice == "Greece"):
            code_language_for_googletrans = 'el'

        if (lang_voice == "Indonesia"):
            code_language_for_speech_recognition  = 'id'



    def record(self):

        global content
        global texttt
        try:
            with mic as source:
                audio = r.listen(source)
                content = r.recognize_google(audio,language=code_language_for_speech_recognition)
                print("Did you say ", content)

                field = self.root.ids['field1']
                field.text = content

                translated = tr.translate(content, code_language_for_googletrans)
                texttt = translated.text

                field = self.root.ids['field2']
                field.text = texttt


        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")

    def playysound(self):

        tts = gTTS(text=texttt, lang=code_language_for_googletrans)
        filename = "w.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)



if __name__=='__main__':
    app = MyApp()
    app.run()