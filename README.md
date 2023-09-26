In response to an error reported by Oracle 19c Database, the size of the Oracle Program global area (PGA) has been increased from 5GB to 8GB.
While researching, we found that only one instance of the Payee application had established a connection to Oracle, while all other instances were experiencing timeout problems and reporting 10 errors to Hikari. The reason for this is that the maxLifetime value was not shorter than the connection time limit imposed by the database infrastructure. The Payee application property file has been reduced from 30 minutes to 5 minutes.
(3) The OP load-balancer is not equally distributing traffic to all instances of the Payee application. The least-cost load-balance algorithm should distribute the load that has not happened. We therefore switched to Round-Robin algorithm and forced the traffic to be distributed to all running instances only for the Payee application.
4) The testing revealed that an existing Payment update query related to the Payee approval process was frequently timed out. We applied the temporary fix to relax the update condition based on the business approval in the application property settings.
Next release will include the permanent fix.
None of the above is noticeable or reproducible in the lower environment.


I am requesting your assistance in choosing an HTTP Status code for the Payment API.

Case 1: Http Status Code 400 - Payment CREATE syntax errors.
Case 2: Http Status Code 422 - For non-syntax errors, such as account frozen or insufficient funds to make the payment etc.

Case 1: A syntax error occurred when creating a payment using the HTTP status code 400.
2: HTTP Status Code 422 - For non-syntax errors, such as an account that has been frozen or insufficient funds available for the payment.

Internet article cataloged 422  as WebDAV and the 402 has been reserved for future use (payment required).
What HTTP Status Code should be used in the above case 2?