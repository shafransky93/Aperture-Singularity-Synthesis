import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
from langchain import LLMChain
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
import os
import sys

os.environ['OPENAI_API_KEY'] = '

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, message):
        self.widget.insert(tk.END, message)
        self.widget.see(tk.END)
        update_image_size(None)

def run_agent(event=None):
    user_input = input_entry.get()
    sys.stdout = TextRedirector(output_text)
    agent.run(user_input)

def update_image_size(event):
    window_width = window.winfo_width()
    window_height = window.winfo_height()

    # Resize the background image
    resized_image = image.resize((window_width, window_height), Image.Resampling.LANCZOS)
    updated_image = ImageTk.PhotoImage(resized_image)

    # Update the image in the scrolled text widget
    output_text.image_create(tk.END, image=updated_image)
    output_text.image = updated_image

# Create the main window
window = tk.Tk()
window.title("Aperture-Singularity-Synthesis GUI")
window.geometry("400x400")
window.configure(bg="#0F0F0F")  # Set background color

# Load the background image for the scrolled text widget
image = Image.open("background.jpg")
background_image = ImageTk.PhotoImage(image)

# Create the input label and entry
input_label = ttk.Label(window, text="Question:")
input_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

input_entry = ttk.Entry(window, width=40)
input_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
input_entry.bind("<Return>", run_agent)  # Bind Enter key to run_agent function

# Create the run button
run_button = ttk.Button(window, text="Run", command=run_agent)
run_button.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

# Create the output text area with the background image
output_text = ScrolledText(window, width=50, height=20, bg="black", fg="lime green")
output_text.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
output_text.insert(tk.END, "\n")  # Add padding for the background image
output_text.bind("<Configure>", update_image_size)
output_text.image_create(tk.END, image=background_image)

# Configure grid weights to make the input_entry and output_text widgets expand with the window
window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(0, weight=1)

# Load the language model and tools
dv = OpenAI(model_name='text-davinci-003')
llm = dv
tools = load_tools(["human","llm-math", "arxiv", "wikipedia", "python_repl", "open-meteo-api", "terminal"], llm=llm)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Bind window resize event to update image size
window.bind("<Configure>", update_image_size)

# Start the GUI event loop
window.mainloop()
