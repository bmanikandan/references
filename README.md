Decision Document: Hybrid Data Architecture for Transactional and Analytical Use Cases

Background

The organization is evaluating database solutions to support both high-volume transactional workloads and large-scale analytical needs, including Fraud Analytics, Risk Analytics, and BI Reporting. The primary challenge is balancing ACID compliance and referential integrity for core transactional data with scalability and performance for analytical workloads.

⸻

Decision

Adopt a hybrid data architecture consisting of:
	•	Oracle RDBMS for merchant, fees, attributes, and transactional data requiring ACID compliance and referential integrity.
	•	NoSQL datastore (DataStax Cassandra) for analytical workloads, populated through data replication from Oracle.
	•	Data replication implemented via Oracle GoldenGate or Kafka (final tool to be determined).

⸻

Rationale
	1.	Manikandan’s Proposal: Oracle GDD or Cassandra supports write-once, read-many use cases and scales efficiently for Fraud Analytics, Risk Analytics, and BI Reports.
	2.	Scott’s Recommendation: Oracle RDBMS ensures strong consistency and supports relational joins, which are essential for transactional datasets.
	3.	Gins’s Suggestion: Kafka provides a flexible, decoupled alternative to GoldenGate for data exchange between Oracle and Cassandra.
	4.	Final Consensus: A hybrid approach leverages Oracle’s strengths for OLTP while enabling Cassandra to handle OLAP workloads at scale.

⸻

Action Items
	1.	Design Oracle RDBMS schema for merchant, fees, attributes, and transactional data.
	2.	Engage with DataStax for Cassandra licensing discussions.
	3.	Conduct Oracle GDD Proof of Concept (POC) with DBA team.
	4.	Evaluate Oracle GoldenGate vs. Kafka for data replication and finalize the integration choice.
