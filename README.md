# IBM Security Identity Manager log abridgement

This script creates a digest in a CSV format for an ISIM trace and msg log files that makes them more human-readable than the original format.
It retains the critical info and dumps extaneous fillers.

## Using
Get python 2.7 and run:

`python digest_itim_log.py <trace.log|msg.log>`

The output will be saved with a "_digest.csv" suffix

You can refine the digest further by filtering out standard events

`digest_filter.bat trace_digest.log trace_important.log`
