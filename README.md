Subject: Clarification on Asynchronous Payments TPS and Kafka Integration

Hi Padma,

I was not aware that the follow-up meeting happened yesterday.

During last week’s meeting, we requested your help in gathering the current Asynchronous payments TPS and the expected/growth TPS from the business side. This information is critical, as we’ve seen several architecture decisions being made based on assumptions rather than concrete data—particularly regarding the introduction of Kafka between CAP and the inner APIs.

To help us proceed with clarity and avoid repeating past mistakes, could you please help address the following questions?
	1.	What is the expected TPS (transactions per second) for Asynchronous payments?
	2.	What is the current TPS being processed by CAP for Asynchronous payments?
	3.	How much time does CAP take to forward a request to the upstream systems after Apigee completes Bearer token validation?
	4.	What evidence supports the assumption that introducing Kafka between CAP and inner APIs can scale to 1000+ TPS?
	•	Are there benchmarks or performance studies that validate this?
	•	Or is this approach based solely on assumptions?
	5.	How can we confidently return a payment response with a Trace ID before the incoming request has been sanitized?
	•	What are the implications and risks of this design choice?

Given the significance of these changes, it’s important we align with both technical and business expectations to avoid creating unnecessary technical debt.

Looking forward to your input.

Best regards,
[Your Name]
