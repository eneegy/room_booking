# -*- coding: utf-8 -*-
# Copyright (c) 2021, eneegy and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
import frappe

class RoomOrders(Document):
	def validate(self):
		if len(self.room) == 0:
			msg = "Not allow to save order with empty room list"
			frappe.throw(msg)

	def before_insert(self):
		self.set_check_in_out_date()
		self.extra_total = self.calculate_extras()
		self.net_total = self.extra_total + self.get_room_price()

	def set_check_in_out_date(self):
		check_in = []
		check_out = []
		for room in self.room:
			check_in.append(room.check_in)
			check_out.append(room.check_out)
		self.check_in = min(check_in)
		self.check_out = max(check_out)
	
	def get_room_price(self):
		room_total = 0
		for room in self.room:
			room_detail = frappe.get_doc("Room Details", room.room)
			room_total += room_detail.calculate_price(room.check_in, room.check_out)
		return room_total
	
	def calculate_extras(self):
		extras_total = 0
		extra_names = []
		extras = frappe.db.get_all('Room Extras', fields=['extra_name', 'rate'])
		for extra in self.extras:
			selected_extra = next(item for item in extras if item.extra_name == extra.room_extra)
			if not selected_extra:
				continue
			extras_total += selected_extra.rate * extra.quantity
		return extras_total
		