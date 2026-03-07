def validate(doc, method):
	"""Sync custom_estimate_status from status on every change/validate."""
	if doc.get("status"):
		doc.custom_estimate_status = doc.status
