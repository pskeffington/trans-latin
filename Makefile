.PHONY: qa audit package-smoke witnesses translation-records latin-units processing-handoffs audit-events audit-chain review-packet status-report audit-manifest release-bundle unit-ids rights-check required-dirs release-check

PYTHON ?= python

qa: audit

audit: package-smoke witnesses translation-records latin-units processing-handoffs audit-events audit-chain unit-ids rights-check required-dirs review-packet status-report audit-manifest

package-smoke:
	PYTHONPATH=src $(PYTHON) scripts/qa/check_package_smoke.py

witnesses:
	$(PYTHON) scripts/qa/validate_witnesses.py

translation-records:
	$(PYTHON) scripts/validate_translation_records.py

latin-units:
	$(PYTHON) scripts/qa/validate_latin_translation_units.py

processing-handoffs:
	$(PYTHON) scripts/qa/validate_processing_handoffs.py

audit-events:
	$(PYTHON) scripts/qa/validate_audit_events.py

audit-chain:
	$(PYTHON) scripts/qa/check_audit_chain.py

review-packet:
	$(PYTHON) scripts/export/export_review_packet.py

status-report:
	$(PYTHON) scripts/qa/generate_status_report.py

audit-manifest:
	$(PYTHON) scripts/export/generate_audit_manifest.py
	$(PYTHON) scripts/qa/validate_audit_manifest.py

release-bundle: audit
	$(PYTHON) scripts/export/stage_release_bundle.py
	$(PYTHON) scripts/qa/check_release_bundle.py

unit-ids:
	$(PYTHON) scripts/qa/check_unit_ids.py

rights-check:
	$(PYTHON) scripts/qa/check_rights_sensitive_files.py

required-dirs:
	$(PYTHON) scripts/qa/check_required_spine.py

release-check: release-bundle
