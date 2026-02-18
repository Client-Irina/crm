# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def create_project_from_won_deal(doc, method=None):
	"""Create a Project automatically when a CRM Deal is marked as Won."""
	if not doc.has_value_changed("status"):
		return

	status_type = frappe.db.get_value("CRM Deal Status", doc.status, "type")
	if status_type != "Won":
		return

	# Project is from ERPNext
	if "erpnext" not in frappe.get_installed_apps():
		return
	if not frappe.db.table_exists("Project"):
		return

	# Avoid duplicate: we use deal name in project_name for lookup
	if frappe.db.exists("Project", {"project_name": doc.name}):
		return

	customer = frappe.db.get_value("Customer", {"crm_deal": doc.name}, "name")
	if not customer and doc.organization:
		customer = frappe.db.exists("Customer", doc.organization)

	project_name = doc.name
	# If we want a friendlier name, use org + deal but keep uniqueness
	title = doc.organization_name or doc.organization or "Won Deal"
	friendly_name = f"{title} - {doc.name}"
	if frappe.db.exists("Project", {"project_name": friendly_name}):
		return

	notes = _build_deal_notes(doc)

	project = frappe.get_doc(
		{
			"doctype": "Project",
			"project_name": friendly_name,
			"status": "Open",
			"customer": customer or None,
			"expected_start_date": doc.closed_date or frappe.utils.getdate(),
			"notes": notes,
		}
	)

	# Link back to deal if Project has the custom field
	if frappe.get_meta("Project").has_field("custom_crm_deal"):
		project.custom_crm_deal = doc.name

	project.insert(ignore_permissions=True)
	frappe.msgprint(
		_("Project {0} created from won deal.").format(frappe.bold(project.name)),
		indicator="green",
		alert=True,
	)


def _build_deal_notes(doc):
	"""Build notes text from CRM Deal details for the Project."""
	lines = [
		f"Created from CRM Deal: {doc.name}",
		f"Organization: {doc.organization_name or doc.organization or '-'}",
		f"Deal value: {doc.currency or ''} {doc.deal_value or 0}",
		f"Closed date: {doc.closed_date or '-'}",
	]
	if doc.next_step:
		lines.append(f"Next step: {doc.next_step}")
	if doc.email:
		lines.append(f"Contact email: {doc.email}")
	if doc.mobile_no:
		lines.append(f"Contact mobile: {doc.mobile_no}")
	return "\n".join(lines)
