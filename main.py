from address_book import AddressBook

def parse_input(user_input: str) -> tuple[str, list[str]]:
    """Розбирає введений рядок на команду та аргументи"""
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args

book = AddressBook.load_from_file()
commands = {
    "hello": lambda: "How can I help you?",
    "add": book.add_contact,
    "change": book.change_contact,
    "phone": book.show_phone,
    "all": book.show_all,
    "add-birthday": book.add_birthday,
    "show-birthday": book.show_birthday,
    "birthdays": book.show_upcoming_birthdays,
}

print("Welcome to the assistant bot!")

while True:
    user_input = input("Enter a command: ")
    command, args = parse_input(user_input)
    if command in ("exit", "close"):
        print("Good bye!")
        book.save_to_file()
        break
    handler = commands.get(command)
    if not handler:
        print("Invalid command.")
        continue
    result = handler(*args)
    print(result)
