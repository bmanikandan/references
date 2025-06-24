Hello Padma,

I wanted to let you know that I was not invited to the follow-up meeting that took place yesterday. Mahe reached out to me to review the design intended for presentation in the upcoming all-hands meeting. However, since the CAAR has not yet been approved, the design is not considered finalized. Therefore, we decided to park this item for now.

We did connect with you and Mark last Thursday to discuss this. One major concern still remains:

Why is the team assuming Kafka will magically increase TPS, simply by copying a pattern from another team?

There are several passthrough channels before the Kafka layer that could impact overall performance — these seem to have been overlooked in the TPS evaluation.

Additionally, we have a few more points that require clarification:
	1.	TPS Allocation:
Is the stated 300 TPS (150 reads and 150 writes) allocated per customer or across all customers?
	2.	Selective Inputs:
It appears that only favorable inputs were considered in the design discussions. This selective approach is a concern.
	3.	Pending Technical Discussions:
Several technical aspects are still under discussion, including:
	•	CAP acting as a proxy
	•	Payment ID (traceId) generation
	•	Traffic distribution across POST and GET calls to meet TPS targets
	•	Acknowledgement mechanism for payment initiation requests

Let’s ensure these are addressed before moving forward with any finalized design.

Best regards,
[Your Name]
