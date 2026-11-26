# Pipeline queue
## Diagnose backlog
When queue depth rises, compare the arrival rate with the worker completion rate over the same interval. Check the oldest message age and inspect worker errors before scaling consumers.
## Replay failed records
Replay a failed record using its original event identifier. Confirm the destination has one row for that identifier before replaying the remaining batch.
