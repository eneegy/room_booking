import frappe
import datetime

def get_context(context):
    query_params = frappe.request.args
    if validate_query_params(frappe.request.args):
        context.rooms = get_available_rooms(query_params['fromDate'], query_params['toDate'], query_params['capacity'])
    else:
        context.error = 'Invalid paramters'
    return context

def validate_query_params(params):
    try:
        fromDate = datetime.datetime.strptime(params['fromDate'], '%Y-%m-%d').date()
        toDate = datetime.datetime.strptime(params['toDate'], '%Y-%m-%d').date()
        today = datetime.date.today()
        int(params['capacity'])
        if fromDate < today or toDate < today:
            return False
        return True
    except ValueError:
        return False

@frappe.whitelist(allow_guest=True)
def get_available_rooms(from_date, to_date, capacity, limit=5, offset=0):
    room_orders = frappe.db.get_list('Room Order Item', fields=['name', 'room'], filters={
        'check_out': ['>=', from_date],
        'docstatus': 1
    })
    room_query_paramters = {
        'capacity': capacity,
        'from_date': from_date,
        'to_date': to_date,
        'limit': limit,
        'offset': offset
    }
    rooms = frappe.db.sql("""
        select
            detail.name,
            detail.images,
            room_type.name as type_name,
            room_type.room_type_rate as basic_rate,
            detail.description,
            detail.capacity,
            current_room_rate.rate
        from
            `tabRoom Details` detail
            join `tabRoom Type` room_type
            left join (
                select
                    room_rate.room_type,
                    room_rate.rate
                from
                    `tabHotel Room Rate` room_rate
                    inner join `tabPeriods` period on room_rate.period = period.periods_name
                where
                    period.from_date >= %(from_date)s
                    and room_rate.status = 'Active'
            ) AS current_room_rate
            on current_room_rate.room_type = room_type.room_type
        where
            detail.room_type = room_type.room_type
            and capacity + extra_capacity >= %(capacity)s
            and detail.docstatus = 1
        LIMIT %(limit)s OFFSET %(offset)s
    """, room_query_paramters, as_dict = 1)
    if len(room_orders) == 0:
        return rooms
    result = list(room for room in rooms if any(allotment.room == room.name for allotment in room_orders))
    return result