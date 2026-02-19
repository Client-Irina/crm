def before_insert(doc, method):
	"""Set production pipeline fields based on company upon Production Plan creation"""
	if not doc.company:
		return

	# If company is Hempston Home
	if doc.company == "Hempston Home":
		doc.custom_hh_production_pipeline = "REVIEW"
		doc.custom_tx_production_pipeline = None

	# If company is Traction X
	elif doc.company == "Traction X":
		doc.custom_tx_production_pipeline = "REVIEW"
		doc.custom_hh_production_pipeline = None


def validate(doc, method):
	"""Validate that the opposite company's pipeline field is always blank"""
	if not doc.company:
		return

	# If company is Hempston Home, ensure TX field is blank
	if doc.company == "Hempston Home":
		if doc.custom_tx_production_pipeline:
			doc.custom_tx_production_pipeline = None

	# If company is Traction X, ensure HH field is blank
	elif doc.company == "Traction X":
		if doc.custom_hh_production_pipeline:
			doc.custom_hh_production_pipeline = None
