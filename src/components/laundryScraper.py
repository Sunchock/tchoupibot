#!/usr/bin/python3
from abc import ABC, abstractmethod
from tkinter.messagebox import NO
from bs4 import BeautifulSoup
import requests

# Scraper to get the machines stats from the Laverie website
class laundryScraper(ABC):
	# default url
	url: str = 'https://www.proxiwash.com/weblaverie/component/weblaverie/?view=instancesfiche&format=raw&s=444ec2'

	# Get data from url and return a BeautifulSoup object
	@abstractmethod
	def __get_data_soup__(self, url: str='') -> BeautifulSoup | None:
		# If url is empty, use the default url
		if not url:
			url = self.url
		# Get the data from the url
		response: requests.Response = requests.get(url)
		# If the request is not successful, return None
		if response.status_code == 200:
			return BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
		return None

	# Feed the machines list from data
	@abstractmethod
	def __feed_machines_list__(self, data_soup: BeautifulSoup) -> list(map(str, str)) | None:
		machines_list: list(map(str, str)) = []
		# Pointer to the machine to be processed
		row_ptr = data_soup.table.tr.next_sibling
		# Loop through all the machines
		while row_ptr is not None:
			current_machine = {}
			current_machine['id'] = int(row_ptr.td.next_sibling.text[-1])
			current_machine['type'] = row_ptr.td.get_text(strip=True)
			current_machine['start_time'] = row_ptr.td.next_sibling.next_sibling.next_sibling.next_sibling.get_text(strip=True)
			current_machine['state'] = row_ptr.td.next_sibling.next_sibling.get_text(strip=True)
			current_machine['end_time'] = row_ptr.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.get_text(strip=True)
			# Add the machine to the list
			machines_list.append(current_machine)
			# Go to the next machine
			row_ptr = row_ptr.next_sibling
		# Return the list of machines else None
		if len(machines_list) > 0:
			return machines_list
		return None

	# Callable method, returns the latest infos about the laundry machines
	@abstractmethod
	def scrape(self, url: str='') -> list(map(str, str)) | None:
		# Get the data from the url
		data_soup: BeautifulSoup = self.__get_data_soup__(url)
		# If the data is not empty, feed the machines list and return it
		if data_soup:
			return self.__feed_machines_list__(data_soup)
		return None