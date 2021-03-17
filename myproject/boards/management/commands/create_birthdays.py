from django.core.management.base import BaseCommand, CommandError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
import datetime
from time import sleep


class Command(BaseCommand):
    help='create_birthday name YYYY-MM-DD payment_email'

    def add_arguments(self, parser):
        parser.add_argument('name')
        parser.add_argument('date')

    def fill_in_details(self, browser, name, date):
        host = browser.find_element(By.ID, 'p_lt_ctl05_pageplaceholder_p_lt_ctl01_CreateEvent_TPartyFor')
        host.send_keys(name)
        event_name = browser.find_element(By.ID, 'p_lt_ctl05_pageplaceholder_p_lt_ctl01_CreateEvent_TEventTitle')
        event_name.send_keys(f"{name}'s Birthday")
        start_datetime = browser.find_element(By.ID, 'p_lt_ctl05_pageplaceholder_p_lt_ctl01_CreateEvent_TDateStart')
        end_datetime = browser.find_element(By.ID, 'p_lt_ctl05_pageplaceholder_p_lt_ctl01_CreateEvent_TDateEnd')
        datestr = datetime.date.fromisoformat(date).strftime("%d/%m/%Y")
        start_datetime.send_keys(f"{datestr} 12:01 AM")
        end_datetime.send_keys(f"{datestr} 11:59 PM")

    def handle(self, *args, **options):
        # print(options)
        ff_options = Options()
        ff_options.add_argument('-headless')
        browser = webdriver.Firefox()
        self.browser = browser

        # login should be done
        browser.get('https://www.gift-it-forward.com/Create-An-Event')
        card = browser.find_element(By.ID, 'ListTemplate32')
        card.click()
        continue_button = browser.find_element(By.ID, 'p_lt_ctl05_pageplaceholder_p_lt_ctl01_CreateEvent_LinkButton1')
        continue_button.click()
        charity_button = browser.find_element(By.ID, 'ListCharity33')
        charity_button.click()
        sleep(1)
        close_button = browser.find_element(By.CLASS_NAME, 'close')
        close_button.click()
        continue_button.click()
        sleep(1)

        self.fill_in_details(browser, options['name'], options['date'])

        continue_button.click()
        sleep(1)
        event_info = browser.find_element(By.ID, 'p_lt_ctl05_pageplaceholder_p_lt_ctl01_CreateEvent_TInvitationMessage')
        event_info.send_keys('Please feel free to donate!')
        
        payment = Select(browser.find_element_by_id('ddlPaymentMethod'))
        payment.select_by_value("PayPal")

        event_info = browser.find_element(By.ID, 'p_lt_ctl05_pageplaceholder_p_lt_ctl01_CreateEvent_TPaypalEmail')
        event_info.send_keys('giftteams@mail.com')
        continue_button.click()

        email = browser.find_element(By.ID, 'p_lt_ctl05_pageplaceholder_p_lt_ctl01_CreateEvent_TUsernameLogin')
        email.send_keys('unsungheroes1@mail.com')
        pw = browser.find_element(By.ID, 'p_lt_ctl05_pageplaceholder_p_lt_ctl01_CreateEvent_TPasswordLogin')
        pw.send_keys('!!aMwT5nTB&NfL7B6BSrroRX!RvjFpGRuDoi^3ZU' + Keys.RETURN)

        login_button = browser.find_element(By.ID, 'p_lt_ctl05_pageplaceholder_p_lt_ctl01_CreateEvent_Button3')
        login_button.click()

        confirm_button = browser.find_element(By.ID, 'clickbb')
        confirm_button.click()

        url = "https://www.gift-it-forward.com" +  browser.current_url.split("epage=")[1]

        browser.close()
        browser.quit()

        print(url)
        return url
        
