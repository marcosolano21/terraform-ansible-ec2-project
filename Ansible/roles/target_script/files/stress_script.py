import time
import multiprocessing
import random
import sys

def cpu_stress_worker(shared_cpu_target):
    """Worker that executes the workload loop based on the dynamic target."""
    window_interval = 0.1
    while True:
        target_pct = shared_cpu_target.value / 100.0
        work_time = window_interval * target_pct
        sleep_time = window_interval * (1.0 - target_pct)

        start_time = time.time()
        while time.time() - start_time < work_time:
            _ = 12345 * 67890

        if sleep_time > 0:
            time.sleep(sleep_time)

if __name__ == "__main__":
    print("--- CHAOTIC SIMULATOR STARTED BY ANSIBLE HANDLER ---", flush=True)

    num_cores = multiprocessing.cpu_count()
    shared_cpu_target = multiprocessing.Value('d', 30.0)  # Initial baseline: 30% CPU utilization.

    processes = []
    for i in range(num_cores):
        p = multiprocessing.Process(target=cpu_stress_worker, args=(shared_cpu_target,), name=f"Core-{i}")
        p.start()
        processes.append(p)

    ram_holder = []
    
    # State variables for the random walk.
    base_cpu = 40.0
    base_ram = 300  # initial MB
    spike_duration = 0  # Cycle counter for traffic spikes.

    try:
        while True:
            # ¿Are we currently experiencing a massive traffic spike?
            if spike_duration > 0:
                spike_duration -= 1
                # High values simulating a temporary overload.
                target_cpu_base = random.uniform(85.0, 95.0)
                target_ram_base = random.randint(550, 650)  # Safe for small EC2 instances.
                if spike_duration == 0:
                    print(" [EVENT] The traffic burst has ended. Returning to normal operation.", flush=True)
            else:
                # 4% chance of a sudden traffic spike occurring
                if random.random() < 0.04:
                    print(" [EVENT] Alert! Sudden traffic spike detected.", flush=True)
                    spike_duration = random.randint(6, 15)  # Will run for 12 to 30 seconds
                    target_cpu_base = random.uniform(85.0, 95.0)
                    target_ram_base = random.randint(550, 650)
                else:
                        # Normal traffic: Random Walk.
                        # The baseline CPU usage randomly drifts on each cycle within the range [-5%, +5%].
                    base_cpu += random.uniform(-5.0, 5.0)
                    base_cpu = max(20.0, min(70.0, base_cpu))  # Límites normales
                    target_cpu_base = base_cpu

                    # RAM usage randomly drifts within the range [-25 MB, +25 MB].
                    base_ram += random.randint(-25, 25)
                    base_ram = max(150, min(450, base_ram))  # Límites normales
                    target_ram_base = base_ram

            # Add high-frequency white noise (jitter) to make the graph appear realistic and less smooth.
            final_cpu = target_cpu_base + random.uniform(-3.0, 3.0)
            final_cpu = max(5.0, min(98.0, final_cpu))  # Enforce the hardware's absolute resource limits.
            shared_cpu_target.value = final_cpu

            final_ram = int(target_ram_base + random.randint(-15, 15))
            final_ram = max(100, min(700, final_ram))

            # Adjust the actual physical RAM allocation on the EC2 instance.
            current_allocated_ram = len(ram_holder)
            if current_allocated_ram < final_ram:
                for _ in range(final_ram - current_allocated_ram):
                    ram_holder.append(b"x" * (1024 * 1024))
            elif current_allocated_ram > final_ram:
                for _ in range(current_allocated_ram - final_ram):
                    if ram_holder:
                        ram_holder.pop()

            print(f"[Current state] Actual -> CPU: {final_cpu:.1f}% | RAM: {len(ram_holder)} MB | Mode: {' PEAK' if spike_duration > 0 else 'Normal'}", flush=True)
            time.sleep(2) 

    except KeyboardInterrupt:
        print("\nStopping the chaotic simulator....", flush=True)
        for p in processes:
            p.terminate()