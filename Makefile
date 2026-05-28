.PHONY: qa audit translation-records latin-units processing-handoffs audit-events unit-ids rights-check required-dirs release-check

PYTHON ?= python

qa: audit

audit: translation-records latin-units processing-handoffs audit-events unit-ids rights-check required-dirs

translation-records:
	$(PYTHON) scripts/validate_translation_records.py

latin-units:
	$(PYTHON) scripts/qa/validate_latin_translation_units.py

processing-handoffs:
	$(PYTHON) scripts/qa/validate_processing_handoffs.py

audit-events:
	$(PYTHON) scripts/qa/validate_audit_events.py

unit-ids:
	$(PYTHON) scripts/qa/check_unit_ids.py

rights-check:
	$(PYTHON) scripts/qa/check_rights_sensitive_files.py

required-dirs:
	$(PYTHON) scripts/qa/check_required_spine.py

release-check: audit
