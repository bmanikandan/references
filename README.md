A comprehensive modernization of the GP (Global Payments) application featuring a clean-sheet Angular rebuild with microservices architecture to support multiple payment types.

Modular design enables seamless addition of new payment types

 Zero Payment Loss & Continuous Operations
 Payments never fail due to system outages—all transactions are queued and automatically processed when systems recover
 Planned maintenance windows no longer disrupt payment processing
 Consistent performance regardless of transaction volume
 

 Timeline
Production Deployment: November 21, 2025
Current Status: End-to-end testing in progress


Kafka Integration
Migration Achievement
Successfully partnered with PNC Payments team to implement direct Apache Kafka Streams integration, replacing traditional web services.
Technical Advantages
1. Increased Resiliency

Payment messages accumulate in Kafka Stream if downstream systems go offline
Automatic recovery when systems come back online
Acknowledgment messages retained during GP system maintenance or unexpected downtime

2. Enhanced Data Availability

Payments and payment statuses accessible to unlimited consumer applications
No source application changes required for new integrations
Event-driven architecture supports multiple subscribers

3. Superior Throughput

Asynchronous, background processing eliminates communication channel constraints
No error returns during high-volume periods (unlike traditional web services)
Eliminates request limit bottlenecks
