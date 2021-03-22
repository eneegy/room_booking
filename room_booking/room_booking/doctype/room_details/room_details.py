# -*- coding: utf-8 -*-
# Copyright (c) 2021, eneegy and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document
import frappe.database

class RoomDetails(Document):
	def calculate_price(self, from_date, to_date):
		filters = {
			'from_date': from_date,
			'to_date': to_date,
			'room_name': self.room_name
		}
		rate = frappe.db.sql("""
			select
				detail.name,
				room_type.rate as basic_rate,
				current_room_rate.rate
			from
				`tabRoom Details` detail
				join `tabRoom Types` room_type
				left join (
					select
						room_rate.room_type,
						room_rate.rate
					from
						`tabHotel Room Rate` room_rate
						inner join `tabPeriods` period on room_rate.period = period.periods_name
					where
						DATE(period.from_date) <= %(from_date)s
						and DATE(period.to_date) >= %(to_date)s
						and room_rate.status = 'Active'
				) AS current_room_rate
				on current_room_rate.room_type = room_type.type_name
			where
				detail.room_type = room_type.type_name
				and detail.room_name = %(room_name)s
		""", filters, as_dict=1)
		applied_rate = rate[0]
		if not applied_rate['rate']:
			return applied_rate['basic_rate']
		return applied_rate['rate']
