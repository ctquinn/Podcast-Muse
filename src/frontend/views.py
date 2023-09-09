import tkinter as tk
from tkinter import filedialog

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")
        self.init_ui()

    def init_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.upload_button = tk.Button(self.root, text="Upload File", command=self.upload_file)
        self.upload_button.pack(pady=20)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # Call the backend function for processing the file
            # For demonstration, we will print the file path
            # In your actual implementation, you would call your backend function here
            print(f"File selected: {file_path}")

            # Assuming your backend function returns a string, you would then display it
            # For demonstration, we are using a hardcoded string
            output_string = "Output from backend processing"
            self.display_output(output_string)

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
        if user_text:
            # Limit the user input to 100 words
            user_text = " ".join(user_text.split()[:100])

            # Call the backend function with the user input
            # For demonstration, we will print the user input
            # In your actual implementation, you would call your backend function here
            print(f"User input: {user_text}")

            # Assuming your backend function returns a string, you would then display it
            # For demonstration, we are using a hardcoded string
            response_string = "Response from backend"
            self.display_output(response_string)




if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
