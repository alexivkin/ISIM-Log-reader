# IBM Security Identity Manager log abridgement

This script creates a digest in a CSV format for an ISIM trace and msg log files that makes them more human-readable than the original format.
It retains the critical info and dumps extaneous fillers.

## Using
Get python 2.7 and run:

`python digest_itim_log.py <trace.log|msg.log>`

The output will be saved with a "_digest.csv" suffix to the same folder as the source. This script also works under jython 2.7 and jython standalone 2.7, but may need more heap than default because of the extensive regexps.

You can refine the digest further by filtering out standard events.

`digest_filter.bat trace_digest.log trace_important.log`

(you need Cygwin grep for this to work)
