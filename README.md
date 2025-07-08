https://www.elastic.co/search-labs/blog/elasticsearch-scoring-and-explain-api



Refer to this article on Elasticsearch’s scoring and explainability: Elasticsearch Scoring and Explain API – Elastic Search Labs.

Elasticsearch is highly suitable for search-driven use cases, fuzzy matching, and analytical queries. It leverages BM25 relevance scoring combined with multi-dimensional vector models. However, its effectiveness is inherently tied to the quality and structure of the underlying corpus, which may limit precision in more structured transactional domains.


Tempus currently uses Elasticsearch to expose data as a service, primarily for search and analytics. However, our use cases are not yet clearly defined or scoped with precision, which limits the strategic selection of the most appropriate storage and query layer.

⸻

Proposed Architectural Direction for Scepter – Globally Distributed Merchant Transactions

The initial architectural direction for Scepter was to adopt a Globally Distributed Database (GDD) to:
	•	Keep data geographically close to the merchant’s customers.
	•	Support internet-scale growth.
	•	Maintain ACID guarantees with eventual or strong consistency models across regions.

If interested, refer to Google’s foundational research on this topic:
📄 Google Spanner Research Paper – OSDI 2012