import frappe
import json

def get_context(context):
    return context


@frappe.whitelist(allow_guest=True)
def book_room():
    booking_details = json.loads(frappe.request.data)
    create_customer_if_not_exist(booking_details)

def create_customer_if_not_exist(booking_details):
    internal_customer = frappe.db.get_value(
        'Customer',
        {
            'mobile_no': booking_details['phone_number'],
            'email_id': booking_details['email']
        }
    )
    if (not internal_customer):
        customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": '%s %s %s'%(booking_details['first_name'], booking_details['middle_name'], booking_details['last_name']),
            "customer_type": "Individual",
            "customer_group": "Individual",
            "territory": "All Territories"
        })
        customer.insert(ignore_permissions=True)
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
                "links": [
                    {
                        "link_doctype": "Customer",
                        "link_name": '%s %s %s'%(booking_details['first_name'], booking_details['middle_name'], booking_details['last_name'])
                    }
                ],
                "first_name": booking_details['first_name'],
                "middle_name": booking_details['middle_name'],
                "last_name": booking_details['last_name']
            })
        contact.insert()
