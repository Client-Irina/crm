def before_insert(doc, method):
	"""Set custom status fields based on company upon Project creation"""
	if not doc.company:
		return

	# If company is Hempston Home: use REVIEW for HH fields, blank TX field
	if doc.company == "Hempston Home":
		if not doc.custom_project_status:
			doc.custom_project_status = "REVIEW"
		if not doc.custom_design_status:
			doc.custom_design_status = "REVIEW"
		doc.custom_tx_project_status = None

	# If company is Traction X: use REVIEW for TX field, blank HH fields
	elif doc.company == "Traction X":
		if not doc.custom_tx_project_status:
			doc.custom_tx_project_status = "REVIEW"
		doc.custom_project_status = None
		doc.custom_design_status = None


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
