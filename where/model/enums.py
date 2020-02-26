from enum import Enum, unique


class FieldType(Enum):
    STRING = {'value': str}
    FLOAT = {'value': float}
    INTEGER = {'value': int}
    BOOLEAN = {'value': bool}
    RATING = {'num_reviews': int, 'average_rating': float}

    def validate(self, data):
        """
        Given an instance of a value, verfiy that the instance satisfies the
        schema for this primitive type.  e.g. if FieldType.STRING.validate was
        called, it would make sure that the `data` parameter looked like
        {
            "value": "some string"
        }

        This method throws a ValueError if the passed value doesn't conform to the
        schema.

        Parameters:
        data (): the instance of this primitive to validate.
        
        Raises:
        ValueError: if the passed data is incorrect
        """
        if type(data) is not dict:
            raise ValueError("YA DONE GOOFED. NEED A DICT.")
        for field in self.value:
            if field not in data:
                raise ValueError(f"Fields of type {self.name} need a {field} field")
            if type(data[field]) is not self.value[field]:
                raise ValueError(f"Expecting field of type {self.value[field]}, got {type(data[field])}")
        if len(data) != len(self.value):
            raise ValueError(f"Too many fields for field of type {self.name}")


@unique
class AuthLevel(Enum):
    USER = 0
    ADMIN = 1
