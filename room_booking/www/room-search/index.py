import frappe

@frappe.whitelist(allow_guest=True)
def get_available_rooms(from_date, to_date, capacity):
    room_orders = frappe.db.get_list('Room Order Item', fields=['name', 'room'], filters={
        'check_out': ['>=', from_date]
    })
    rooms = frappe.db.sql("""
        select name
        from `tabRoom Details`
        where capacity + extra_capacity >= %s
    """, capacity)
    if len(room_orders) == 0:
        return rooms
    result = list(room for room in rooms if any(allotment.room == room for allotment in room_orders))
    return result