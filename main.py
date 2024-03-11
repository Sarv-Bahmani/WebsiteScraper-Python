import requests
from bs4 import BeautifulSoup


class Error(Exception):
    pass


class SyncOutput:
    def __init__(self, phone_number):
        self.url = f"https://sync.me/search/?number={phone_number}"
        self.response = None
        self.div_element = None
        self.phone_number = None
        self.location = None
        self.name = None

    def get_response(self):
        self.response = requests.get(self.url)

    def get_div(self):
        self.get_response()
        if self.response.status_code != 200:
            raise Error("NO INFORMATION!")
        soup = BeautifulSoup(self.response.content, 'html.parser')
        self.div_element = soup.find('div', class_='NumberDetailsCard_card__container___2SMok')

    def get_phone(self):
        phone_number_element = self.div_element.find('h1', class_='NumberDetailsCard_phoneNumber___1E8NS')
        self.phone_number = phone_number_element.text.strip() if phone_number_element else 'N/A'

    def get_location(self):
        location_element = self.div_element.find('div', class_='NumberDetailsCard_card__location___17xLR')
        self.location = location_element.text.strip() if location_element else 'N/A'

    def get_name(self):
        head_section = self.div_element.find('div', class_='NumberDetailsCard_card__head___3dM4Q')
        if head_section:
            name_element = head_section.find('div', class_='NumberDetailsCard_card__name____58-0')
            self.name = name_element.text.strip() if name_element else 'N/A'

    def get_data(self):
        self.get_div()
        if self.div_element:
            self.get_phone()
            self.get_name()
            self.get_location()

    def print_data(self):
        self.get_data()
        data = {'phone_number': self.phone_number, 'name': self.name, 'location': self.location}
        print(data)


phone_number = input("Enter phone number with the country code and a + at the beginning: ")
SyncObject = SyncOutput(phone_number=phone_number)
SyncObject.print_data()

