import csv
import datetime


# Извлекает часы из строки
def get_hour(str):
    return str.split(":")[0]


# Вычисляет среднее
def mean(arr, len):
    return sum(arr) / len


# Вычисляет дисперсию
def dispersion(arr, len):
    return sum((xi - mean(arr, len)) ** 2 for xi in arr) / len


def count_in_three_days(data, days):
    array = {}
    i = 0
    while True:
        if (not (data[i][0] == days[0])) and (not (data[i][0] == days[1])) and (not (data[i][0] == days[2])):
            break
        if not data[i][0] + " " + get_hour(data[i][1]) in array.keys():
            array[data[i][0] + " " + get_hour(data[i][1])] = 1
        else:
            array[data[i][0] + " " + get_hour(data[i][1])] += 1
        i = i + 1
    return array


def count_in_month(data):
    array = {}
    i = 0
    while not i == len(data):
        if data[i][0] not in array.keys():
            array[data[i][0]] = 1
        else:
            array[data[i][0]] = array[data[i][0]] + 1
        i = i + 1
    return array


def on_day(data, str):
    array = {}
    i = 0
    while not i == len(data):
        year, month, day = data[i][0].split("-")
        if datetime.date(int(year), int(month), int(day)).strftime("%A") == str:
            if data[i][0] not in array.keys():
                array[data[i][0]] = 1
            else:
                array[data[i][0]] = array[data[i][0]] + 1
        i = i + 1
    return array


def by_week(data):
    array = {}
    i = 0
    while not i == len(data):
        year, month, day = data[i][0].split("-")
        week = datetime.date(int(year), int(month), int(day)).strftime("%V")
        if not week in array.keys():
            array[week] = 1
        else:
            array[week] += 1
        i = i + 1
    return array


def by_months(data):
    array = {}
    i = 0
    while not i == len(data):
        year, month, day = data[i][0].split("-")
        temp = year + "-" + month
        if temp not in array.keys():
            array[temp] = 1
        else:
            array[temp] = array[temp] + 1
        i = i + 1
    return array


april = []
march = []
may = []
all = []
with open("ddd.csv", "r", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        year_month = row[0].split(" ")
        all.append(year_month)
        if "2020-04" in row[0]:
            april.append(year_month)
        if "2020-03" in row[0]:
            march.append(year_month)м
        if "2020-05" in row[0]:
            may.append(year_month)

days = ['2020-04-01', '2020-04-02', '2020-04-03']

stat = count_in_three_days(april, days)
print("in_three_days: ", stat)
print("mean: ", mean(stat.values(), 72))
print("var: ", dispersion(stat.values(), 72))
print("\n")

stat1 = count_in_month(april)
print("by_month: ", stat1)
print("mean: ", mean(stat1.values(), 31) / 24)
print("var: ", dispersion(stat1.values(), 31) / 24)
print("\n")

stat2 = on_day(march + april + may, 'Monday')
print("on_monday: ", stat2)
print("mean: ", mean(stat2.values(), 13) / 24)
print("var: ", dispersion(stat2.values(), 13) / 24)
print("\n")

stat2 = on_day(march + april + may, 'Tuesday')
print("Tuesday: ", stat2)
print("mean: ", mean(stat2.values(), 13) / 24)
print("var: ", dispersion(stat2.values(), 13) / 24)
print("\n")

stat2 = on_day(march + april + may, 'Wednesday')
print("Wednesday: ", stat2)
print("mean: ", mean(stat2.values(), 13) / 24)
print("var: ", dispersion(stat2.values(), 13) / 24)
print("\n")

stat2 = on_day(march + april + may, 'Thursday')
print("Thursday: ", stat2)
print("mean: ", mean(stat2.values(), 13) / 24)
print("var: ", dispersion(stat2.values(), 13) / 24)
print("\n")

stat2 = on_day(march + april + may, 'Friday')
print("Friday: ", stat2)
print("mean: ", mean(stat2.values(), 13) / 24)
print("var: ", dispersion(stat2.values(), 13) / 24)
print("\n")

stat2 = on_day(march + april + may, 'Saturday')
print("Saturday: ", stat2)
print("mean: ", mean(stat2.values(), 13) / 24)
print("var: ", dispersion(stat2.values(), 13) / 24)
print("\n")

stat3 = on_day(march + april + may, 'Sunday')
print("on_Sunday: ", stat3)
print("mean: ", mean(stat3.values(), 13) / 24)
print("var: ", dispersion(stat3.values(), 13) / 24)
print("\n")

stat4 = by_week(march + april + may)
print("by week: ", stat4)
print("mean: ", mean(stat4.values(), 14) / 7 / 24)
print("var: ", dispersion(stat4.values(), 14) / 7 / 24)
print("\n")

stat5 = by_months(all)
print("by moths in all data: ", stat5)
print("mean: ", mean(stat5.values(), 17) / 30 / 24)
print("var: ", dispersion(stat5.values(), 17) / 30 / 24)
print("\n")
