from fields.field import Field

class Phone(Field):
    # Телефон з валідацією (10 цифр)
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

    @staticmethod
    def validate(value):
        return value.isdigit() and len(value) == 10

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        self._value = value