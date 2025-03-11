# Copyright (c) 2025, Adam Dawoodjee and contributors
# For license information, please see license.txt

# import frappe

import frappe
from frappe import _
from frappe.model.document import Document


class LencoSettings(Document):
	pass

@frappe.whitelist()
def get_lenco_settings():
	"""Returns the Lenco public key from settings."""
	settings = frappe.get_doc("Lenco Settings")
	return {
		"public_key": settings.public_key,
		"environment": settings.sandbox
	}