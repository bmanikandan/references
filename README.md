
This change requires an update to the Dockerfile to ensure files are created on the NAS. Currently, the report listener generates files using a random user ID that is not part of group ID 4342.

As a temporary measure to maintain the customer’s synoptic flow, please work with the Midrange team to grant full access (777) to the report folders. A permanent fix will be implemented in the upcoming release.

Epic Name: System Optimization and Efficiency

Epic Summary: Improve overall system performance, reduce resource consumption, and enhance scalability through targeted optimizations across infrastructure, application layers, and processes.

Epic Description:
The goal of this epic is to identify and implement measures to optimize system performance and improve efficiency. This includes analyzing current bottlenecks, reducing latency, enhancing throughput, and optimizing resource usage (compute, memory, storage). The outcomes should lead to better scalability, improved user experience, and cost efficiency.

Goals / Objectives:
	1.	Identify and address performance bottlenecks.
	2.	Optimize application code and database queries.
	3.	Enhance resource utilization (CPU, memory, I/O).
	4.	Improve system scalability to handle increased load.
	5.	Establish monitoring and metrics for ongoing performance insights.

Acceptance Criteria:
	•	Performance benchmarks are defined and measured before and after optimization.
	•	Response times improved by X% (set realistic target).
	•	Resource utilization reduced by Y%.
	•	System can handle Z% more concurrent users without degradation.
	•	Monitoring dashboards and alerts implemented for performance metrics.

Key Deliverables:
	•	Performance audit report.
	•	Optimization plan with prioritized action items.
	•	Implemented code and infrastructure improvements.
	•	Updated documentation on performance best practices.

Dependencies:
	•	Development team for code changes.
	•	Infrastructure/DevOps for environment and scaling adjustments.
	•	QA for performance and load testing.

Potential Stories under this Epic:
	1.	Conduct system performance audit.
	2.	Optimize critical database queries.
	3.	Implement caching strategies.
	4.	Improve API response times.
	5.	Tune container and VM configurations.
	6.	Conduct load and stress testing.
	7.	Set up automated performance monitoring and reporting.
