#!/usr/bin/env python
# -*-coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

class AbstractBrowser(object):
	"""
	Abstract browser class which has a webdriver and helper functions as attributes.
	"""
	def __init__(self, executable_path, browser='chromium', **kwargs):
		"""
		browser takes the following values: chromium, firefox, iexplorer
		"""
		if browser == 'chromium':
			chrome_options = webdriver.ChromeOptions()
			chrome_options.add_experimental_option("prefs", kwargs.get('chrome_options', {}))
			self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
		else:
			raise ValueError('Only Chromium webdriver supported at this time.')
		self.wait = WebDriverWait(self.driver, 600)

	def submit_form(self, credentials, **kwargs):
		if len(credentials):
			for key in credentials:
				self.find_element_by_name(key).send_keys(credentials[key])

		if kwargs.has_key('submit_button_id'):
			self.find_element_by_id(kwargs.get('submit_button_id')).click()
		elif kwargs.has_key('submit_button_name'):
			self.find_element_by_name(kwargs.get('submit_button_name')).click()
		else:
			raise ValueError('No submit button parameter provided')

	def get_page_source(self):
		"""
		Returns html source of current page.
		"""
		return self.driver.page_source

	def get_url(self, url):
		self.driver.get(url)

	def find_element_by_name(self, name):
		return self.driver.find_element(By.NAME, name)

	def find_element_by_id(self, _id):
		return self.driver.find_element(By.ID, _id)

	def find_element_by_tag(self, tag_name):
		return self.driver.find_element(By.TAG_NAME, tag_name)

	def wait_for_element(self, attribute_value, by=By.ID):
		self.wait.until(expected_conditions.presence_of_element_located((by, attribute_value)))

	def sleep(self, seconds=60):
		"""
		Calls time.sleep for specified seconds, defaults to 60.
		"""
		time.sleep(seconds)

	def close(self):
		self.driver.close()

	def quit(self):
		self.driver.quit()