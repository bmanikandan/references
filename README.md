This is a deployment strategy and it has nothing to do with fetching retail entitlements in any way. A single pod is used by the retail to bundle all SFP APIs and BFF APIs together.

In the end, BFF calls the SFP API using HTTPS regardless of whether it is bubbled in a single pod or outside single pod.