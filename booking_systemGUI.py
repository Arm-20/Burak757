import tkinter as tk
from tkinter import messagebox
from flight import Flight

class BookingSystemGUI:
    """
    Main GUI class using Tkinter.
    The UI consists of a left panel for data entry and action buttons,
    and a right panel that displays the seat map in an airplane layout.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("Apache Airlines Seat Booking")
        self.flight = Flight()

        # Build UI: left panel for entries/buttons, right panel for seat map.
        self._build_left_panel()
        self._build_seat_map()

        # Initial update to color-code the seat map.
        self.update_seat_map()

    def _build_left_panel(self):
        """
        Left panel: contains entry fields for Seat ID and Passenger Name,
        and buttons for checking availability, booking, freeing seats,
        showing status, and exiting the application.
        """
        left_frame = tk.Frame(self.master)
        left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        tk.Label(left_frame, text="Seat ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.seat_entry = tk.Entry(left_frame)
        self.seat_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(left_frame, text="Passenger Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = tk.Entry(left_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        self.check_button = tk.Button(left_frame, text="Check Availability", command=self.check_seat)
        self.check_button.grid(row=2, column=0, padx=5, pady=5)

        self.book_button = tk.Button(left_frame, text="Book Seat", command=self.book_seat)
        self.book_button.grid(row=2, column=1, padx=5, pady=5)

        self.free_button = tk.Button(left_frame, text="Free Seat", command=self.free_seat)
        self.free_button.grid(row=3, column=0, padx=5, pady=5)

        self.show_status_button = tk.Button(left_frame, text="Show Booking Status", command=self.show_booking_status)
        self.show_status_button.grid(row=3, column=1, padx=5, pady=5)

        self.exit_button = tk.Button(left_frame, text="Exit", command=self.master.quit)
        self.exit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def _build_seat_map(self):
        """
        Right panel: Builds a visual seat map resembling an airplane layout.
        Layout:
          - 6 rows.
          - Left group: seats A & B (columns 1 and 2).
          - An aisle (empty column 3).
          - Right group: seats C & D (columns 4 and 5).
          - Row labels on column 0.
        """
        self.seat_map_frame = tk.Frame(self.master, bd=2, relief=tk.SUNKEN)
        self.seat_map_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Header row: empty label for row numbers, then seat labels for left group,
        # an empty cell for the aisle, then seat labels for right group.
        tk.Label(self.seat_map_frame, text="").grid(row=0, column=0, padx=5, pady=5)
        left_group = ["A", "B"]
        for i, seat in enumerate(left_group):
            tk.Label(self.seat_map_frame, text=seat, font=("Arial", 10, "bold"))\
                .grid(row=0, column=i+1, padx=5, pady=5)
        tk.Label(self.seat_map_frame, text="").grid(row=0, column=3, padx=20, pady=5)  # Aisle separator
        right_group = ["C", "D"]
        for i, seat in enumerate(right_group):
            tk.Label(self.seat_map_frame, text=seat, font=("Arial", 10, "bold"))\
                .grid(row=0, column=i+4, padx=5, pady=5)

        # Create rows for seats (rows 1 to 6).
        self.seat_buttons = {}
        for row in range(1, 7):
            # Row label
            tk.Label(self.seat_map_frame, text=str(row), font=("Arial", 10, "bold"))\
                .grid(row=row, column=0, padx=5, pady=5)
            # Left group seats (A, B)
            for i, seat_letter in enumerate(left_group):
                seat_id = f"{row}{seat_letter}"
                btn = tk.Button(self.seat_map_frame, text=seat_id, width=4,
                                command=lambda s=seat_id: self.seat_button_click(s))
                btn.grid(row=row, column=i+1, padx=2, pady=2)
                self.seat_buttons[seat_id] = btn
            # Aisle separator (empty cell)
            tk.Label(self.seat_map_frame, text="").grid(row=row, column=3, padx=20, pady=2)
            # Right group seats (C, D)
            for i, seat_letter in enumerate(right_group):
                seat_id = f"{row}{seat_letter}"
                btn = tk.Button(self.seat_map_frame, text=seat_id, width=4,
                                command=lambda s=seat_id: self.seat_button_click(s))
                btn.grid(row=row, column=i+4, padx=2, pady=2)
                self.seat_buttons[seat_id] = btn

    def seat_button_click(self, seat_id):
        """
        When a seat button is clicked, populate the Seat ID entry.
        """
        self.seat_entry.delete(0, tk.END)
        self.seat_entry.insert(0, seat_id)

    def update_seat_map(self):
        """
        Update each seat button's color based on its status.
          - Green indicates a free seat.
          - Red indicates a booked seat.
        """
        for seat_id, btn in self.seat_buttons.items():
            status = self.flight.get_all_seats_status().get(seat_id)
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

        availability = self.flight.check_availability(seat_id)
        if availability is None:
            messagebox.showerror("Error", f"Seat {seat_id} does not exist.")
        else:
            if availability:
                messagebox.showinfo("Availability", f"Seat {seat_id} is FREE.")
            else:
                messagebox.showinfo("Availability", f"Seat {seat_id} is BOOKED.")

    def book_seat(self):
        seat_id = self.seat_entry.get().strip()
        passenger_name = self.name_entry.get().strip() or None
        if not seat_id:
            messagebox.showwarning("Warning", "Please enter a seat ID.")
            return

        success = self.flight.book_seat(seat_id, passenger_name)
        if success:
            messagebox.showinfo("Success", f"Seat {seat_id} has been booked.")
        else:
            messagebox.showerror("Error", f"Could not book seat {seat_id} (it might be already booked or invalid).")
        self.update_seat_map()

    def free_seat(self):
        seat_id = self.seat_entry.get().strip()
        if not seat_id:
            messagebox.showwarning("Warning", "Please enter a seat ID.")
            return

        success = self.flight.free_seat(seat_id)
        if success:
            messagebox.showinfo("Success", f"Seat {seat_id} is now free.")
        else:
            messagebox.showerror("Error", f"Could not free seat {seat_id} (it might already be free or invalid).")
        self.update_seat_map()

    def show_booking_status(self):
        all_seats_status = self.flight.get_all_seats_status()
        status_text = "Seat Status:\n"
        for seat_id, status in all_seats_status.items():
            status_text += f"{seat_id}: {status}\n"
        messagebox.showinfo("Booking Status", status_text)