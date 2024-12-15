import time

# Initialize variables to keep track of time
start = None
elapsed = 0

# Function to start the stopwatch
def start_time():
    global start
    if start is None:
        start = time.time()
    else:
        pass

# Function to stop the stopwatch
def stop_time():
    global start, elapsed
    if start is not None:
        elapsed += time.time() - start
        start = None
    else:
        pass

# Function to reset the stopwatch
def reset_time():
    global start, elapsed
    start = None
    elapsed = 0

# Function to get the current elapsed time
def get_elapsed_time():
    global start, elapsed
    if start is not None:
        return elapsed + (time.time() - start)
    return elapsed

