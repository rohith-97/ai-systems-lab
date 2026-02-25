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