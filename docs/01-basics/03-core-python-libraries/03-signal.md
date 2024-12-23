# Signal module

- The **`signal`** module in Python provides a way to handle system signals, allowing you to execute custom code when specific signals are received by your program.
- Signals are asynchronous notifications sent to a process, often triggered by external events or user actions (e.g., pressing `Ctrl+C`).

---

## Basic Usage

!!! info "Signals"
    - Signals are identified by constants like `signal.SIGINT`, `signal.SIGTERM`, etc.
    - `SIGINT` is sent when you press `Ctrl+C`.
    - `SIGTERM` is sent to terminate a program (e.g., via `kill` command).

!!! info "Handlers"
    - You can register a custom function (signal handler) to be executed when a specific signal is received.
    - Use `signal.signal(signal_name, handler_function)` to register a handler.

---

## Handling `SIGINT` (Ctrl+C)

```python
import signal
import time

def handle_sigint(signum, frame):
    print(f"Received signal {signum}. Exiting gracefully!")
    exit(0)

# Register the handler for SIGINT
signal.signal(signal.SIGINT, handle_sigint)

print("Running program. Press Ctrl+C to interrupt.")
while True:
    time.sleep(1)
```

**Output when you press `Ctrl+C`:**

```txt
Running program. Press Ctrl+C to interrupt.
Received signal 2. Exiting gracefully!
```

---

## Handling `SIGTERM`

```python
import signal
import time

def handle_sigterm(signum, frame):
    print("Received SIGTERM. Cleaning up resources...")
    exit(0)

# Register the handler for SIGTERM
signal.signal(signal.SIGTERM, handle_sigterm)

print("Running program. Use 'kill -15 <PID>' to terminate.")
while True:
    time.sleep(1)
```

**Output when sending `SIGTERM`:**

```txt
Received SIGTERM. Cleaning up resources...
```

---

## Ignoring Signals

You can ignore specific signals by setting their handler to `signal.SIG_IGN`:

```python
import signal
import time

# Ignore SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal.SIG_IGN)

print("Try pressing Ctrl+C. It will be ignored.")
time.sleep(10)
print("Program finished.")
```

**Output:**

```txt
Try pressing Ctrl+C. It will be ignored.
Program finished.
```

---

## Restoring Default Behavior

You can restore the default behavior for a signal using `signal.SIG_DFL`:

```python
import signal
import time

def custom_handler(signum, frame):
    print("Custom handler for SIGINT!")

# Set custom handler
signal.signal(signal.SIGINT, custom_handler)

print("Press Ctrl+C to trigger the custom handler.")
time.sleep(5)

# Restore default behavior
signal.signal(signal.SIGINT, signal.SIG_DFL)
print("Default behavior restored. Press Ctrl+C again.")
time.sleep(5)
```

**Output:**

```txt
Press Ctrl+C to trigger the custom handler.
Custom handler for SIGINT!
Default behavior restored. Press Ctrl+C again.
# Exits program on second Ctrl+C
```

---

## Using `signal.alarm`

You can set an alarm to send a `SIGALRM` signal after a specific time:

```python
import signal
import time

def handle_alarm(signum, frame):
    print("Alarm triggered!")

# Register handler and set alarm
signal.signal(signal.SIGALRM, handle_alarm)
signal.alarm(5)  # Trigger SIGALRM after 5 seconds

print("Waiting for alarm...")
time.sleep(10)
```

**Output after 5 seconds:**

```txt
Waiting for alarm...
Alarm triggered!
```

---

## Key Points to Remember

1. **Signals**
> Signals are used for asynchronous events like interrupts or termination requests.

2. **Handlers**
> Register handlers using `signal.signal(signal_name, handler_function)`.
>
> Handlers must accept two arguments: `signum` (signal number) and `frame` (current stack frame).

3. **Special Constants**
> `signal.SIG_IGN`: Ignore the signal.
> 
> `signal.SIG_DFL`: Restore the default behavior.

4. **Common Signals**
> `SIGINT`: Interrupt (Ctrl+C).
> 
> `SIGTERM`: Termination request.
> 
> `SIGALRM`: Alarm timer expiration.

---

## Summary

!!! info ""
    - The `signal` module provides fine-grained control over how your Python program responds to external signals.
    - You can customize behavior for interrupts (`Ctrl+C`), termination requests, or other signals, making it ideal for building robust, interactive, and cleanup-aware applications.
