# Retry Storm Lab

This lab demonstrates how **immediate retries under partial failure can cause cascading failure**
and how **exponential backoff stabilizes the system**.

The system is fully runnable online using **GitHub Codespaces** and can be torn down with one click.

---

##  What this lab simulates

- A service calling a **slow and flaky dependency**
- Immediate retries → **retry storm**
- Load amplification → **cascading failure**
- Exponential backoff → **stability**

A live UI visualizes:
- Requests/sec
- Retries/sec
- Average latency
- System state (CASCADING FAILURE vs STABLE)

---

## How to spin up the lab (online)

### Option 1: GitHub Codespaces (recommended)

1. Open this repository on GitHub
2. Click **Code → Codespaces → Create Codespace**
3. Wait for VS Code to open in the browser

Once VS Code opens, start the system:

```bash
docker compose up --build -d
