Hi Sathish,

I wanted to share some thoughts regarding the solution proposed by the Retail Innovation Team as an alternative to the single pod model. While the intention to improve resource utilization is appreciated, this approach—much like the single pod setup—appears to go against the fundamental design principles of Kubernetes. By definition, a Kubernetes pod is the smallest deployable unit, and this solution seems to deviate from that standard.

Additionally, deploying a WAR file within a servlet container that follows a thread-per-request model reflects an older, two-decades-old architecture. This model struggles to scale effectively under modern, high-concurrency demands. Today, the industry is moving toward task-per-request, non-blocking IO approaches using reactive REST services, where a single thread can manage multiple HTTP requests more efficiently.

Not sure when Retail will recognize this shift, but leading organizations have already started adopting more efficient and scalable technologies. For example:
	•	Legacy caching tools like EH Cache, Oracle Coherence, and VMware Data Fabric are being replaced with high-performance solutions like Redis and Aerospike.
	•	ScyllaDB is being adopted over Apache Cassandra for improved performance.
	•	Redpanda is replacing Apache Kafka in several cases; PNC Retail DSP, for instance, has adopted Redpanda.
	•	Popular NoSQL alternatives now include MongoDB, ScyllaDB, Amazon DynamoDB, and Couchbase.

Furthermore, we’re seeing a strong move toward solutions closer to bare-metal performance:
	•	Oracle’s GraalVM allows compiling Java into native binaries.
	•	BlackRock continues using C/C++, while many teams are now adopting Rust for its safety and performance.
	•	Tempus Payments has even adopted Delphi, showing how some organizations are revisiting low-overhead languages for specific use cases.

This industry-wide shift highlights the importance of aligning architecture with modern scalability and performance requirements. I’m happy to explore this further if you’d like to discuss.