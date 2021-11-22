import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains


class Whatsapp:
    driver = None

    __searchIconXPath = '//*[@id="side"]/div[1]/div/label/div'
    __searchBarXPath = '//*[@id="side"]/div[1]/div/label/div/div[2]'
    __userItemXPath = '//span[@title = "{}"]'
    __messageBoxXPath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
    __sendButtonXPath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'
    __emojiButtonXPath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[1]/button[2]/span'
    __stickerButtonXPath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[1]/button[4]'
    __stickerXPath = '//*[@id="main"]/footer/div[2]/div/div[3]/div[1]/div/div[1]/div[2]/div/div[1]/div[{}]/div/span/img'

    # new chat x-paths
    __newChatUrl = 'https://wa.me/{}'
    __newChatBtnXPath = '//*[@id="action-button"]'
    __continueInWhatsappWebBtnXpath = '//*[@id="fallback_block"]/div/div/a'

    def __init__(self, driver):
        self.driver = driver
        self.driver.get("https://web.whatsapp.com")

    def __click(self, xPath, willWait=True):
        if willWait:
            self.__makeWaitUntilClickable(xPath)
        self.driver.find_element(by=By.XPATH, value=xPath).click()

    def __find(self, xPath, willWait=True):
        if willWait:
            self.__makeWaitUntilVisible(xPath)
        return self.driver.find_element(by=By.XPATH, value=xPath)

    def __makeWaitUntilVisible(self, xPath):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xPath)))

    def __makeWaitUntilClickable(self, xPath):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, xPath)))

    def __moveToElement(self, element):
        ActionChains(self.driver).move_to_element(element).perform()

    def __sendMessages(self, messages):
        text_input = self.__find(self.__messageBoxXPath)
        for message in messages:
            text_input.send_keys(message)
            self.__click(self.__sendButtonXPath)

    def __sendStickers(self, stickerIndexes):
        for i in stickerIndexes:
            if i == stickerIndexes[0]:
                # pressing emoji button
                self.__click(self.__emojiButtonXPath)
                # pressing sticker button
                self.__click(self.__stickerButtonXPath)
            # send stickers
            print(i)
            try:
                self.__click(self.__stickerXPath.format(i))
            except TimeoutException:
                self.driver.execute_script('arguments[0].scrollIntoView(true)',
                                           self.driver.find_element(By.XPATH, self.__stickerXPath.format(i)))

    def __searchUser(self, user):
        self.__click(self.__searchIconXPath)
        searchBar = self.__find(self.__searchBarXPath)
        searchBar.send_keys(user)
        time.sleep(2)
        # find user
        try:
            self.__click(self.__userItemXPath.format(user))
        except TimeoutException:
            print("Contact not found")

    def sendMessageToMultipleUsers(self, usernames, messages):
        for user in usernames:
            self.__searchUser(user)
            self.__sendMessages(messages)

    def sendStickerToMultipleUsers(self, usernames, stickerIndexes):
        for user in usernames:
            self.__searchUser(user)
            self.__sendStickers(stickerIndexes)

    def sendMessageToUnknownNumbers(self, phoneNumbers, messages):
        for phoneNumber in phoneNumbers:
            self.driver.get(self.__newChatUrl.format(phoneNumber))
            self.__click(self.__newChatBtnXPath)
            self.__click(self.__continueInWhatsappWebBtnXpath)
            self.__sendMessages(messages)
