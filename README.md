Thanks for taking the time to evaluate GraalM on a weekend, Vijay.
The following observations have been made based on the following link:
In the link provided there is a study report from Chronicle Queue, they have two versions of their queue product, one based on Java and one based on C++. JDK and GraalVM queue products were evaluated using JIT rather than AOT.

The primary focus of our work is on ahead-of-time compilation (AOT) to native images, that is, Java to platform-specific native images, in which case the application will communicate with bare-metal hardware.