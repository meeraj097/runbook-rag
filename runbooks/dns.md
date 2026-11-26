# DNS resolution
## Compare resolvers
When a DNS lookup times out, query the same hostname against the configured resolver and a known working resolver. Record each response code and latency. A successful IP connection alongside a failed hostname lookup narrows the investigation to name resolution.
## Handover
Attach the query timestamp, affected site, resolver address and response code to the DNS incident. Repeat the original lookup after recovery.
