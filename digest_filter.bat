@echo off
rem An example list of filters to remove all not important/successful events from a log digest
rem Run with input and output file names
grep -v -E ",.?(ProfileTable refresh time|entry|Log statements for PMR|Entry|Date,Time|Refreshing|adding|Empty|requestID .*? completed successfully|message is outbound|Session ID from SOAP Message|Session id.*set in the message context|using global|using Orphan|.*OU=Hidden|.*=SUCCESSFUL|Processed data collected|Refreshing schema|###|.* successful|0 disallowed|SvcID=|session ID in Handler on the return path)" %1 > %2
