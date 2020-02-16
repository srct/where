import enum


class FieldType(enum.Enum):
    STRING = {'value': str}
    FLOAT = {'value': float}
    INTEGER = {'value': int}
    BOOLEAN = {'value': bool}
    RATING = {'num_reviews': int, 'average_rating': float}

    def validate(self, data):
        if type(data) is not dict:
            raise ValueError("YA DONE GOOFED. NEED A DICT.")
        for field in self.value:
            if field not in data:
                raise ValueError(f"Fields of type {self.name} need a {field} field")
            self.value[field](data[field])  # This will throw ValueError if it fails to validate
