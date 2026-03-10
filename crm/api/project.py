

def validate(doc, method):
	"""Ensure opposite company's status fields are always blank"""
	if not doc.company:
		return

	# If company is Hempston Home, ensure TX field is blank
	if doc.company == "Hempston Home":
		if doc.custom_tx_project_status:
			doc.custom_tx_project_status = None

	# If company is Traction X, ensure HH fields are blank
	elif doc.company == "Traction X":
		if doc.custom_project_status:
			doc.custom_project_status = None
		if doc.custom_design_status:
			doc.custom_design_status = None
