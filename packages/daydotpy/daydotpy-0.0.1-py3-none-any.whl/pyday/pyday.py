import datetime

class pyday:
    def __init__(self, time_obj=None):
        self.time = time_obj if time_obj else datetime.datetime.now()

    @classmethod
    def now(cls):
        return cls()

    def start_of(self, unit):
        if unit == "year":
            self.time = self.time.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        elif unit == "month":
            self.time = self.time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif unit == "day":
            self.time = self.time.replace(hour=0, minute=0, second=0, microsecond=0)
        return self

    def add(self, value, unit):
        if unit == "year":
            self.time += datetime.timedelta(days=value * 365)
        elif unit == "month":
            self.time += datetime.timedelta(days=value * 30)
        elif unit == "day":
            self.time += datetime.timedelta(days=value)
        return self

    def set(self, unit, value):
        if unit == "year":
            self.time = self.time.replace(year=value)
        elif unit == "month":
            self.time = self.time.replace(month=value)
        elif unit == "day":
            self.time = self.time.replace(day=value)
        return self

    def format(self, layout):
        return self.time.strftime(layout)
