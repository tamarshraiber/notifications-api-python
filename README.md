# Notification delivery API

A small HTTP API that manages and delivers notifications across email, SMS, and push channels.

## Install

```
pip install -r requirements.txt
```

A virtual environment is optional but recommended (`python -m venv .venv` then activate).

## Run

```
python src/main.py
```

Starts the HTTP server on port 3000.

NOTE: The server pre-populates in-memory storage with a few sample notifications on startup.

## Endpoints

### POST /notifications

Create a notification.

```
curl -X POST http://localhost:3000/notifications \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello","targetChannels":[{"type":"email","value":"user@example.com"}]}'
```

### GET /notifications

List all notifications.

```
curl http://localhost:3000/notifications
```

### GET /notifications/:id

Fetch a single notification by id. Returns 404 if not found.

```
curl http://localhost:3000/notifications/1
```

### PUT /notifications/:id

Update a notification. Returns 404 if not found.

```
curl -X PUT http://localhost:3000/notifications/1 \
  -H "Content-Type: application/json" \
  -d '{"message":"Updated message"}'
```

### POST /notifications/:id/send

Send a single notification. Returns 404 if not found.

```
curl -X POST http://localhost:3000/notifications/1/send
```

### POST /notifications/send-bulk

Send all pending notifications.

```
curl -X POST http://localhost:3000/notifications/send-bulk
```




# What did I improve?

### Architecture:
I divided the project into clear layers so that the code would be more readable and clear, understandable and easy to expand:
**Models layer:**
Notification class
**Repository layer:**
Responsible for storing the data to separate the data from the logic
**Service layer:**
Responsible for the business logic of the system
**Utilities layer:**
Helper functions that were separated into separate files:
<u> processor-</u> responsible for the logic of sending messages
<u> seed-</u> generates initial data
<u> segmenter-</u> helper functions for calculating data (dedup, SMS segments, tests, etc.)

### Validation and correctness:
I added input checks to make sure that valid inputs are entered and not empty inputs:
message check
target_channels check
type/value check
allowed types check
Update status by sending

### Exception management:
Separation between common error types: ValueError, not found, Exception
to send clear messages to the user about the exception, to prevent that the server will crash and to separate types of exceptions

### Tools used:
GitHubCopilot, ChatGPT, Gemini, Poastman

I not only improved the structure of the system but also its entire flow of sending messages, including validation, sending, error handling and status management.

