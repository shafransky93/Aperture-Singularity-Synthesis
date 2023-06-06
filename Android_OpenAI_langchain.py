import speech_recognition as sr
from kivy.app import App
import subprocess
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.lang import Builder

Builder.load_string('''
<WrappingLabel>:
    text_size: self.width, None
    size: self.texture_size

<ImageButton>:
    background_normal: ''
    background_down: ''
''')

class WrappingLabel(Label):
    pass

class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''

class TerminalApp(App):
    def build(self):
        layout = FloatLayout()

        # Set background image
        background_image = Image(source='./images/background.jpg', allow_stretch=True)
        layout.add_widget(background_image)

        # Create a ScrollView widget to contain the Label
        scroll_view = ScrollView()
        scroll_view.size_hint = (1, 0.9)
        scroll_view.pos_hint = {'top': 1}
        layout.add_widget(scroll_view)

        # Create a WrappingLabel widget for the output text
        self.output_label = WrappingLabel(text='', markup=True, size_hint_y=None, valign='top')
        self.output_label.color = (0, 1, 0, 1)  # Set text color to green
        self.output_label.bind(texture_size=self.output_label.setter('size'))
        scroll_view.add_widget(self.output_label)

        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)

        self.input_text = TextInput(multiline=False)
        self.input_text.bind(on_text_validate=self.execute_command)  # Bind Enter key to execute command
        input_layout.add_widget(self.input_text)

        run_button = ImageButton(source='./images/run_button_normal.png', size_hint=(None, 1), width=80)
        run_button.bind(on_press=self.execute_command)
        input_layout.add_widget(run_button)

        speech_button = ImageButton(source='./images/speech_button_normal.png', size_hint=(None, 1), width=80)
        speech_button.bind(on_press=self.speech_to_text)
        input_layout.add_widget(speech_button)

        run_program_button = ImageButton(source='./images/run_program_button_normal.png', size_hint=(None, 1), width=120)
        run_program_button.bind(on_press=self.run_program)
        input_layout.add_widget(run_program_button)

        layout.add_widget(input_layout)

        return layout

    def execute_command(self, instance):
        command = self.input_text.text
        self.input_text.text = ''

        # Check if a program is already running
        if hasattr(self, 'process') and self.process.poll() is None:
            self.process.stdin.write(command + '\n')
            self.process.stdin.flush()
            self.output_label.text += '\n' + command  # Add the command to the output
        else:
            output = ''
            try:
                self.process = subprocess.Popen(['python', 'AppOpenAI_langchain.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE, universal_newlines=True)
                self.process.stdin.write(command + '\n')
                self.process.stdin.flush()
                output, errors = self.process.communicate()
            except FileNotFoundError:
                output = f"Error: Program 'test.py' not found."

            self.output_label.text += '\n$ python AppOpenAI_langchain.py\n' + output

    def speech_to_text(self, instance):
        with sr.Microphone() as source:
            self.output_label.text += '\nListening...'
            audio = self.recognizer.listen(source)

        try:
            self.output_label.text += '\nRecognizing...'
            command = self.recognizer.recognize_google(audio)
            self.input_text.text = command
            self.execute_command(None)
        except sr.UnknownValueError:
            self.output_label.text += '\nUnable to recognize speech.'
        except sr.RequestError as e:
            self.output_label.text += '\nSpeech recognition request error: ' + str(e)

    def run_program(self, instance):
        program_path = 'AppOpenAI_langchain.py'  # Specify the path of the program file
        output = ''
        try:
            process = subprocess.Popen(['python', program_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True)
            output, errors = process.communicate()
        except FileNotFoundError:
            output = f"Error: Program '{program_path}' not found."

        self.output_label.text += '\n$ python ' + program_path + '\n' + output

    def on_start(self):
        self.output_label.text += 'Welcome to the Aperture Singularity Synthesis!\n'
        self.output_label.text += 'Type commands below and press the Run button or Enter to execute.\n'
        self.output_label.text += 'Click the Speak button to use speech-to-text.'
        self.output_label.text += '\nClick the Run Program button to execute a Python program.'
        # Initialize the speech recognizer
        self.recognizer = sr.Recognizer()

if __name__ == '__main__':
    TerminalApp().run()
