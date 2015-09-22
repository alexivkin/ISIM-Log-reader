@echo off
rem A list of filters to remove all not important/successful events from a log digest
rem run with input and output file names
grep -v -E ",.?(adding|Empty|requestID|using global|using Orphan|.*OU=Hidden|.*SUCCESSFUL|Failed first char|Failed numeric test|Processed data collected|Refreshing schema|###|.*successful|0 disallowed|SvcID=)" %1 > %2