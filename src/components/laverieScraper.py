#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

class laverieScaper:
	list_machines = []

	def __init__(self) -> None:
		r = requests.get('https://www.proxiwash.com/weblaverie/component/weblaverie/?view=instancesfiche&format=raw&s=444ec2')
		data = r.content.decode('utf-8')
		soup = BeautifulSoup(data, 'html.parser')
		self.__register_machines_infos__(soup)

	def __register_machines_infos__(self, soup) -> None:
		row_ptr = soup.table.tr.next_sibling

		while row_ptr is not None:
			current_machine = {}
			current_machine['id'] = int(row_ptr.td.next_sibling.text[-1])
			current_machine['type'] = row_ptr.td.get_text(strip=True)
			current_machine['start_time'] = row_ptr.td.next_sibling.next_sibling.next_sibling.next_sibling.get_text(strip=True)
			current_machine['state'] = row_ptr.td.next_sibling.next_sibling.get_text(strip=True)
			current_machine['end_time'] = row_ptr.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.get_text(strip=True)
			self.list_machines.append(current_machine)
			row_ptr = row_ptr.next_sibling

	def printMachinesStates(self):
		for machine in self.list_machines:
			print(machine)

	def getMachines(self):
		return self.list_machines

	def getMachineByIndex(self, index):
		return self.list_machines[index]