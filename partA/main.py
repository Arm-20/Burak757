import tkinter as tk
from booking_systemGUI import BookingSystemGUI

def main():
    root = tk.Tk()
    app = BookingSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
