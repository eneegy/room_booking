import frappe
import datetime

def get_context(context):
    query_params = frappe.request.args
    if validate_query_params(frappe.request.args):
        context.rooms = get_available_rooms(query_params['fromDate'], query_params['toDate'], query_params['capacity'])
    return context

def validate_query_params(params):
    try:
        datetime.datetime.strptime(params['fromDate'], '%Y-%m-%d')
        datetime.datetime.strptime(params['toDate'], '%Y-%m-%d')
        int(params['capacity'])
        return True
    except ValueError:
        return False


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