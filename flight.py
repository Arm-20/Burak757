from seat import Seat

class Flight:
    
    def __init__(self, flight_number="Burak757"):
        self.flight_number = flight_number
        # For simplicity, we use a small set of seats
        seat_ids = ["1A", "1B", "2A", "2B", "3A", "3B"]
        self.seats = {}
        for seat_id in seat_ids:
            self.seats[seat_id] = Seat(seat_id)

    def get_seat(self, seat_id):
        return self.seats.get(seat_id)

    def check_availability(self, seat_id):
        seat = self.get_seat(seat_id)
        if seat:
            return seat.is_free()
        return None  # Means seat_id does not exist

    def book_seat(self, seat_id, passenger_name=None):
        seat = self.get_seat(seat_id)
        if seat:
            return seat.book(passenger_name)
        return False

    def free_seat(self, seat_id):
        seat = self.get_seat(seat_id)
        if seat:
            return seat.free()
        return False

    def get_all_seats_status(self):
        """
        Returns a dictionary mapping seat_id to its status.
        """
        return {seat_id: seat.status for seat_id, seat in self.seats.items()}