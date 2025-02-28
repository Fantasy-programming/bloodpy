import customtkinter as ctk
from auth import AdminLogin
import tkinter as tk

if __name__ == "__main__":
    try:
        # Set appearance mode
        ctk.set_appearance_mode("light")
        
        # Create root window
        root = ctk.CTk()
        
        # Initialize login screen
        app = AdminLogin(root)
        
        # Start the application
        root.mainloop()
    except Exception as e:
        print(f"Application error: {e}")
    finally:
        # Ensure all Tk resources are properly released
        try:
            pending = root.tk.call('after', 'info')
            if pending:
                for after_id in pending:
                    root.after_cancel(after_id)
        except:
            pass
