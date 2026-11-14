import matplotlib.pyplot as plt
# Shortest Remaining Time First (SRTF)
processes = ['P1', 'P2', 'P3', 'P4']
arrival_time = [1, 7, 9, 25]
burst_time = [6, 10, 2, 3]
quantum = 5
context_switch = 2


remaining_burst_time = burst_time[:]
completion_time = [0] * len(processes)
current_time = 0
gantt_chart = []
turnaround_time = [0] * len(processes)
waiting_time = [0] * len(processes)

# اجرای الگوریتم 
while True:
    # انتخاب فرآیند با کوتاه‌ترین زمان باقی‌مانده که آماده است
    available_processes = [i for i in range(len(processes)) if arrival_time[i] <= current_time and remaining_burst_time[i] > 0]

    if not available_processes:
        if all(t == 0 for t in remaining_burst_time):
            break
        current_time += 1
        continue

    process_idx = min(available_processes, key=lambda x: remaining_burst_time[x])

    # اجرای فرآیند برای یک واحد زمان
    # هم میتونیم استفاده کنیم ولی quantum اینجا از 
    start_time = current_time
    current_time += 1
    remaining_burst_time[process_idx] -= 1

    # ثبت در گانت چارت
    #ترکیب بخش‌ های متوالی اجرای یک فرآیند
    if len(gantt_chart) > 0 and gantt_chart[-1][2] == processes[process_idx]:
        gantt_chart[-1] = (gantt_chart[-1][0], current_time, processes[process_idx]) #زمان پایان به‌روزرسانی می‌شود
    else:
        gantt_chart.append((start_time, current_time, processes[process_idx]))

    # اگر فرآیند کامل شده باشد
    if remaining_burst_time[process_idx] == 0:
        completion_time[process_idx] = current_time
        turnaround_time[process_idx] = completion_time[process_idx] - arrival_time[process_idx]
        waiting_time[process_idx] = turnaround_time[process_idx] - burst_time[process_idx]

    # افزودن زمان سوئیچ اگر فرآیندها باقی مانده باشند و تغییر فرآیند رخ دهد
    if any(t > 0 for t in remaining_burst_time):
        next_processes = [i for i in range(len(processes)) if arrival_time[i] <= current_time and remaining_burst_time[i] > 0]
        
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
ax.set_title("SRTF")
ax.set_xlim(0, current_time + 2)
plt.show()