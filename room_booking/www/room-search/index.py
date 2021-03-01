@frappe.whitelist(allow_guest=True)
def get_available_rooms(from_date, to_date, capacity)
    rooms = frappe.db.getlist('Hotel Room')