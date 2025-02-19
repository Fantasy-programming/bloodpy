import customtkinter as ctk
from auth import AdminLogin

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    root = ctk.CTk()
    app = AdminLogin(root)
    root.mainloop()
