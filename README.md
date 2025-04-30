Hi Sathish,

I wanted to share some thoughts regarding the proposed solution by the Retail Innovation Team as an alternative to the single pod approach. While the intent was to improve resource utilization, this solution—similar to the single pod model—appears to conflict with the core principles of Kubernetes. As per Kubernetes design, a pod is intended to be the smallest deployable unit, and this solution seems to diverge from that foundational concept.

Additionally, deploying a WAR file that depends on a traditional servlet container (which typically follows a thread-per-request model) reflects an older architecture that may not effectively address the challenges of today’s high-concurrency systems. Modern architectures tend to favor reactive, non-blocking IO models where a single thread can handle multiple HTTP requests, enabling more efficient use of system resources.

To illustrate how industry leaders are addressing similar challenges:
	•	Traditional caching solutions like EH Cache, Oracle Coherence, or VMware Data Fabric are being replaced by high-performance alternatives like Redis and Aerospike.
	•	Apache Cassandra is being superseded by ScyllaDB, offering better performance and lower latencies.
	•	Apache Kafka is being replaced by more efficient streaming platforms like Redpanda; PNC Retail DSP, for instance, has adopted Redpanda.
	•	NoSQL options such as MongoDB, ScyllaDB, Amazon DynamoDB, and Couchbase are gaining widespread adoption.

We’re also seeing a broader industry shift towards more hardware-efficient approaches:
	•	Oracle’s GraalVM enables the compilation of Java into native binaries.
	•	Companies like BlackRock continue to leverage C/C++, and many are transitioning to Rust for performance-critical applications.
	•	Interestingly, Tempus Payments is making use of the Delphi programming language.

This movement toward solutions that get closer to the hardware underscores a collective recognition that optimizing resource utilization requires rethinking software architecture at a fundamental level.

Happy to discuss this further if helpful.