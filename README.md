Request for Migration of Services and Onboarding Support for PPG under DSP Namespace

Dear Team,

Overview:
PPG Merchant Services is an external, internet-facing application currently targeting IFT Small Business users (~3,000+). The platform enables merchants to:
	•	View plastic card transactions
	•	Generate reports and statements
	•	View deposits
	•	Manage disputes and chargebacks

This functionality was previously implemented under the APP mnemonic. We are now in the process of decoupling the external-facing features and migrating them under the PPG mnemonic.

We request the same level of support currently extended to the APP mnemonic for a smooth transition.

⸻

Technical Details:
The following components are planned to be used under PPG:
	•	sfp-customer-product-service-dsp
	•	sfp-customer-access-entitlement-dsp

Currently, we have been advised to host these services within our OCP namespace and access the DSP database directly from the APP mnemonic. However, the CAAR and TDF teams have raised concerns that this approach leads to tight coupling, even though it followed an approved integration pattern.

Architecture guidance now recommends hosting the above components within the DSP OCP namespace and exposing them via HTTPS-based API routes (potentially through Apigee) for consumption by PPG or any other mnemonic.

⸻

Request for Support:
	1.	Service Migration Feasibility
Please advise on the feasibility and steps for:
	•	Migrating sfp-customer-product-service-dsp and sfp-customer-access-entitlement-dsp to the DSP namespace
	•	Exposing these services via Apigee as secure API endpoints
	2.	Onboarding PPG under DSP
We would appreciate support to:
	•	Officially onboard PPG under DSP
	•	Update relevant documentation including PTO, PTB, and associated paperwork

Your guidance and assistance in enabling this migration and onboarding effort is highly appreciated.