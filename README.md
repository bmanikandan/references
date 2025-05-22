📦 Scepter Error Handling Library for Spring Boot

This library provides a standardized, robust error-handling mechanism for RESTful APIs built with Spring Boot. It is designed to minimize ambiguity, reduce boilerplate, and ensure that all error responses are handled consistently and clearly—regardless of developer interpretation or custom exception design.

✅ Key Features
	•	Standards-Compliant Error Format
	•	Implements RFC 9457 — Problem Details for HTTP APIs, published July 2023.
	•	Supports extended, non-standard members to enable actionable client behavior based on error codes.
	•	Accurate HTTP Status Codes
	•	Errors return proper HTTP status codes (400, 404, 409, 500, etc.) based on the error context.
	•	Ensures that error semantics match the underlying cause.
	•	Detailed, Structured Error Responses
	•	Includes a unique error code, human-readable message, and context-specific details.
	•	Designed to help clients understand and fix issues quickly.
	•	Internationalization (i18n) Support
	•	Default locale: en-US.
	•	Seamless localization via message property files (messages_es.properties, messages_ja.properties, etc.).
	•	No additional coding required to support new languages.
	•	Unified Exception Treatment
	•	Treats JDK exceptions and domain-specific custom exceptions equally.
	•	Always produces a consistent response structure.
	•	Fail-Fast Constraint Validation
	•	Bean validation uses a fail-fast strategy to reduce CPU cycles for invalid requests.
	•	Improves API performance by rejecting bad requests early in the request lifecycle.

📌 Benefits
	•	Developers don’t need to write boilerplate error handlers or worry about consistency.
	•	Clients get predictable and machine-readable error responses.
	•	Easy integration into any Spring Boot application without heavy customization.