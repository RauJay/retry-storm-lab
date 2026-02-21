# Retry Storm Lab

This lab demonstrates how retries without exponential backoff can cause cascading failures.

## How to run
1. Click **Code → Codespaces → Create Codespace**
2. System boots automatically
3. Run load:


## What to observe
- Latency spikes
- Errors increase
- Retries amplify DB load

## Fix
Replace retries with exponential backoff and observe system stability.
