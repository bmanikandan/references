The CAP Team appears to be moving toward adopting Kafka and standardizing on a single architectural solution, based on the assumption that Kafka inherently delivers speed improvements for both asynchronous and synchronous payment flows.

Synchronous payments refer to transactions processed in real-time or near real-time, where the response is received immediately. In contrast, asynchronous payments involve a delay between the initiation and final resolution of the transaction—processing can take from a few minutes to several days, depending on the payment rail used (e.g., WIRE, ACH).

However, this direction raises concerns for both types of flows. It appears to be more of a technical debt route rather than a well-grounded architectural decision, driven by assumptions rather than validated needs. Additionally, there’s an expectation for CAP to generate trace IDs using a custom open-source algorithm based on timestamps and random text, rather than leveraging standardized enterprise tools. This introduces unpredictability and complexity in managing trace ID uniqueness, especially when their existing custom algorithm, though scaled to millions of payments, lacks enterprise-level controls to prevent duplication.

CAP continues to assert that “the business wants to use Kafka,” but in reality, this direction appears to be largely driven by a contractor who strongly believes this is the best architectural fit for PNC’s flows. Unfortunately, this vision is being justified by leaning on business input rather than aligning with sound technical strategy or enterprise architectural principles. The absence of strong internal guidance to challenge or validate this approach only deepens the risk of misalignment with what PNC truly needs.



Here’s a high-level overview of the current global technology strategy trends (2025) being adopted across leading industries and tech-forward organizations:

⸻

🌐 1. AI-First Strategy
	•	Generative AI Integration: Companies embed AI in customer service, development, operations, and marketing using tools like ChatGPT, Copilot, Claude, etc.
	•	Custom LLMs and Fine-Tuning: Organizations build domain-specific models (legal, medical, finance) to improve performance and control.
	•	AI Governance: Strong focus on AI ethics, regulatory compliance (e.g., EU AI Act), and explainability.

⸻

☁️ 2. Cloud-Native & Multi-Cloud
	•	Kubernetes-first Development: Most new systems are containerized and orchestrated via Kubernetes.
	•	Hybrid and Multi-Cloud: Avoiding vendor lock-in by spreading workloads across AWS, Azure, GCP, and private data centers.
	•	Edge Computing Expansion: Real-time workloads pushed closer to the user (e.g., in retail, manufacturing, telco).

⸻

🔒 3. Zero Trust Security Architecture
	•	Identity-centric Access: Everything from device to app access is authenticated and verified.
	•	SBOM & Supply Chain Security: Security now includes third-party open-source components via Software Bill of Materials (SBOM).
	•	Quantum-safe Encryption: Early adoption of encryption standards resistant to future quantum attacks.

⸻

🏗️ 4. Composable Architecture
	•	API-First and Event-Driven: Businesses shift from monoliths to modular services, often using Kafka, GraphQL, or REST APIs.
	•	Headless Systems: Especially in commerce and CMS systems — front-end and back-end are decoupled.
	•	Serverless Adoption: Event-triggered compute (like AWS Lambda) used for flexible scaling and cost efficiency.

⸻

⚙️ 5. Platform Engineering & DevEx
	•	Internal Developer Platforms (IDPs): Centralized tooling for software teams (Backstage, Humanitec, Port).
	•	Golden Paths: Predefined safe development practices and templates to reduce cognitive load.
	•	GitOps & Automation: Declarative infrastructure management using tools like ArgoCD and Flux.

⸻

📊 6. Real-Time Data and Observability
	•	Streaming over Batch: Kafka, Flink, and Pulsar power low-latency pipelines.
	•	AI Observability: Monitoring LLMs for drift, hallucination, and cost.
	•	Unified Data Fabric: Blending data lakes, warehouses, and real-time streams for better insights.

⸻

📱 7. Human-Tech Interaction Focus
	•	Spatial Computing: Apple Vision Pro and Meta Quest push the boundaries of XR.
	•	Voice & Multimodal Interfaces: Interfaces now respond to voice, image, video, and text input.
	•	Digital Twins & Simulation: Used in manufacturing, logistics, and smart cities to test scenarios virtually.

⸻

📉 8. Cost Optimization and Sustainable Tech
	•	Green IT: Carbon-aware software deployment, server utilization efficiency, and sustainable data centers.
	•	FinOps Culture: Real-time cloud spend tracking and shared accountability between engineering and finance.

⸻

If you’re looking for a strategy brief for a company or leadership presentation, I can format this as a 1-pager, slide, or executive summary. Would you like that?