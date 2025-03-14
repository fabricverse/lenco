import frappe
from frappe import _
from frappe.utils.password import get_decrypted_password
from datetime import datetime

def get_context(context):
    context.name = "Administrator"

    settings = frappe.get_doc("Lenco Settings")
    context.key = get_decrypted_password("Lenco Settings", "Lenco Settings", "api_public_key", False)
    #"pub-e2c508bc1bf4d846ed54fa7f22dd3f0c2ae5e8422052a552"
    context.url = "https://pay.lenco.co/js/v1/inline.js"
    if settings.sandbox == 1:
        context.url = "https://pay.sandbox.lenco.co/js/v1/inline.js"


    """
    Retrieves payment link details based on the 'l' query parameter and sets context.
    Displays a "Not Found" error if the link is invalid.
    """
    link_id = frappe.request.args.get('link')

    if not link_id:
        context.message = _("Invalid payment link.")
        context.title = _("Payment Link Not Found")
        context.not_found = True
        print('payment_link')
        return

    try:
        pl = frappe.get_all("Payment Link", filters={"route": link_id}, limit=1, pluck='name')
        if pl:
            payment_link = frappe.get_doc("Payment Link", pl[0])

            channels = get_payment_channels(payment_link.name)
            context.channels = channels

            context.amount = payment_link.price
            context.currency = payment_link.currency
            context.vendor_name = payment_link.vendor_name
            context.vendor_slug = payment_link.vendor_name.lower().replace(' ', '-')
            context.description = payment_link.description
            context.purchase_type = payment_link.purchase_type
            
            now = datetime.now()
            context.datetime = str(now.strftime("%d%m%Y%H%M%S"))
            context.current_date = now.strftime("%m/%d/%Y")
            context.current_time = now.strftime("%H:%M:%S")

            print(context.purchase_type)

            context.not_found = False

            context.url = "https://pay.lenco.co/js/v1/inline.js"
            if settings.sandbox==1 or payment_link.status=="Testing":
                context.url = "https://pay.sandbox.lenco.co/js/v1/inline.js"

        else:
            raise frappe.DoesNotExistError

    except frappe.DoesNotExistError:
        context.message = _("Payment link not found.")
        context.title = _("Payment Link Not Found")
        context.not_found = True
        print('DoesNotExistError')
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Error retrieving payment link"))
        context.message = _("An unexpected error occurred.")
        context.title = _("Error")
        context.not_found = False

        print('Exception', str(e))

def get_payment_channels(link_name):
    channels = frappe.get_all("Lenco Payment Mode", filters={"parent": link_name}, fields=["mode"])
    return [channel.mode.lower().replace(' ', '-') for channel in channels]