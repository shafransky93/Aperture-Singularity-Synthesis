import tkinter as tk
from functools import partial
from ApertureSingularitySynthesis import SingingSynthesizer

def synthesize_button_clicked(text_entry, synthesizer):
    text = text_entry.get()

    if text:
        synthesizer.synthesize_singing(text)
    else:
        print("Please enter some text.")

def create_gui():
    # Create the main window
    window = tk.Tk()
    window.title("Singing Synthesis")

    # Set a custom background color
    window.configure(bg="#f2f2f2")

    # Create the text entry field
    text_label = tk.Label(window, text="Text:", bg="#f2f2f2", font=("Arial", 12))
    text_label.pack(pady=10)
    text_entry = tk.Entry(window, font=("Arial", 12))
    text_entry.pack()

    # Create the SingingSynthesizer instance
    synthesizer = SingingSynthesizer()

    # Create the synthesis button
    synthesize_button = tk.Button(window, text="Synthesize", command=partial(synthesize_button_clicked, text_entry, synthesizer), bg="#4caf50", fg="white", font=("Arial", 12))
    synthesize_button.pack(pady=20)

    # Run the GUI event loop
    window.mainloop()

# Run the GUI
create_gui()
