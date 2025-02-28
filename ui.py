# ui.py

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
import datetime
import auth  # For logout functionality

# Define blood groups
BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]


class BloodBankUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Bank Management")
        self.root.geometry("1000x700")
        self.db = Database()
        self.current_donor = None
        self.donate_donor_menu = None  # Initialize the donor menu reference

        self.create_widgets()
        self.populate_treeview()

    def create_widgets(self):
        tree_frame = ctk.CTkFrame(self.root)
        tree_frame.pack(padx=10, pady=10, fill="x")

        # Table
        self.tree = ttk.Treeview(
            tree_frame, columns=("blood_group", "units"), show="headings", height=8
        )
        self.tree.heading("blood_group", text="Blood Group")
        self.tree.heading("units", text="Units Available")
        self.tree.pack(side=tk.LEFT, fill="x", expand=True)

        # Scrollbar of the frame
        scrollbar = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Frame where the 2 forms are
        forms_frame = ctk.CTkFrame(self.root)
        forms_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # --- Donation Frame ---
        donate_container = ctk.CTkFrame(forms_frame)
        donate_container.pack(side=tk.LEFT, padx=40, pady=40)

        donate_frame = ctk.CTkFrame(donate_container, fg_color="transparent")
        donate_frame.pack(padx=40, pady=20)  # Added horizontal padding

        ctk.CTkLabel(
            donate_frame, text="Donate", font=("Helvetica", 24), anchor="center"
        ).grid(row=0, column=0, padx=5, pady=10)

        # Donor Selection
        ctk.CTkLabel(donate_frame, text="Select Donor:", font=("Helvetica", 14)).grid(
            row=1, column=0, padx=5, pady=5
        )

        # Get list of donors
        donors = self.db.fetch_donors()
        donor_names = [f"{d['name']} ({d['blood_group']})" for d in donors]

        self.donate_donor_var = ctk.StringVar()
        self.donate_donor_menu = ctk.CTkOptionMenu(
            donate_frame,
            values=donor_names if donor_names else ["No donors registered"],
            width=300,
            height=40,
            font=("Helvetica", 14),
            variable=self.donate_donor_var,
            command=self.on_donor_selected,
        )
        self.donate_donor_menu.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(donate_frame, text="Units:", font=("Helvetica", 14)).grid(
            row=2, column=0, padx=5, pady=5
        )

        self.donate_units_entry = ctk.CTkEntry(
            donate_frame,
            width=300,
            height=40,
            font=("Helvetica", 14),
            placeholder_text="Enter units of blood",
        )
        self.donate_units_entry.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(donate_frame, text="Date:", font=("Helvetica", 14)).grid(
            row=3, column=0, padx=5, pady=5
        )
        self.donate_date_entry = ctk.CTkEntry(
            donate_frame,
            width=300,
            height=40,
            font=("Helvetica", 14),
            placeholder_text="Enter donation date",
        )
        self.donate_date_entry.insert(
            0, datetime.date.today().strftime("%Y-%m-%d")
        )  # Default to today
        self.donate_date_entry.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkButton(
            donate_frame,
            text="Submit Donation",
            command=self.donate_dbase,
            width=200,
            height=40,
            font=("Helvetica", 14, "bold"),
        ).grid(row=4, columnspan=2, pady=(0, 20))

        # --- Request Frame ---
        request_container = ctk.CTkFrame(forms_frame)
        request_container.pack(side=tk.RIGHT, padx=40, pady=40)

        request_frame = ctk.CTkFrame(request_container, fg_color="transparent")
        request_frame.pack(padx=40, pady=20)

        ctk.CTkLabel(
            request_frame, text="Request", font=("Helvetica", 24), anchor="center"
        ).grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        ctk.CTkLabel(
            request_frame, text="Requester Name:", font=("Helvetica", 14)
        ).grid(row=1, column=0, padx=5, pady=5)
        self.request_name_entry = ctk.CTkEntry(
            request_frame,
            width=300,
            height=40,
            font=("Helvetica", 14),
            placeholder_text="Enter requester name",
        )
        self.request_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(request_frame, text="Blood Group:", font=("Helvetica", 14)).grid(
            row=2, column=0, padx=5, pady=5
        )

        # Get available blood groups (only those with units > 0)
        available_blood_groups = self.get_available_blood_groups()
        
        self.request_bg_entry = ctk.CTkOptionMenu(
            request_frame,
            values=available_blood_groups if available_blood_groups else ["No blood available"],
            width=300,
            height=40,
            font=("Helvetica", 14),
        )
        self.request_bg_entry.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(request_frame, text="Units:", font=("Helvetica", 14)).grid(
            row=3, column=0, padx=5, pady=5
        )
        self.request_units_entry = ctk.CTkEntry(
            request_frame,
            width=300,
            height=40,
            font=("Helvetica", 14),
            placeholder_text="Enter units of blood",
        )
        self.request_units_entry.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkLabel(request_frame, text="Date:", font=("Helvetica", 14)).grid(
            row=4, column=0, padx=5, pady=5
        )
        self.request_date_entry = ctk.CTkEntry(
            request_frame,
            width=300,
            height=40,
            font=("Helvetica", 14),
            placeholder_text="Enter request date",
        )
        self.request_date_entry.insert(
            0, datetime.date.today().strftime("%Y-%m-%d")
        )  # Default to today
        self.request_date_entry.grid(row=4, column=1, padx=5, pady=5)

        ctk.CTkButton(
            request_frame,
            text="Submit Request",
            command=self.request_dbase,
            width=200,
            height=40,
            font=("Helvetica", 14, "bold"),
        ).grid(row=5, columnspan=2, pady=(0, 20))

        # --- Control Buttons (Donor Registration, Donation History, Logout) ---
        control_frame = ctk.CTkFrame(self.root)
        control_frame.pack(pady=10, padx=10)

        donor_reg_button = ctk.CTkButton(
            control_frame,
            text="Register Donor",
            command=self.open_donor_registration,
            width=200,
            height=40,
            font=("Helvetica", 14, "bold"),
        )
        donor_reg_button.grid(row=0, column=0, padx=5)

        donation_history_button = ctk.CTkButton(
            control_frame,
            text="View Donation History",
            command=self.open_donation_history,
            width=200,
            height=40,
            font=("Helvetica", 14, "bold"),
        )
        donation_history_button.grid(row=0, column=1, padx=5)

        donor_management_button = ctk.CTkButton(
            control_frame,
            text="Manage Donors",
            command=self.open_donor_management,
            width=200,
            height=40,
            font=("Helvetica", 14, "bold"),
        )
        donor_management_button.grid(row=0, column=2, padx=5)

        logout_button = ctk.CTkButton(
            control_frame,
            text="Logout",
            command=self.logout,
            width=200,
            height=40,
            font=("Helvetica", 14, "bold"),
        )
        logout_button.grid(row=0, column=3, padx=5)

    def get_available_blood_groups(self):
        """Get blood groups that have available units (> 0)"""
        records = self.db.fetch_all_blood_records()
        available_groups = []
        for record in records:
            if record["units_available"] > 0:
                available_groups.append(record["blood_group"])
        return available_groups

    def populate_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = self.db.fetch_all_blood_records()
        for record in records:
            self.tree.insert(
                "", tk.END, values=(record["blood_group"], record["units_available"])
            )
        
        # Update the request blood group dropdown with available blood groups
        available_groups = self.get_available_blood_groups()
        self.request_bg_entry.configure(
            values=available_groups if available_groups else ["No blood available"]
        )

    def donate_dbase(self):
        if not self.current_donor:
            messagebox.showerror("Input Error", "Please select a donor.")
            return

        blood_group = self.current_donor["blood_group"]
        try:
            units = int(self.donate_units_entry.get().strip())
        except ValueError:
            messagebox.showerror(
                "Input Error", "Please enter a valid number for units."
            )
            return

        if not blood_group:
            messagebox.showerror("Input Error", "Please enter a blood group.")

            return

        self.db.add_donation(blood_group, units)
        self.db.add_transaction(
            self.current_donor["name"], blood_group, units, "DONATION"
        )
        messagebox.showinfo(
            "Donation", f"Donation recorded for blood group {blood_group}."
        )
        self.populate_treeview()
        self.donate_bg_entry.delete(0, tk.END)
        self.donate_units_entry.delete(0, tk.END)

    def request_dbase(self):
        blood_group = self.request_bg_entry.get()
        if blood_group == "No blood available":
            messagebox.showerror("Input Error", "No blood groups are currently available.")
            return
        try:
            units = int(self.request_units_entry.get().strip())
        except ValueError:
            messagebox.showerror(
                "Input Error", "Please enter a valid number for units."
            )
            return

        if not blood_group:
            messagebox.showerror("Input Error", "Please enter a blood group.")
            return

        requester_name = self.request_name_entry.get().strip()
        if not requester_name:
            messagebox.showerror("Input Error", "Please enter requester name.")
            return

        success, msg = self.db.process_request(blood_group, units)
        if success:
            self.db.add_transaction(requester_name, blood_group, units, "REQUEST")
        if success:
            messagebox.showinfo("Request", msg)
        else:
            messagebox.showerror("Request Error", msg)
        self.populate_treeview()
        self.request_bg_entry.delete(0, tk.END)
        self.request_units_entry.delete(0, tk.END)

    def open_donor_registration(self):
        reg_win = ctk.CTkToplevel(self.root)
        reg_win.title("Register Donor")

        label_name = ctk.CTkLabel(reg_win, text="Name:")
        label_name.grid(row=0, column=0, padx=5, pady=5)
        name_entry = ctk.CTkEntry(reg_win)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        label_bg = ctk.CTkLabel(reg_win, text="Blood Group:")
        label_bg.grid(row=1, column=0, padx=5, pady=5)
        bg_entry = ctk.CTkOptionMenu(reg_win, values=BLOOD_GROUPS)
        bg_entry.grid(row=1, column=1, padx=5, pady=5)

        label_contact = ctk.CTkLabel(reg_win, text="Contact:")
        label_contact.grid(row=2, column=0, padx=5, pady=5)
        contact_entry = ctk.CTkEntry(reg_win)
        contact_entry.grid(row=2, column=1, padx=5, pady=5)

        def submit_donor():
            name = name_entry.get().strip()
            blood_group = bg_entry.get()
            contact = contact_entry.get().strip()
            if not name or not blood_group or not contact:
                messagebox.showerror("Input Error", "Please fill in all fields.")
                return
            self.db.register_donor(name, blood_group, contact, datetime.date.today())
            messagebox.showinfo("Success", "Donor registered successfully.")
            self.refresh_donor_list()  # Update the donor dropdown
            reg_win.destroy()

        submit_button = ctk.CTkButton(reg_win, text="Submit", command=submit_donor)
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def open_donation_history(self):
        history_win = ctk.CTkToplevel(self.root)
        history_win.title("Blood Transaction History")
        history_win.geometry("800x600")

        history_frame = ctk.CTkFrame(history_win)
        history_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Create Treeview
        tree = ttk.Treeview(
            history_frame,
            columns=("date", "type", "name", "blood_group", "units"),
            show="headings",
        )

        # Define column headings
        tree.heading("date", text="Date")
        tree.heading("type", text="Type")
        tree.heading("name", text="Name")
        tree.heading("blood_group", text="Blood Group")
        tree.heading("units", text="Units")

        # Define column widths
        tree.column("date", width=100)
        tree.column("type", width=100)
        tree.column("name", width=200)
        tree.column("blood_group", width=100)
        tree.column("units", width=100)

        tree.pack(side=tk.LEFT, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        # Fetch and display records
        records = self.db.fetch_transaction_history()
        if not records:
            tree.insert("", tk.END, values=("No records found", "-", "-", "-", "-"))
        else:
            for record in records:
                tree.insert(
                    "",
                    tk.END,
                    values=(
                        record["transaction_date"].strftime("%Y-%m-%d"),
                        record["transaction_type"],
                        record["name"],
                        record["blood_group"],
                        record["units"],
                    ),
                )

    def refresh_donor_list(self):
        """Update the donor dropdown menu with the latest donor list."""
        donors = self.db.fetch_donors()
        donor_names = [f"{d['name']} ({d['blood_group']})" for d in donors]
        if self.donate_donor_menu:
            self.donate_donor_menu.configure(
                values=donor_names if donor_names else ["No donors registered"]
            )
            if donor_names:  # If there are donors, set to the first one
                self.donate_donor_menu.set(donor_names[0])
                self.on_donor_selected(donor_names[0])

    def on_donor_selected(self, selection):
        """Handle donor selection from dropdown."""
        if selection != "No donors registered":
            donor_name = selection.split(" (")[
                0
            ]  # Extract name from "Name (Blood Group)"
            donor = self.db.get_donor_details(donor_name)
            if donor:
                self.current_donor = donor
                self.donate_bg_entry.set(donor["blood_group"])

    def open_donor_management(self):
        """Open donor management window to view and delete donors"""
        mgmt_win = ctk.CTkToplevel(self.root)
        mgmt_win.title("Donor Management")
        mgmt_win.geometry("800x500")

        # Create frame for donor list
        frame = ctk.CTkFrame(mgmt_win)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Create Treeview for donor list
        columns = ("id", "name", "blood_group", "contact", "donation_date")
        donor_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        # Define column headings
        donor_tree.heading("id", text="ID")
        donor_tree.heading("name", text="Name")
        donor_tree.heading("blood_group", text="Blood Group")
        donor_tree.heading("contact", text="Contact")
        donor_tree.heading("donation_date", text="Last Donation Date")
        
        # Define column widths
        donor_tree.column("id", width=50)
        donor_tree.column("name", width=200)
        donor_tree.column("blood_group", width=100)
        donor_tree.column("contact", width=150)
        donor_tree.column("donation_date", width=150)
        
        donor_tree.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=donor_tree.yview)
        donor_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Add control buttons
        btn_frame = ctk.CTkFrame(mgmt_win)
        btn_frame.pack(pady=10, padx=10, fill="x")
        
        # Function to populate donor list
        def populate_donor_list():
            for item in donor_tree.get_children():
                donor_tree.delete(item)
            
            donors = self.db.fetch_full_donor_list()
            for donor in donors:
                donor_date_str = donor["donation_date"].strftime('%Y-%m-%d') if donor["donation_date"] else "Never"
                donor_tree.insert("", tk.END, values=(
                    donor["id"],
                    donor["name"],
                    donor["blood_group"],
                    donor["contact"],
                    donor_date_str
                ))
        
        # Function to delete selected donor
        def delete_selected_donor():
            selected_item = donor_tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a donor to delete")
                return
                
            donor_id = donor_tree.item(selected_item[0])['values'][0]
            donor_name = donor_tree.item(selected_item[0])['values'][1]
            
            if messagebox.askyesno("Delete Donor", f"Are you sure you want to delete donor {donor_name}? This action cannot be undone."):
                success = self.db.delete_donor(donor_id)
                if success:
                    messagebox.showinfo("Success", f"Donor {donor_name} has been deleted")
                    populate_donor_list()  # Refresh the list
                    self.refresh_donor_list()  # Update the dropdown in main window
                else:
                    messagebox.showerror("Error", "Could not delete donor. Please try again.")
        
        # Add buttons
        delete_btn = ctk.CTkButton(
            btn_frame,
            text="Delete Selected Donor",
            command=delete_selected_donor,
            width=200,
            height=40,
            font=("Helvetica", 14, "bold"),
        )
        delete_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        refresh_btn = ctk.CTkButton(
            btn_frame,
            text="Refresh List",
            command=populate_donor_list,
            width=200,
            height=40,
            font=("Helvetica", 14, "bold"),
        )
        refresh_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Initially populate the donor list
        populate_donor_list()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            login_root = ctk.CTk()
            auth.AdminLogin(login_root)
            login_root.mainloop()


if __name__ == "__main__":
    root = ctk.CTk()
    app = BloodBankUI(root)
    root.mainloop()
