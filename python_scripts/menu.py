import pycurl
import pypdf
import datetime
import locale
from io import BytesIO

def get_todays_menu():
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    current_year = datetime.datetime.now().strftime('%Y')
    calendar_week = datetime.datetime.now().strftime('%V')
    todays_day = datetime.datetime.now().strftime('%A')

    url = f"https://clients.eurest.ch/xPrint/reishauer/de/Zahnr%C3%A4dli/{current_year}{calendar_week}/weekly"
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    reader = pypdf.PdfReader(buffer)
    page = reader.pages[0]
    text = page.extract_text()
    reader.close()
    lines = text.split('\n')

    menu = [''] * 3

    for line in lines:
        if todays_day.upper() in line.upper():
            for i in range(3):
                menu[i] = lines[lines.index(line) + i + 1]

    return menu

def generate_menu(menu):
    max_length = max(len(menu[0]), len(menu[1]), len(menu[2])) + 2
    table = (
        f"+{'=' * max_length}+\n"
        f"| {'+ + + Reishauer Zahnrädli Mensa + + +':^{max_length - 1}}|\n"
        f"| {datetime.datetime.now().strftime('%A, %-d. %B %Y'):^{max_length - 1}}|\n"
        f"+{'=' * max_length}+\n"
        f"| {'Menü':<{max_length - 1}}|\n"
        f"+{'-' * max_length}+\n"
        f"| {menu[0]:<{max_length - 1}}|\n"
        f"+{'=' * max_length}+\n"
        f"| {'Vegetarisch':<{max_length - 1}}|\n"
        f"+{'-' * max_length}+\n"
        f"| {menu[1]:<{max_length - 1}}|\n"
        f"+{'=' * max_length}+\n"
        f"| {'Spezial':<{max_length - 1}}|\n"
        f"+{'-' * max_length}+\n"
        f"| {menu[2]:<{max_length - 1}}|\n"
        f"+{'=' * max_length}+"
    )

    print(table)

if __name__ == '__main__':
    original_menu = get_todays_menu()
    generate_menu(original_menu)
