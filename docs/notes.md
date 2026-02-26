1. Why does async not help CPU-bound tasks?
    well cpu bound tasks are more heavy and math oriented, if there is no waiting, the thread is already busy, async has no use . but when you wait for a task to complerte and then you can do other chores, async comes into play.
    Async works via cooperative multitasking

    A coroutine only yields control when it hits await

    CPU-bound code has no await points

    So it blocks the event loop

    asyncio improves io concurrency, not cpu parallellism.

2. Why does ProcessPoolExecutor scale but ThreadPoolExecutor doesn’t for CPU?  
    its like 8 chefs has 8 knives and in another kitchen, 8 chefs share 1 knife. 
    Tradeoff:

    Processes cost more memory

    Inter-process communication overhead

    Serialization overhead (pickling)  

3. Why did semaphore=100 give near-perfect scaling?
    thread is constantly utilized. it just prevents overload.
    Async has extremely low scheduling overhead compared to OS threads.

4. If you remove semaphore limit entirely (1000 concurrent), what do you predict will happen?
    overload, memory pressure, increased latency, timeouts, possible crash.
    Connection pool exhaustion

    Open file descriptor limits

    Increased tail latency

5. If we change sleep to 1 second, what will async runtime become?
    runtime increases.     
    Runtime ≈ (1000 / concurrency) × latency
    Async doesn’t magically make latency disappear.
    It just overlaps waiting.



6. Memory scales with concurrency”

Correct — but why exactly?
When you created 1000 tasks:
Each task allocates:
A coroutine object
A Task wrapper
Stack frames
Future objects
References in gather
Internal state for scheduling
All of that sits in memory simultaneously.
Important nuance:
Memory usage scales with number of live coroutines, not just amount of work.
Even if each task “does nothing”, the task itself is an object graph.
That’s why high-concurrency servers must:
Limit in-flight requests
Use connection pools
Apply backpressure
This is production reality.   


7. The reason runtime didn’t increase:
Because sleep does not consume CPU.
So overlapping waiting hides latency.
Key correction:
Async overlaps waiting, it does not create CPU parallelism.


8. If each task did large JSON serialization

Now we’re getting interesting.
What happens?
CPU-bound work increases
GIL contention increases
Event loop blocks longer
Latency increases
Tail latency spikes
Throughput drops
Memory grows due to larger objects
Most importantly:
Serialization happens in Python space → GIL locked → no parallelism.
So async loses its advantage.
This is exactly why inference systems:
Offload heavy compute to C/CUDA
Use worker pools
Batch operations

9. If tasks = 50,000

Let’s be more mechanical:
You would see:
Massive memory growth
Increased GC cycles
Longer scheduling queues
Increased latency variance
Possible “too many open files”
Event loop lag
The system becomes unstable not because of CPU,
but because of scheduler pressure and memory overhead.
This is how production systems collapse.