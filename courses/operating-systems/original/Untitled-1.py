import matplotlib.pyplot as plt
import random


def fcfs_scheduling(processes, arrival_time, burst_time, context_switch):
    start_time = []
    end_time = []
    completion_time = []
    turnaround_time = []
    waiting_time = []
    current_time = 0
    gantt_chart = []

    for i in range(len(processes)):
        if current_time < arrival_time[i]:  #ورودی حتما به ترتیب باشه 
            current_time = arrival_time[i]  # اگر CPU بیکار باشد زمان را جلو می‌بریم
        start_time.append(current_time)
        current_time += burst_time[i]
        end_time.append(current_time)
        completion_time.append(current_time)
        turnaround_time.append(completion_time[i] - arrival_time[i])
        waiting_time.append(turnaround_time[i] - burst_time[i])
        gantt_chart.append((start_time[-1], end_time[-1], processes[i]))

        # افزودن زمان سوئیچ، مگر اینکه فرآیند آخر باشد
        if i < len(processes) - 1:
            gantt_chart.append((current_time, current_time + context_switch, 'CS'))
            current_time += context_switch


    # چاپ جدول زمان‌بندی
    print("Process | Arrival | Burst | Completion | Turnaround | Waiting")
    for i in range(len(processes)):
        print(f"{processes[i]:>7} | {arrival_time[i]:>7} | {burst_time[i]:>5} | {completion_time[i]:>10} | {turnaround_time[i]:>10} | {waiting_time[i]:>7}")

    # # زمان‌های شروع، پایان و ترتیب فرایندها
    # for i in range(len(processes)):
    #     print(f"Process {processes[i]}: Start Time = {start_time[i]}, End Time = {end_time[i]}")

    # رسم گانت چارت
    fig, ax = plt.subplots(figsize=(12, len(processes) * 1))
    y_positions = range(len(gantt_chart))

    for idx, (start, end, label) in enumerate(gantt_chart):
        color = 'skyblue' if label != 'CS' else 'lightcoral'
        ax.barh(y_positions[idx], end - start, left=start, edgecolor='black', align='center', color=color)
        ax.text((start + end) / 2, y_positions[idx], label, ha='center', va='center', color='black', fontsize=10)

    ax.set_yticks(y_positions)
    ax.set_yticklabels([label for _, _, label in gantt_chart])
    ax.set_xlabel("Time")
    ax.set_title("FCFS")
    ax.set_xlim(0, max(end_time) + context_switch + 2)
    plt.show()

def round_robin_scheduling(processes, burst_time, arrival_time, quantum, context_switch):
    # کپی کردن زمان‌های ورود و اجرا
    remaining_burst_time = burst_time[:] # dc
    completion_time = [0] * len(processes)
    current_time = 0
    queue = []
    visited = [False] * len(processes)

    gantt_chart = []
    turnaround_time = [0] * len(processes)
    waiting_time = [0] * len(processes)

    # اجرای الگوریتم 
    while True:
        # اضافه کردن فرآیندهای جدید به صف
        for i in range(len(processes)):
            if arrival_time[i] <= current_time and not visited[i]:
                queue.append(i)
                visited[i] = True

        if not queue: 
            if all(t == 0 for t in remaining_burst_time):
                break
            current_time += 1
            continue

        process_idx = queue.pop(0)

        # اجرای فرآیند
        start_time = current_time
        exec_time = min(quantum, remaining_burst_time[process_idx]) 
        current_time += exec_time
        remaining_burst_time[process_idx] -= exec_time

        gantt_chart.append((start_time, current_time, processes[process_idx]))

        # اگر فرآیند کامل شده باشد
        if remaining_burst_time[process_idx] == 0:
            completion_time[process_idx] = current_time
            turnaround_time[process_idx] = completion_time[process_idx] - arrival_time[process_idx]
            waiting_time[process_idx] = turnaround_time[process_idx] - burst_time[process_idx]

        # افزودن زمان سوئیچ
        gantt_chart.append((current_time, current_time + context_switch, 'CS'))
        current_time += context_switch

        # اگر فرآیند کامل نشده باشد
        if remaining_burst_time[process_idx] != 0:
            # اضافه کردن فرآیندهای جدید به صف
            for i in range(len(processes)):
                if arrival_time[i] <= current_time and not visited[i]:
                    queue.append(i)
                    visited[i] = True
                    
            queue.append(process_idx)

    # چاپ جدول زمان‌بندی
    print("Process | Arrival | Burst | Completion | Turnaround | Waiting")
    for i in range(len(processes)):
        print(f"{processes[i]:>7} | {arrival_time[i]:>7} | {burst_time[i]:>5} | {completion_time[i]:>10} | {turnaround_time[i]:>10} | {waiting_time[i]:>7}")


    # رسم گانت چارت
    fig, ax = plt.subplots(figsize=(12, len(gantt_chart) * 0.5))
    y_positions = range(len(gantt_chart))

    for idx, (start, end, label) in enumerate(gantt_chart):
        color = 'skyblue' if label != 'CS' else 'lightcoral'
        ax.barh(y_positions[idx], end - start, left=start, edgecolor='black', align='center', color=color)
        ax.text((start + end) / 2, y_positions[idx], label, ha='center', va='center', color='black', fontsize=10)

    ax.set_yticks(y_positions)
    ax.set_yticklabels([label for _, _, label in gantt_chart])
    ax.set_xlabel("Time")
    ax.set_title("Round Robin")
    ax.set_xlim(0, current_time + 2)
    plt.show()

def spn_scheduling(processes, arrival_time, burst_time, context_switch):
    # Shortest Process Next (SPN)
    # کپی کردن زمان‌های ورود و اجرا
    remaining_burst_time = burst_time[:]
    completion_time = [0] * len(processes)
    current_time = 0
    gantt_chart = []
    turnaround_time = [0] * len(processes)
    waiting_time = [0] * len(processes)
    # visited = [False] * len(processes)

    # اجرای الگوریتم 
    while True:
        # انتخاب فرآیند با کوتاه‌ترین زمان اجرا که آماده است
        available_processes = [i for i in range(len(processes)) if arrival_time[i] <= current_time and remaining_burst_time[i] > 0]
        
        #جلو بردن زمان 
        if not available_processes:
            if all(t == 0 for t in remaining_burst_time):
                break
            current_time += 1
            continue

        process_idx = min(available_processes, key=lambda x: remaining_burst_time[x])

        # اجرای فرآیند
        start_time = current_time
        current_time += remaining_burst_time[process_idx]
        gantt_chart.append((start_time, current_time, processes[process_idx]))
        
        completion_time[process_idx] = current_time
        turnaround_time[process_idx] = completion_time[process_idx] - arrival_time[process_idx]
        waiting_time[process_idx] = turnaround_time[process_idx] - burst_time[process_idx]
        remaining_burst_time[process_idx] = 0

        # افزودن زمان سوبیچ اگر فرآیندها باقی مانده باشند
        if any(t > 0 for t in remaining_burst_time):
            gantt_chart.append((current_time, current_time + context_switch, 'CS'))
            current_time += context_switch

    # چاپ جدول زمان‌بندی
    print("Process | Arrival | Burst | Completion | Turnaround | Waiting")
    for i in range(len(processes)):
        print(f"{processes[i]:>7} | {arrival_time[i]:>7} | {burst_time[i]:>5} | {completion_time[i]:>10} | {turnaround_time[i]:>10} | {waiting_time[i]:>7}")


    # رسم گانت چارت
    fig, ax = plt.subplots(figsize=(12, len(gantt_chart) * 0.5))
    y_positions = range(len(gantt_chart))

    for idx, (start, end, label) in enumerate(gantt_chart):
        color = 'skyblue' if label != 'CS' else 'lightcoral'
        ax.barh(y_positions[idx], end - start, left=start, edgecolor='black', align='center', color=color)
        ax.text((start + end) / 2, y_positions[idx], label, ha='center', va='center', color='black', fontsize=10)

    ax.set_yticks(y_positions)
    ax.set_yticklabels([label for _, _, label in gantt_chart])
    ax.set_xlabel("Time")
    ax.set_title("SPN")
    ax.set_xlim(0, current_time + 2)
    plt.show()

def srtf_scheduling(processes, arrival_time, burst_time, quantum, context_switch):
    # Shortest Remaining Time First (SRTF)
    # کپی کردن زمان‌های ورود و اجرا
    remaining_burst_time = burst_time[:]
    completion_time = [0] * len(processes)
    current_time = 0
    gantt_chart = []
    turnaround_time = [0] * len(processes)
    waiting_time = [0] * len(processes)

    while True:
        # انتخاب فرآیندهایی که آماده اجرا هستند
        available_processes = [i for i in range(len(processes)) if arrival_time[i] <= current_time and remaining_burst_time[i] > 0]

        if not available_processes:
            if all(t == 0 for t in remaining_burst_time):
                break
            current_time += 1
            continue

        # انتخاب فرآیند با کوتاه‌ترین زمان باقی‌مانده
        process_idx = min(available_processes, key=lambda x: remaining_burst_time[x])

        # اجرای فرآیند با توجه به کوانتوم تایم
        start_time = current_time
        execution_time = min(quantum, remaining_burst_time[process_idx])  # اجرای محدود به کوانتوم یا زمان باقی‌مانده
        current_time += execution_time
        remaining_burst_time[process_idx] -= execution_time

        # ثبت در گانت چارت
        if len(gantt_chart) > 0 and gantt_chart[-1][2] == processes[process_idx]:
            gantt_chart[-1] = (gantt_chart[-1][0], current_time, processes[process_idx])
        else:
            gantt_chart.append((start_time, current_time, processes[process_idx]))

        # اگر فرآیند کامل شده باشد
        if remaining_burst_time[process_idx] == 0:
            completion_time[process_idx] = current_time
            turnaround_time[process_idx] = completion_time[process_idx] - arrival_time[process_idx]
            waiting_time[process_idx] = turnaround_time[process_idx] - burst_time[process_idx]

        # افزودن زمان سوئیچ
        if any(t > 0 for t in remaining_burst_time) and remaining_burst_time[process_idx] >= 0:
            gantt_chart.append((current_time, current_time + context_switch, 'CS'))
            current_time += context_switch

    # چاپ جدول زمان‌بندی
    print("Process | Arrival | Burst | Completion | Turnaround | Waiting")
    for i in range(len(processes)):
        print(f"{processes[i]:>7} | {arrival_time[i]:>7} | {burst_time[i]:>5} | {completion_time[i]:>10} | {turnaround_time[i]:>10} | {waiting_time[i]:>7}")

    # رسم گانت چارت
    fig, ax = plt.subplots(figsize=(12, len(gantt_chart) * 0.5))
    y_positions = range(len(gantt_chart))

    for idx, (start, end, label) in enumerate(gantt_chart):
        color = 'skyblue' if label != 'CS' else 'lightcoral'
        ax.barh(y_positions[idx], end - start, left=start, edgecolor='black', align='center', color=color)
        ax.text((start + end) / 2, y_positions[idx], label, ha='center', va='center', color='black', fontsize=10)

    ax.set_yticks(y_positions)
    ax.set_yticklabels([label for _, _, label in gantt_chart])
    ax.set_xlabel("Time")
    ax.set_title("SRTF with Quantum Time")
    ax.set_xlim(0, current_time + 2)
    plt.show()

def hrrn_scheduling(processes, arrival_time, burst_time, context_switch):
    # کپی کردن زمان‌های ورود و اجرا
    remaining_burst_time = burst_time[:]
    completion_time = [0] * len(processes)
    current_time = 0
    gantt_chart = []
    turnaround_time = [0] * len(processes)
    waiting_time = [0] * len(processes)
    # visited = [False] * len(processes)

    # اجرای الگوریتم 
    while True:
        # انتخاب فرآیند با بالاترین نسبت پاسخ که آماده است
        available_processes = [i for i in range(len(processes)) if arrival_time[i] <= current_time and remaining_burst_time[i] > 0]

        if not available_processes:
            if all(t == 0 for t in remaining_burst_time):
                break
            current_time += 1
            continue

        # محاسبه نسبت پاسخ برای هر فرآیند آماده
        response_ratios = {
            i: (current_time - arrival_time[i] + burst_time[i]) / burst_time[i] for i in available_processes
        }

        # انتخاب فرآیند با بالاترین نسبت پاسخ
        process_idx = max(response_ratios, key=response_ratios.get)

        # اجرای فرآیند
        start_time = current_time
        current_time += remaining_burst_time[process_idx]
        gantt_chart.append((start_time, current_time, processes[process_idx]))

        completion_time[process_idx] = current_time
        turnaround_time[process_idx] = completion_time[process_idx] - arrival_time[process_idx]
        waiting_time[process_idx] = turnaround_time[process_idx] - burst_time[process_idx]
        remaining_burst_time[process_idx] = 0

        # افزودن زمان سوئیچ اگر فرآیندها باقی مانده باشند
        if any(t > 0 for t in remaining_burst_time):
            gantt_chart.append((current_time, current_time + context_switch, 'CS'))
            current_time += context_switch

    # چاپ جدول زمان‌بندی
    print("Process | Arrival | Burst | Completion | Turnaround | Waiting")
    for i in range(len(processes)):
        print(f"{processes[i]:>7} | {arrival_time[i]:>7} | {burst_time[i]:>5} | {completion_time[i]:>10} | {turnaround_time[i]:>10} | {waiting_time[i]:>7}")

    # رسم گانت چارت
    fig, ax = plt.subplots(figsize=(12, len(gantt_chart) * 0.5))
    y_positions = range(len(gantt_chart))

    for idx, (start, end, label) in enumerate(gantt_chart):
        color = 'skyblue' if label != 'CS' else 'lightcoral'
        ax.barh(y_positions[idx], end - start, left=start, edgecolor='black', align='center', color=color)
        ax.text((start + end) / 2, y_positions[idx], label, ha='center', va='center', color='black', fontsize=10)

    ax.set_yticks(y_positions)
    ax.set_yticklabels([label for _, _, label in gantt_chart])
    ax.set_xlabel("Time")
    ax.set_title("HRRN")
    ax.set_xlim(0, current_time + 2)
    plt.show()

    





# نمونه ورودی
processes = ['P1', 'P2', 'P3', 'P4']
arrival_time = [1, 7, 9, 25]
burst_time = [6, 10, 2, 3]
quantum = 5
context_switch = 2

# print("\n--- FCFS Scheduling ---")
# fcfs_scheduling(processes, arrival_time, burst_time, context_switch)

print("\n--- Round Robin Scheduling ---")
round_robin_scheduling(processes, burst_time, arrival_time, quantum, context_switch)

# print("\n--- SJF Scheduling ---")
# spn_scheduling(processes, arrival_time, burst_time, context_switch)

# print("\n--- SRTF Scheduling ---")
# srtf_scheduling(processes, arrival_time, burst_time, quantum, context_switch)

# print("\n--- HRRN Scheduling ---")
# hrrn_scheduling(processes, arrival_time, burst_time, context_switch)