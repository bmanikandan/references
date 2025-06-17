The team raised concerns that we hadn’t configured the correct Helm Chart version. The SVM team had introduced group node permissions and released a new Helm Chart version. However, even after testing with the provided version, it didn’t work as expected.

Kye resolved the issue on the fly and published another release today. Despite that, the ISTIO-PROXY container failed to start again—this time due to a memory out-of-exception. We increased the memory allocation from 1GB to 2GB, which allowed the application to deploy successfully. All services are now back to operational.
