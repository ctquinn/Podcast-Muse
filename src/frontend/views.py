import tkinter as tk
from tkinter import filedialog

import os

from src.frontend.utility_functions import parse_and_check_audio_file

from src.backend.services.audio_edit_service import create_audio_file_stub, create_audio_files
from src.backend.services.audio_transcript_service import create_transcript_file_stub, create_combined_transcript_file, load_transcript_text
from src.backend.services.transcript_summary_service import generate_five_bullet_summary_text, generate_answer_general_query

class MainApplication:
    def __init__(self, root):
        # TKinter Class Variables
        self.root = root
        self.root.title("Podcast Muse")
        self.root.geometry("600x600")  # Set the initial size of the window

        # Backend Class Variables
        self.transcript_text = None
        self.loading = False
        self.status_string = None
        self.dot_count = 0
        self.qa_dict = {}

        self.init_ui()

    ########################################
    # UI Configuration
    ########################################
    def init_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a frame to hold the title label, with a box outline and a specific background color
        self.title_frame = tk.Frame(self.root, bd=2, relief="solid", highlightbackground="white", highlightthickness=2)
        self.title_frame.pack(anchor='center', padx=20, pady=20)

        # Create a label with large text "Podcast Muse", centered and towards the top, with matching background color
        self.title_label = tk.Label(self.title_frame, text="Podcast Muse", font=('Helvetica', 24))
        self.title_label.pack(anchor='center', padx=10, pady=10)  # Center the label within the frame

        # Create the "Upload File" button, centered and underneath the label
        self.upload_button = tk.Button(self.root, text="Upload File", command=self.upload_file)
        self.upload_button.pack(anchor='center')  # Center the button

        # Status String
        self.status_string = tk.StringVar(value="Please Upload a File in .mp3, .mp4, .mpeg, .mpga, .m4a, .wav, or .webm format")
        self.status_label = tk.Label(self.root, textvariable=self.status_string)
        self.status_label.pack(anchor='center', pady=5)
    

    ########################################
    # Initial Summarization Flow
    ########################################
    def start_loading_animation(self):
        if self.loading:
            self.dot_count += 1
            self.dot_count = (self.dot_count + 1) % 4
            self.status_string.set("Processing" + "." * self.dot_count)
            self.root.after(300, self.start_loading_animation)


    def display_summary_result(self, summary_result):
        # Display the summary result in the UI
        self.summary_label = tk.Label(self.root, text=summary_result, justify='left')
        self.summary_label.pack(anchor='center', pady=5)

        # Create an input field for user text entry
        self.user_input = tk.Entry(self.root, width=50)
        self.user_input.pack(anchor='center', pady=5)
        
        # Create a "Send" button to send the user input
        self.send_button = tk.Button(self.root, text="Send", command=self.send_input)
        self.send_button.pack(anchor='center', pady=5)

        # Create a label to display the response from the generate_answer_general_query function
        self.response_label = tk.Label(self.root, text="", justify='center')
        self.response_label.pack(anchor='center', pady=5)

        # Create a reset button at the bottom of the window
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_app)
        self.reset_button.pack(anchor='center', pady=5)


    def upload_file(self):
        file_path = filedialog.askopenfilename()

        file_name, file_extension, allowed_extension = parse_and_check_audio_file(file_path)

        if file_path and allowed_extension:
            self.loading = True
            self.status_string.set("Processing")
            self.start_loading_animation()

            base_file_path = os.path.join(os.getcwd(), "resources", "output_files")
            
            # Call the create_audio_file function
            audio_output_filename = file_name + "_audio.mp3"
            # audio_output_path = os.path.join(base_file_path, audio_output_filename)
            audio_output_path = os.path.join(base_file_path, file_name)
            # audio_output_list = create_audio_files(file_path, base_file_path, file_name)
            audio_output_list = create_audio_files(file_path, audio_output_path)
            # create_audio_file(file_path, audio_output_path, second_length=600)
        
            # Call the create_transcript_file function
            transcript_output_filename = file_name + "_transcript.txt"
            transcript_output_filename = file_name
            # transcript_output_path = os.path.join(base_file_path, transcript_output_filename)
            transcript_output_path = audio_output_path
            transcript_result = create_combined_transcript_file(audio_output_list, transcript_output_path)
            # transcript_result = create_transcript_file(audio_output_path, transcript_output_path)
            
            if transcript_result is None:
                # If the result is None, call the load_transcript_text function
                transcript_possible_path = os.path.join(audio_output_path, "transcript.txt")
                transcript_result = load_transcript_text(transcript_possible_path)
                if transcript_result is None:
                    # If the result is still None, display an error message and return
                    return
            
            self.transcript_text = transcript_result

            # Call the generate_five_bullet_summary_text function with the transcript result
            summary_output_filename = file_name + "_summary.txt"
            summary_output_path = os.path.join(base_file_path, summary_output_filename)
            summary_result = generate_five_bullet_summary_text(transcript_result, audio_output_path)

            # Update status string
            self.loading=False
            self.status_string.set("Processing Complete")

            # Display the summary result below the status string
            self.display_summary_result(summary_result)

        else:
            self.status_string.set("Invalid File: Please upload a .mp3, .mp4, .mpeg, .mpga, .m4a, .wav, or .webm")


    def reset_app(self):
        self.transcript_text = None
        self.loading = False
        self.status_string = None
        self.dot_count = 0
        self.qa_dict = {}
        self.init_ui()



    ########################################
    # Post Summarization Query Flow
    ########################################
    def display_output(self, output):
        output_label = tk.Label(self.root, text=output)
        output_label.pack(pady=20)

        # Create a text entry for user input and a button to send the input
        self.user_input = tk.Entry(self.root, width=50)
        self.user_input.pack(pady=10)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_input)
        self.send_button.pack(pady=20)

        self.reset_button = tk.Button(self.root, text="Reset", command=self.init_ui)
        self.reset_button.pack(pady=20)


    def send_input(self):
        user_text = self.user_input.get()
        if not user_text or len(user_text.split()) > 100:
            return
        
        # Limit the user input to 100 words
        self.loading = True
        self.start_loading_animation()

        user_text = " ".join(user_text.split()[:100])
        print(f"User input: {user_text}")
        existing_qa = self.qa_dict.get(user_text)
        if existing_qa:
            self.response_label.config(text=existing_qa)
            self.user_input.delete(0, tk.END)
            self.loading = False
            self.status_string.set("Processing Complete")
        else:
            # Call for query response
            response_string = generate_answer_general_query(self.transcript_text, user_text)
            self.qa_dict[user_text] = response_string
            self.response_label.config(text=response_string)
            self.user_input.delete(0, tk.END)

            # Update status string
            self.status_string.set("Processing Complete")
            self.loading = False


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
