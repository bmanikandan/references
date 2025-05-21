	•	A single MongoDB collection for all sections is sufficient. Avoid creating separate collections per section.
	•	Section data is first stored in the PNC datastore and discarded after PDF generation — no need to maintain relationships with the Statements collection.
	•	Statement data is generated after PDF creation.
	•	The statement_job is no longer required.
	•	Enable/Disable flags should be managed via template_section_map.
	•	Remove enableSections from merchant_statement_config.
	•	Introduced Statement lifecycle states:
	•	Initiated → Data Collected → Report Generation → Ready → Active