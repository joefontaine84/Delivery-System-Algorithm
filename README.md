<h1> Delivery-System-Algorithm </h1>

<h2>High-level Overview</h2>
This algorithm was designed to meet a very specific set of conditions where the ultimate goal was to have two (2) delivery trucks deliver all of their packages
while remaining under a combined total of 140 miles traveled. Moreover, the algorithm had to account for delayed package arrivals and incorrect package addresses being applied. A list of packages and
their associated notes/issues are provided in a CSV file within the repository. In addition, a separate CSV file in the repository contains the package locations. 

<br></br>

A modified nearest neighbor algorithm was selected to solve the provided problem. Some aspects of the algorithm include:
<ul>
  <li>Hash tables for enhanced algorithmic time complexity;</li>
  <li>Recursion for more efficient processing and reduction of human-entered code</li>
</ul>

A simple command-line interface was included with this application that checks the status of any package at select periods of time. 
