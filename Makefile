.PHONY: qa audit translation-records release-check

PYTHON ?= python

qa: audit

audit: translation-records

translation-records:
	$(PYTHON) scripts/validate_translation_records.py

release-check: audit
