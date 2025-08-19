Last week: decisions & direction (refined)
	•	Shift in scope: Instead of drawing diagrams, generate executable DDL for the MERCHANT table.
	•	Reference source: A Prod MongoDB instance on Rajiv’s box will be used to inspect existing schema & data patterns.
	•	Data growth model (open choice): Sathish + Scott to pick between
	•	A. Vertical growth via JSON (single JSON/OSON/CLOB column for flexible attributes), or
	•	B. Horizontal (column-per-field) with explicit columns (and possibly an extension table).
	•	Database path: Decide whether to
	•	Start on Oracle 19c (with sharding now, smooth path to 23ai), or
	•	Jump to Oracle 23ai (JSON native/OSON & newer features).
	•	Scope control for today: Only the MERCHANT table (no Fees, Attributes, Pricing, etc.).