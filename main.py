from functools import wraps
from collections import UserDict

def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Контакт не знайдено"
        except ValueError:
            return "Хибний формат, перевірте кількість аргументів"
        except IndexError:
            return "Хибний формат, перевірте кількість аргументів"
    return wrapper


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must have exactly 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError(f"Phone number {phone} not found.")

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                self.phones.remove(p)
                self.phones.append(Phone(new_phone))
                return
        raise ValueError(f"Phone number {old_phone} not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def __str__(self):
        phones = ', '.join([phone.value for phone in self.phones])
        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Record with name {name} not found.")


@input_error
def add_contact(args, address_book):
    name, phone = args
    if name in address_book.data:
        record = address_book.find(name)
        record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        address_book.add_record(record)
    return f"Contact {name} with phone {phone} added."


@input_error
def change_contact(args, address_book):
    name, old_phone, new_phone = args
    record = address_book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Contact {name} updated phone {old_phone} to {new_phone}."
    else:
        return "Contact not found."


@input_error
def show_phone(args, address_book):
    name = args[0]
    record = address_book.find(name)
    if record:
        return str(record)
    else:
        return "Contact not found."


def show_all(address_book):
    if address_book.data:
        return "\n".join([str(record) for record in address_book.data.values()])
    else:
        return "No contacts available."


def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        cmd, *args = user_input.strip().split()

        if cmd in ["close", "exit"]:
            print("Good bye!")
            break
        elif cmd == "hello":
            print("How can I help you?")
        elif cmd == "add":
            print(add_contact(args, address_book))
        elif cmd == "change":
            print(change_contact(args, address_book))
        elif cmd == "phone":
            print(show_phone(args, address_book))
        elif cmd == "all":
            print(show_all(address_book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()