import tkinter as tk
from tkinter import filedialog

import os

from src.backend.services.audio_edit_service import create_audio_file
from src.backend.services.audio_transcript_service import create_transcript_file, load_transcript_text
from src.backend.services.transcript_summary_service import generate_five_bullet_summary_text, generate_answer_general_query

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Podcast Muse")
        self.root.geometry("400x400")  # Set the initial size of the window

        self.transcript_text = None

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
        self.status_string = tk.StringVar(value="Status: Waiting for file upload")
        self.status_label = tk.Label(self.root, textvariable=self.status_string)
        self.status_label.pack(anchor='center', pady=5)
    

    ########################################
    # Initial Summarization Flow
    ########################################
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
        if file_path:
            self.status_string.set("File Processing")
            self.root.update_idletasks()

            base_file_path = os.path.join(os.getcwd(), "resources", "output_files")
            
            # Call the create_audio_file function
            audio_output_path = os.path.join(base_file_path, "podcast_audio.mp3")
            create_audio_file(file_path, audio_output_path, second_length=600)
            
            # Update status string
            self.status_string.set("File Saved, Now Transcribing")
            self.root.update_idletasks()

            # Call the create_transcript_file function
            transcript_output_path = os.path.join(base_file_path, "podcast_transcript.txt")
            transcript_result = create_transcript_file(audio_output_path, transcript_output_path)
            
            if transcript_result is None:
                # If the result is None, call the load_transcript_text function
                transcript_result = load_transcript_text(transcript_output_path)
                if transcript_result is None:
                    # If the result is still None, display an error message and return
                    self.status_string.set("Error: Transcript could not be created")
                    self.root.update_idletasks()
                    return
            
            self.transcript_text = transcript_result
            
            # Update status string
            self.status_string.set("Transcript Complete, Now Summarizing")
            self.root.update_idletasks()

            # Call the generate_five_bullet_summary_text function with the transcript result
            summary_output_path = os.path.join(base_file_path, "podcast_summary.txt")
            summary_result = generate_five_bullet_summary_text(transcript_result, summary_output_path)

            # Update status string
            self.status_string.set("Processing Complete")
            self.root.update_idletasks()

            # Display the summary result below the status string
            self.display_summary_result(summary_result)


    def reset_app(self):
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
        if user_text and len(user_text.split()) <= 100:
            # Limit the user input to 100 words
            user_text = " ".join(user_text.split()[:100])

            # Call the backend function with the user input
            # For demonstration, we will print the user input
            # In your actual implementation, you would call your backend function here
            print(f"User input: {user_text}")

            # Assuming your backend function returns a string, you would then display it
            # For demonstration, we are using a hardcoded string
            response_string = generate_answer_general_query(self.transcript_text, user_text)
            self.response_label.config(text=response_string)
            self.user_input.delete(0, tk.END)
            # self.display_output(response_string)

        #  # Open a new window to get further input from the user
        # self.new_window = tk.Toplevel(self.root)
        # self.new_window.title("General Query")
        
        # # Create a Label and Entry widget in the new window
        # tk.Label(self.new_window, text="Enter your query (up to 200 characters):").pack(pady=10)
        # self.new_user_input = tk.Entry(self.new_window, width=50)
        # self.new_user_input.pack(pady=10)
        
        # # Create a button to submit the query
        # tk.Button(self.new_window, text="Submit", command=self.process_general_query).pack(pady=20)


    # def process_general_query(self):
    #     query_text = self.new_user_input.get()
    #     if query_text and len(query_text) <= 200:
    #         # Close the new window
    #         self.new_window.destroy()
            
    #         # Call the generate_answer_general_query function and get the response
    #         response = generate_answer_general_query(self.transcript_text, query_text)
            
    #         # Display the response where the initial summary was
    #         self.summary_label.config(text=response)



if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
