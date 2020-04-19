import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import random
import time

class Attendance:
    def __init__(self):
        self.company_id = os.environ['COMPANY_ID']
        self.account = os.environ['ACCOUNT']
        self.password = os.environ['PASSWORD']
        options = Options()
        options.binary_location = '/app/.apt/usr/bin/google-chrome'
        options.add_argument('lang=en')
        options.add_argument('--headless')

        self.driver = webdriver.Chrome(
            executable_path='/app/.chromedriver/bin/chromedriver', chrome_options=options)

    def login(self):
        self.driver.get('https://attendance.moneyforward.com/employee_session/new')
        self.driver.find_element_by_id('employee_session_form_office_account_name').send_keys(self.company_id)
        self.driver.find_element_by_id('employee_session_form_account_name_or_email').send_keys(self.account)
        self.driver.find_element_by_id('employee_session_form_password').send_keys(self.password)
        self.driver.find_element_by_xpath('//input[@value="ログイン"]').click()

    def stamp(self, target_date):
        self.driver.get('https://attendance.moneyforward.com/my_page/attendances')
        self.open_stamp_modal(target_date)
        time.sleep(3)
        self.fill_up_stamp()
        self.save_stamp()

    def open_stamp_modal(self, target_date):
        target_date_element_xpath = '//td/a[@data-url="/my_page/attendances/{target_date}/edit"]'.format(target_date=target_date)
        target_modal_link = self.driver.find_element_by_xpath(target_date_element_xpath)
        parente_el = target_modal_link.find_element_by_xpath('./..')
        if not parente_el.find_element_by_xpath('//td[@class="column-classification"]').text == '平日':
          raise Exception('not work day')
        else:
          target_modal_link.location_once_scrolled_into_view
          time.sleep(1)
          target_modal_link.click()

    def fill_up_stamp(self):
        # add 2 attendance forms to clock in and clock out
        self.driver.find_element_by_xpath("//*[text()='打刻を追加']").click()
        self.driver.find_element_by_xpath("//*[text()='打刻を追加']").click()

        # ClockIn
        event_form = self.driver.find_element_by_xpath(
            '//select[@name="attendance_schedule_form[attendance_record_forms_attributes][0][event]"]')
        Select(event_form).select_by_value('clock_in')

        time_form = self.driver.find_element_by_xpath(
            '//input[@name="attendance_schedule_form[attendance_record_forms_attributes][0][time]"]')
        time_form.clear()
        time_form.send_keys(self.volatile_time(8, 40))

        # ClockOut
        event_form = self.driver.find_element_by_xpath(
            '//select[@name="attendance_schedule_form[attendance_record_forms_attributes][1][event]"]')
        Select(event_form).select_by_value('clock_out')

        time_form = self.driver.find_element_by_xpath(
            '//input[@name="attendance_schedule_form[attendance_record_forms_attributes][1][time]"]')
        time_form.clear()
        time_form.send_keys(self.volatile_time(18, 50))

    def save_stamp(self):
        save_button = self.driver.find_element_by_xpath(
            '//div[@class="attendance-table-button-contents"]/input[@value="保存"]')
        save_button.click()

    def volatile_time(self, hour, minutes):
        minutes = minutes + random.randrange(-10, 10)
        return "{hour}:{minutes}".format(hour=hour, minutes=minutes)
