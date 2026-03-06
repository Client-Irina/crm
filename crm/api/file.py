import frappe


def after_insert(doc, method):
	"""When an attachment is uploaded to a CRM Deal and custom_project_photo is blank, set it to this file."""
	if doc.attached_to_doctype != "CRM Deal" or not doc.attached_to_name:
		return
	if not doc.file_url:
		return
	if not frappe.db.exists("CRM Deal", doc.attached_to_name):
		return
	current_photo = frappe.db.get_value(
		"CRM Deal", doc.attached_to_name, "custom_project_photo"
	)
	if current_photo:
		return
	frappe.db.set_value(
		"CRM Deal",
		doc.attached_to_name,
		"custom_project_photo",
		doc.file_url,
		update_modified=True,
	)
