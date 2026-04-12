subjects = []
study_time = []

for i in range(4):
    sub = input("Enter subject name: ")
    diff = int(input("Enter difficulty (0-10): "))

    if 0 <= diff <= 4:
        hours = 2
    elif 5 <= diff <= 8:
        hours = 4
    elif 9 <= diff <= 10:
        hours = 6
    else:
        hours = 2

    subjects.append(sub)
    study_time.append(hours)

print("\n--- STUDY PLAN ---")
for i in range(len(subjects)):
    print(subjects[i]} "->" study_time[i], "hours/day")
