Concerns on CAP Team’s Kafka Adoption Strategy

Good morning,

The CAP Team appears to be moving toward adopting Kafka, based on the assumption that it inherently brings speed improvements for both asynchronous and synchronous payment flows. However, this direction raises concerns, as it seems to be more of a technical debt path than a well-justified architectural decision.

There is also an expectation for CAP to generate trace IDs using random algorithms, which adds further unpredictability and complexity to observability and debugging.

While CAP maintains that “the business wants to use Kafka,” it seems this is largely being driven by a contractor who believes this is the best architecture. Unfortunately, this vision is being justified by leveraging business input rather than technical alignment. The hardest part is that we currently lack a knowledgeable representative at PNC who can challenge or guide this direction, ensuring it aligns with what PNC truly needs.
