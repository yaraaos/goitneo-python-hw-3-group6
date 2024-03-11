from collections import UserDict
from datetime import datetime, timedelta


class Birthday:
    def __init__(self, date):
        if isinstance(date, str):
            if not self.validate_date(date):
                raise ValueError("Invalid date format. Please use DD.MM.YYYY")
            self.date = datetime.strptime(date, '%d.%m.%Y')
        elif isinstance(date, datetime):
            self.date = date
        
    def validate_date(self, date):
        try:
            datetime.strptime(date, '%d.%m.%Y')
            return True
        except ValueError:
            return False


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, number):
        if self.validate_number(number):
            self.number = number
        else:
            raise ValueError("Invalid phone number format")

    def validate_number(self, number):
        if len(number) == 10 and number.isdigit():
            return True
        else:
            return False
        
    def __str__(self):
        return str(self.value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, date):
        self.birthday = Birthday(datetime.strptime(date, '%d.%m.%Y'))
        return self.birthday.date.strftime('%d/%m/%Y')

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        return "Phone added"

    def remove_phone(self, phone_remove):
        for phone in self.phones:
            if phone.value == phone_remove:
                self.phones.remove(phone)
                return "Phone deleted"
        return "Phone not found"

    def edit_phone(self, new_phone):
        self.phones = [Phone(new_phone)]
        return "Phone edited"

    def find_phone(self):
        if self.phones:
            return "; ".join(str(phone.number) for phone in self.phones)
        else:
            return "Phone not found"

    def __str__(self):
        phones_str = "; ".join(phone.number for phone in self.phones)
        return f"Contact name: {self.name.value}, Phone: {phones_str}"


class AddressBook(UserDict):
    def get_birthdays_per_week(self):
        today = datetime.today().date()
        one_week_ahead = today + timedelta(days=7)
        upcoming_birthdays = False 

        print("Upcoming birthdays this week:")
        for name, record in self.data.items():
            if record.birthday:  
                birthday_this_year = record.birthday.date.replace(year=today.year).date()
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                if today <= birthday_this_year <= one_week_ahead:
                    print(f"{name}: {birthday_this_year.strftime('%d.%m.%Y')}")
                    upcoming_birthdays = True  

        if not upcoming_birthdays:
            print("No birthdays next week.")

    def add_record(self, name, record):
        self.data[name] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return "Record not found"

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return "Record deleted"
        else:
            return "Record not found"


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e) 
        except (KeyError, IndexError) as e:
            return "An unexpected error occurred: " + str(e)
    return inner


@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError 
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(name, record) 
    return "Contact added."


@input_error
def change_contact(args, book):
    phone, username = args
    book[phone] = username
    return "Phone changed."


@input_error
def show_phone(args, book):
    username = args[0]
    if username in book:
        record = book[username]
        if record.phones:
            phone_numbers = ", ".join(phone.number for phone in record.phones)
            return phone_numbers
        else:
            return "No phone numbers found"
    else:
        return "Contact not found"
    
def show_birthday(args, book):
    username = args[0]
    if username in book:
        record = book[username]
        if record.birthday:
            return record.birthday.date.strftime('%d.%m.%Y')
        else:
            return "Birthday was not added for this contact"
    else:
        return "Contact not found"


def show_all(book):
    for name, record in book.items():
        print(record)

@input_error
def add_bday(args, book):
    if len(args) < 2:
        return "Please provide both a name and a birthday."
    name, birthday = args[0], args[1]
    if name in book.data:
        record = book.data[name] 
        record.add_birthday(birthday) 
        return "Birthday added successfully."
    else:
        return "Username not found in contacts."


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "all":
            show_all(book)
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "add-birthday":
            print(add_bday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            book.get_birthdays_per_week()
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
