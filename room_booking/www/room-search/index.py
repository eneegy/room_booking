import frappe

@frappe.whitelist(allow_guest=True)
def get_available_rooms(from_date, to_date, capacity):
    rooms = frappe.db.get_list('Hotel Room',
                               filters={
                                   'capacity': ['>=', capacity]
                               })
    # (0 - draft, 1 - submitted, 2- cancelled)
    room_allotments = frappe.db.get_list('Hotel Room Allotment',
                                        filters={
                                            'to_date': ['>=', from_date],
                                            'status': ['in', ['Booked', 'Checked in']],
                                            'docstatus': 1
                                        },
                                        fields=['room', 'docstatus'])
    if len(room_allotments) == 0:
        return rooms
    result = list(room for room in rooms if any(allotment.room == room.room for allotment in room_allotments))
    return result