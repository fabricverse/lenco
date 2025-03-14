import frappe

def get_context(context):
    context.request_data = frappe.form_dict
    print("\n")