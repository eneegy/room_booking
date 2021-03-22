import frappe
import json
import datetime

def get_context(context):
    context.room = frappe.request.args['roomName']
    context.extras = frappe.db.get_all('Room Extras', fields=['extra_name', 'rate', 'description'])
    return context


@frappe.whitelist(allow_guest=True)
def book_room():
    booking_details = json.loads(frappe.request.data)
    test_room = 'Basic 2-1'
    full_name = '%s %s %s'%(booking_details['first_name'], booking_details['middle_name'], booking_details['last_name'])
    full_name2 = 'Thanh Dao'
    # 1. Validate if room available
    if not is_room_in_use(booking_details['room_list'])['error']:
        # 2. Create customer if not exist
        customer = create_customer_if_not_exist(booking_details)
        # 3. Create order
        create_order(customer, booking_details)
    else:
        return {
            'error': 'Room in use',
            'booking_state': 'Failed'
        }

def generate_extras(extras):
    result = []
    for extra in extras:
        result.append({
            'room_extra': extra['name'],
            'quantity': extra['quantity']
        })
    return result

def generate_room_list(rooms):
    result = []
    for room in rooms:
        result.append({
            'room': room['room_name'],
            'check_in': room['check_in'],
            'check_out': room['check_out'],
            'note': None
        })
    return result


def create_order(customer, booking_detail):
    order = frappe.get_doc({
        'doctype': 'Room Orders',
        'customer': customer,
        'guest_name': customer,
        'room': generate_room_list(booking_detail['room_list']),
        'extras': generate_extras(booking_detail['extras'])
    })
    order.insert()
    order.submit()
    return True


def create_customer_if_not_exist(booking_details):
    internal_customer = frappe.db.get_value(
        'Customer',
        {
            'mobile_no': booking_details['phone_number'],
            'email_id': booking_details['email']
        }
    )
    if (not internal_customer):
        full_name = '%s %s %s'%(booking_details['first_name'], booking_details['middle_name'], booking_details['last_name'])
        contact = frappe.get_doc({
                "doctype": "Contact",
                "phone_nos":[
                    {
                        "phone": booking_details['phone_number'],
                        "is_primary_phone": True,
                        "is_primary_mobile_no": True
                    }
                ],
                "email_ids": [
                    {
                        "email_id": booking_details['email'],
                        "is_primary": True
                    }
                ],
                "first_name": booking_details['first_name'],
                "middle_name": booking_details['middle_name'],
                "last_name": booking_details['last_name']
            })
        contact.insert()
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": full_name,
            "customer_type": "Individual",
            "customer_group": "Individual",
            "territory": "All territories",
            "customer_primary_contact": contact.name
        })
        customer.insert(ignore_permissions=True)
        return customer.name
    return internal_customer

def is_room_in_use(room_orders):
    room_names = []
    check_in_dates = []
    check_out_dates = []
    for room in room_orders:
        room_names.append(room['room_name'])
        check_in_dates.append(room['check_in'])
        check_out_dates.append(room['check_out'])

    filters = {
        'room_names': room_names,
        'check_in_dates': check_in_dates,
        'check_out_dates': check_out_dates
    }

    orders = frappe.db.sql("""
        select room_order_item.room, room_orders.check_in, room_orders.check_out as order_count
        from
            `tabRoom Orders` room_orders
            inner join `tabRoom Order Item` room_order_item on room_order_item.parent = room_orders.name
        where
            room_order_item.room IN %(room_names)s
            and DATE(room_orders.check_in) IN %(check_in_dates)s
            and DATE(room_orders.check_out) IN %(check_out_dates)s
            and room_orders.docstatus = 1
    """, filters, as_dict=1)
    for order in orders:
        matched = next(room for room in room_orders if room['room_name'] == order.room)
        check_in = datetime.datetime.strptime(matched['check_in'], '%Y-%m-%d').date()
        check_out = datetime.datetime.strptime(matched['check_out'], '%Y-%m-%d').date()
        order_check_in = order.check_in.date()
        if order_check_in >= check_in and order_check_in <= check_out:
            return {
                'error': 'Room in use',
                'room_number': order.room
            }
    return {
        'error': None
    }

