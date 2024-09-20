It exposes APIs that allow merchants to submit evidence from their side. The Scepter program allows merchants to electronically submit evidence that is clear and accurate to defend themselves against a chargeback dispute raised by the cardholder's financial institution in response to a chargeback dispute. This kind of electronic evidence must be presented within 21 days of the date on which the request for a chargeback was made. Supported documents are either in the form of an office document or an image or a PDF document.

It should be noted that Scepter is still waiting to receive the list of supported document formats and the max file size from Tempus, so the list should be available shortly.

Since the exposed set of APIs are related to the app-dispute-api functionality, due to the high memory consumption and files system 1/0 operations involved, this functionality has been separated out as a separate microservice in order to reduce memory consumption.

The following are some of the known evidences.
  Receipts or contracts that are signed
  A proof of service or delivery in the form of an invoice
﻿﻿A copy of a Terms of Service and Refund Policy
* ﻿﻿etc.
