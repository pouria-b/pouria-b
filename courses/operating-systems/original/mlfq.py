import matplotlib.pyplot as plt
import itertools

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.start_time = -1

def mlfq(processes, arrival_time, burst_time, quantum, context_switch):
    queue1 = []
    queue2 = []
    queue3 = []
    
    time = 0
    completed_processes = []
    process_list = [Process(processes[i], arrival_time[i], burst_time[i]) for i in range(len(processes))]
    gantt_chart = []

    def round_robin(queue, quantum):
        nonlocal time
        if queue:
            process = queue.pop(0)
            if process.start_time == -1:
                process.start_time = max(time, process.arrival_time)

            execute_time = min(process.remaining_time, quantum)
            gantt_chart.append((process.name, time, time + execute_time))
            time += execute_time
            process.remaining_time -= execute_time

            if process.remaining_time > 0:
                queue.append(process)
            else:
                process.completion_time = time
                completed_processes.append(process)

            # Add context switch
            gantt_chart.append(("CS", time, time + context_switch))
            time += context_switch

    def srtf(queue):
        nonlocal time
        queue.sort(key=lambda x: (x.remaining_time, x.arrival_time))
        if queue:
            process = queue.pop(0)
            if process.start_time == -1:
                process.start_time = max(time, process.arrival_time)

            execute_time = process.remaining_time
            gantt_chart.append((process.name, time, time + execute_time))
            time += execute_time
            process.remaining_time = 0
            process.completion_time = time
            completed_processes.append(process)

            # Add context switch
            gantt_chart.append(("CS", time, time + context_switch))
            time += context_switch

    def fcfs(queue):
        nonlocal time
        if queue:
            process = queue.pop(0)
            if process.start_time == -1:
                process.start_time = max(time, process.arrival_time)

            execute_time = process.remaining_time
            gantt_chart.append((process.name, time, time + execute_time))
            time += execute_time
            process.remaining_time = 0
            process.completion_time = time
            completed_processes.append(process)

            # Add context switch
            gantt_chart.append(("CS", time, time + context_switch))
            time += context_switch

    while len(completed_processes) < len(processes):
        for process in process_list:
            if process.arrival_time <= time and process not in queue1 and process not in queue2 and process not in queue3 and process not in completed_processes:
                queue1.append(process)

        if queue1:
            round_robin(queue1, quantum)
        elif queue2:
            srtf(queue2)
        elif queue3:
            fcfs(queue3)
        else:
            time += 1

        for process in queue1[:]:
            if process.remaining_time <= quantum:
                queue1.remove(process)
                queue2.append(process)

        for process in queue2[:]:
            if process.remaining_time <= 0:
                queue2.remove(process)
                queue3.append(process)

    for process in completed_processes:
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time

    print("Process\tArrival\tBurst\tCompletion\tTurnaround\tWaiting")
    for process in process_list:
        print(f"{process.name}\t\t{process.arrival_time}\t\t{process.burst_time}\t\t{process.completion_time}\t\t{process.turnaround_time}\t\t{process.waiting_time}")

    draw_gantt_chart(gantt_chart)

def draw_gantt_chart(gantt_chart):
    fig, ax = plt.subplots(figsize=(12, 6))

    # Generate distinct colors for processes
    process_colors = itertools.cycle(["skyblue", "lightgreen", "gold", "violet", "lightcoral", "orange"])
    color_map = {}

    labels_in_legend = set()

    for process_name, start, end in gantt_chart:
        if process_name == "CS":
            if "Context Switch" not in labels_in_legend:
                ax.barh("Gantt Chart", end - start, left=start, color="red", edgecolor="black", label="Context Switch")
                labels_in_legend.add("Context Switch")
            else:
                ax.barh("Gantt Chart", end - start, left=start, color="red", edgecolor="black")
        else:
            if process_name not in color_map:
                color_map[process_name] = next(process_colors)
            if process_name not in labels_in_legend:
                ax.barh("Gantt Chart", end - start, left=start, color=color_map[process_name], edgecolor="black", label=process_name)
                labels_in_legend.add(process_name)
            else:
                ax.barh("Gantt Chart", end - start, left=start, color=color_map[process_name], edgecolor="black")

    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    ax.set_title("Gantt Chart with Context Switches")
    ax.legend()
    plt.show()

# Test input
processes = ['P1', 'P2', 'P3', 'P4']
arrival_time = [1, 7, 9, 25]
burst_time = [6, 10, 2, 3]
quantum = 5
context_switch = 2

mlfq(processes, arrival_time, burst_time, quantum, context_switch)
