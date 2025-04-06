class Seat:
    
    def __init__(self, seat_id, status="free", passenger_name=None):
        self.seat_id = seat_id
        self.status = status
        self.passenger_name = passenger_name  # For additional functionality

    def is_free(self):
        return self.status == "free"

    def book(self, passenger_name=None):
        if self.is_free():
            self.status = "booked"
            self.passenger_name = passenger_name
            return True
        return False

    def free(self):
        if not self.is_free():
            self.status = "free"
            self.passenger_name = None
            return True
        return False