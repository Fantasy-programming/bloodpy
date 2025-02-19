import customtkinter as ctk
import tkinter.messagebox as messagebox
from PIL import Image
from database import Database
from ui import BloodBankUI


class AdminLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login")
        self.root.geometry("1000x700")  # Increased window size
        self.db = Database()

        # Configure grid weights to center content
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.grid(row=0, column=1, sticky="nsew")

        # Left image
        try:
            left_image = ctk.CTkImage(
                light_image=Image.open("assets/left.jpg"),
                dark_image=Image.open("assets/left.jpg"),
                size=(250, 700),
            )
            left_label = ctk.CTkLabel(self.root, image=left_image, text="")
            left_label.grid(row=0, column=0, sticky="nsew")
        except:
            print("Left image not found")

        # Right image
        try:
            right_image = ctk.CTkImage(
                light_image=Image.open("assets/right.jpg"),
                dark_image=Image.open("assets/right.jpg"),
                size=(250, 700),
            )
            right_label = ctk.CTkLabel(self.root, image=right_image, text="")
            right_label.grid(row=0, column=2, sticky="nsew")
        except:
            print("Right image not found")

        # Logo at the top
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open("assets/logo.png"),
                dark_image=Image.open("assets/logo.png"),
                size=(150, 150),
            )
            logo_label = ctk.CTkLabel(main_frame, image=logo_image, text="")
            logo_label.pack(pady=(50, 40))
        except:
            print("Logo not found")

        # Login frame with increased horizontal padding
        login_frame = ctk.CTkFrame(main_frame)
        login_frame.pack(padx=20, pady=20)

        # Container for form elements with padding
        form_container = ctk.CTkFrame(login_frame, fg_color="transparent")
        form_container.pack(padx=40, pady=20)  # Added horizontal padding

        # Username
        username_label = ctk.CTkLabel(
            form_container, text="Username:", font=("Helvetica", 14)
        )
        username_label.pack(pady=(0, 5))

        self.username_entry = ctk.CTkEntry(
            form_container,
            width=300,
            height=40,
            font=("Helvetica", 14),
            placeholder_text="Enter username",
        )
        self.username_entry.pack(pady=(0, 20))

        # Password
        password_label = ctk.CTkLabel(
            form_container, text="Password:", font=("Helvetica", 14)
        )
        password_label.pack(pady=5)

        self.password_entry = ctk.CTkEntry(
            form_container,
            width=300,
            height=40,
            font=("Helvetica", 14),
            placeholder_text="Enter password",
            show="*",
        )
        self.password_entry.pack(pady=(0, 20))

        # Login button
        login_button = ctk.CTkButton(
            form_container,
            text="Login",
            command=self.login,
            width=200,
            height=40,
            font=("Helvetica", 14, "bold"),
        )
        login_button.pack(pady=(0, 20))

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror(
                "Login Error", "Please enter both username and password"
            )
            return

        # Authenticate credentials
        if self.db.authenticate_admin(username, password):
            messagebox.showinfo("Login Successful", "Welcome!")
            self.root.destroy()  # Close login window
            # Open main application window
            main_window = ctk.CTk()
            BloodBankUI(main_window)
            main_window.mainloop()
        else:
            messagebox.showerror(
                "Login Failed", "Invalid credentials. Please try again."
            )
