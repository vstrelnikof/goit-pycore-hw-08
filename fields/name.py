from fields.field import Field

class Name(Field):
    # Ім'я — обов'язкове поле
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)