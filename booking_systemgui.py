from database_manager import *
import tkinter as tk
from tkinter import messagebox

class BookingSystemGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Apache Airlines Seat Booking (SQLite)")
        # Initialize the database manager
        self.db_manager = DatabaseManager()

        # Define airplane layout:
        # - 6 rows
        # - Left group: seats A & B; Right group: seats C & D (with an aisle in between)
        self.rows = range(1, 7)
        self.left_group = ["A", "B"]
        self.right_group = ["C", "D"]

        # Insert seats into the database
        for row in self.rows:
            for seat in self.left_group + self.right_group:
                seat_id = f"{row}{seat}"
                self.db_manager.insert_seat(seat_id, row, seat)

        # Build the UI panels
        self.build_left_panel()
        self.build_seat_map()

        # Refresh the seat map colors from the database
        self.update_seat_map()

    def build_left_panel(self):
        left_frame = tk.Frame(self.master)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(left_frame, text="Seat ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.seat_entry = tk.Entry(left_frame)
        self.seat_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Passenger Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = tk.Entry(left_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Passport #:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.passport_entry = tk.Entry(left_frame)
        self.passport_entry.grid(row=2, column=1, padx=5, pady=5)

        self.check_button = tk.Button(left_frame, text="Check Availability", command=self.check_seat)
        self.check_button.grid(row=3, column=0, padx=5, pady=5)

        self.book_button = tk.Button(left_frame, text="Book Seat", command=self.book_seat)
        self.book_button.grid(row=3, column=1, padx=5, pady=5)

        self.free_button = tk.Button(left_frame, text="Free Seat", command=self.free_seat)
        self.free_button.grid(row=4, column=0, padx=5, pady=5)

        self.show_status_button = tk.Button(left_frame, text="Show Booking Status", command=self.show_booking_status)
        self.show_status_button.grid(row=4, column=1, padx=5, pady=5)

        self.exit_button = tk.Button(left_frame, text="Exit", command=self.on_exit)
        self.exit_button.grid(row=5, column=0, columnspan=2, pady=10)

    def build_seat_map(self):
        """
        This is constructs the right panel displaying an airplane-like seat map.
        Layout:
          - Header row: Left group seat labels, an empty cell for the aisle, and right group seat labels.
          - Each row starts with a row number, then seat buttons for left group, an aisle separator, then right group.
        """
        self.seat_map_frame = tk.Frame(self.master, bd=2, relief=tk.SUNKEN)
        self.seat_map_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Header row
        tk.Label(self.seat_map_frame, text="").grid(row=0, column=0, padx=5, pady=5)
        for i, seat in enumerate(self.left_group):
            tk.Label(self.seat_map_frame, text=seat, font=("Arial", 10, "bold"))\
                .grid(row=0, column=i+1, padx=5, pady=5)
        tk.Label(self.seat_map_frame, text="").grid(row=0, column=3, padx=20, pady=5)  # Aisle separator
        for i, seat in enumerate(self.right_group):
            tk.Label(self.seat_map_frame, text=seat, font=("Arial", 10, "bold"))\
                .grid(row=0, column=i+4, padx=5, pady=5)

        # Create seat buttons for each row
        self.seat_buttons = {}
        for row in self.rows:
            tk.Label(self.seat_map_frame, text=str(row), font=("Arial", 10, "bold"))\
                .grid(row=row, column=0, padx=5, pady=5)
            # Left group seats
            for i, seat in enumerate(self.left_group):
                seat_id = f"{row}{seat}"
                btn = tk.Button(self.seat_map_frame, text=seat_id, width=4,
                                command=lambda s=seat_id: self.seat_button_click(s))
                btn.grid(row=row, column=i+1, padx=2, pady=2)
                self.seat_buttons[seat_id] = btn
            # Aisle separator (empty cell)
            tk.Label(self.seat_map_frame, text="").grid(row=row, column=3, padx=20, pady=2)
            # Right group seats
            for i, seat in enumerate(self.right_group):
                seat_id = f"{row}{seat}"
                btn = tk.Button(self.seat_map_frame, text=seat_id, width=4,
                                command=lambda s=seat_id: self.seat_button_click(s))
                btn.grid(row=row, column=i+4, padx=2, pady=2)
                self.seat_buttons[seat_id] = btn

    def seat_button_click(self, seat_id):
        """
        When a seat button is clicked, populate the Seat ID entry field.
        """
        self.seat_entry.delete(0, tk.END)
        self.seat_entry.insert(0, seat_id)

    def update_seat_map(self):
        """
        Update each seat button's color based on its booking status:
          - Green for free.
          - Red for booked.
        """
        all_seats = {seat_id: status for seat_id, status in self.db_manager.get_all_seats()}
        for seat_id, btn in self.seat_buttons.items():
            status = all_seats.get(seat_id)
            if status == "free":
                btn.config(bg="green", fg="black")
            elif status == "booked":
                btn.config(bg="red", fg="white")
            else:
                btn.config(bg="gray", fg="white")

    def check_seat(self):
        seat_id = self.seat_entry.get().strip()
        if not seat_id:
            messagebox.showwarning("Warning", "Please enter a seat ID.")
            return
        status = self.db_manager.get_seat_status(seat_id)
        if status is None:
            messagebox.showerror("Error", f"Seat {seat_id} does not exist.")
        else:
            messagebox.showinfo("Seat Status", f"Seat {seat_id} is {status.upper()}.")

    def book_seat(self):
        seat_id = self.seat_entry.get().strip()
        passenger_name = self.name_entry.get().strip() or None
        passport_num = self.passport_entry.get().strip() or None
        if not seat_id:
            messagebox.showwarning("Warning", "Please enter a seat ID.")
            return
        status = self.db_manager.get_seat_status(seat_id)
        if status is None:
            messagebox.showerror("Error", f"Seat {seat_id} does not exist.")
            return
        if status == "booked":
            messagebox.showerror("Error", f"Seat {seat_id} is already booked.")
            return
        # Generate unique booking reference
        booking_ref = generate_unique_booking_ref(self.db_manager)
        self.db_manager.update_seat_booking(seat_id, booking_ref, passport_num, passenger_name, None, "booked")
        messagebox.showinfo("Success", f"Seat {seat_id} has been booked with reference {booking_ref}.")
        self.update_seat_map()

    def free_seat(self):
        seat_id = self.seat_entry.get().strip()
        if not seat_id:
            messagebox.showwarning("Warning", "Please enter a seat ID.")
            return
        status = self.db_manager.get_seat_status(seat_id)
        if status is None:
            messagebox.showerror("Error", f"Seat {seat_id} does not exist.")
            return
        if status == "free":
            messagebox.showerror("Error", f"Seat {seat_id} is already free.")
            return
        self.db_manager.update_seat_booking(seat_id, None, None, None, None, "free")
        messagebox.showinfo("Success", f"Seat {seat_id} is now free.")
        self.update_seat_map()

    def show_booking_status(self):
        seats = self.db_manager.get_all_seats()
        status_text = "Current Seat Status:\n\n"
        for seat_id, status in seats:
            status_text += f"{seat_id}: {status}\n"
        messagebox.showinfo("Booking Status", status_text)

    def on_exit(self):
        self.db_manager.close()
        self.master.quit()
