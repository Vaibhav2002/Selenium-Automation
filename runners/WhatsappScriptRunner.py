from selenium import webdriver
from scipts.whatsapp_automation import Whatsapp


def __getChromeOptions():
    options = webdriver.ChromeOptions()
    options.add_argument(r'--user-data-dir=C:\Users\vaibh\AppData\Local\Google\Chrome\User Data\Default')
    options.add_argument('--profile-directory=Default')
    return options


if __name__ == '__main__':
    options = __getChromeOptions()
    chrome = webdriver.Chrome(executable_path=r'D:\PycharmProjects\automation\chromedriver.exe', options=options)
    whatsapp = Whatsapp(chrome)
    whatsapp.sendStickerToMultipleUsers(['Sahil Das'], [i for i in range(1, 50)])
