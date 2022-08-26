# V1 - UK Index error analysis

Problem: V1 of this index described two different ways of calculating the composite IMD. The UK wide index should have just used the employment information for comparison because the NI income data is incomparable. The GB index could use both. 

Due to an error (a typo of "UK" vs "uk") in the generation script, the income and employment information was used for both. As the NI information was incomparable, this led to SOAs in Northern Ireland being ranked as much less deprived than using the correct method. The GB-only index was unaffected by this problem. 

3479 (8%) of small areas have their population decile changed by this error. The following table shows the shift in decile by nation of moving from v1 (incorrect method) to v2 (correct method).

This change affects almost all NI SOA position and the scale of the change is greater - with a reasonable proportion moving more than 1 decile. 
In aggregate, the change affects more LSOA/DZ in other parts of the country - but the scale of the change is smaller, with all movement within one decile. 






| nation | -3 | -2 | -1 | 1 | 2 | 3 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| E | 0 | 0 | 489 | 718 | 0 | 0 |
| N | 19 | 306 | 386 | 12 | 1 | 1 |
| S | 0 | 0 | 178 | 389 | 0 | 0 |
| W | 0 | 0 | 0 | 980 | 0 | 0 |





# Actions taken

* Error in generation script fixed, and aggregate analysis in readme file rerun.
* As this error was found as part of upgrading to a new versioned data structure, the scale of the change is reflected in a major version bump to V2. 
* The original plan was to maintain old URLs for the data files - instead I've broken those links to encourage any external users hotlinking to the file to come back to the repo, and get the up-to-date data.
