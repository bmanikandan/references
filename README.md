Initially, we thought that we would adopt the Arrays approach. The primary reasons that made us to stay away from the arrays approach are outlined below, so you can see why we made our decision.

Arrays approach

This data type corresponds to a Java data structure of List<PayFacFee>
   Allows duplicate entries to be entered. The applications that write data into the Fee collection always ensure that they write extra logic in order to prevent duplicate entries from being entered.
   When a card is being searched, one must iterate over the entire collection when the complexity notation is expressed in O(N), which is big O-time.
   In the absence of proper handling, it can lead to a potentially error-prone state.


Key-Value pattern advantages
Corresponding data stature in Java is Map<String, PayFacFee>
1.    Atomically prevent duplicates by construct, so there is no need to write extra logic in order to prevent duplicate entries from occurring.
2.    The complexity of the lookup time in big O notation is O(1).
3.    Despite its clean appearance, the set is well-structured and free of errors. It is scalable horizontally and vertically.
4. 
