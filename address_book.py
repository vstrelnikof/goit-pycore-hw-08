import pickle
from pathlib import Path
from collections import UserDict
from datetime import datetime, date
from record import Record

DATA_FILE = Path("addressbook.pkl")

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError, TypeError) as e:
            return f"Error: {e}"
    return inner

class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> (Record | None):
        return self.data.get(name)

    @input_error
    def add_contact(self, name: str, phone: str) -> str:
        record: Record | None = self.find(name)
        if not record:
            record = Record(name)
            self.add_record(record)
            message = "Contact added."
        else:
            message = "Contact updated."
        record.add_phone(phone)
        return message

    @input_error
    def change_contact(self, name: str, old_phone: str, new_phone: str) -> str:
        record: Record | None = self.find(name)
        if not record:
            raise KeyError(f"No contacts found: {name}")
        if record.edit_phone(old_phone, new_phone):
            return "Phone updated."
        else:
            return "Old phone not found."

    @input_error
    def show_phone(self, name: str) -> str:
        record: Record | None = self.find(name)
        if not record or not record.phones:
            return "Phones not found."
        return f"{name}: {', '.join(p.value for p in record.phones)}"

    @input_error
    def show_all(self) -> str:
        if not self.data:
            return "No contacts saved."
        return "\n".join(str(record) for record in self.data.values())

    @input_error
    def add_birthday(self, name: str, date: str) -> str:
        record: Record | None = self.find(name)
        if not record:
            raise KeyError(f"No contacts found: {name}")
        record.add_birthday(date)
        return "Birthday added."

    @input_error
    def show_birthday(self, name: str) -> str:
        record: Record | None = self.find(name)
        if not record or not record.birthday:
            return "Birthday not found."
        return f"{name}: {record.birthday.value.strftime('%d.%m.%Y')}"

    @input_error
    def show_upcoming_birthdays(self) -> str:
        today = datetime.today().date()
        upcoming = {}
        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value
                try:
                    bday_this_year = bday.replace(year=today.year)
                except ValueError:
                    # Якщо 29 лютого, а рік не високосний → переносимо на 28 лютого
                    if bday.month == 2 and bday.day == 29:
                        bday_this_year = date(today.year, 2, 28)
                    else:
                        raise
                if bday_this_year < today:
                    try:
                        bday_this_year = bday.replace(year=today.year + 1)
                    except ValueError:
                        if bday.month == 2 and bday.day == 29:
                            bday_this_year = date(today.year + 1, 2, 28)
                delta = (bday_this_year - today).days
                if 0 <= delta < 7:
                    day = bday_this_year.strftime("%A")
                    upcoming.setdefault(day, []).append(record.name.value)
        if not upcoming:
            return "No birthdays in the next week."
        return "\n".join(f"{day}: {', '.join(names)}" for day, names in upcoming.items())

    def save_to_file(self, filename: Path = DATA_FILE) -> None:
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load_from_file(cls, filename: Path = DATA_FILE):
        if filename.exists():
            with open(filename, "rb") as f:
                return pickle.load(f)
        return cls()