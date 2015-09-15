# ISIM log abridgement

This code creates a digest in a CSV format for an ISIM log file that is makes it more human-readable than the original format.
It retains the critical info and dumps extaneous fillers.

## Using
Get python 2.7 and run

`python digest_itim_log.py <trace.log|msg.log>`

The output will be saved with a "_digest.csv" suffix