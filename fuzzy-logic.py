import xlrd
import xlwt
import matplotlib.pyplot as plt


class student:
    def __init__(self, index, degree):
        self.index = index
        self.degree = degree


def trapezoid_set(x, a, b, c, d):
    if x <= a or x >= d:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x <= c:
        return 1
    elif c <= x <= d:
        return -(x - d) / (d - c)

# ========= Bulanıklaştırma =========
def fuzzification_income(income):
    low_income = trapezoid_set(income, float('-inf'), 0, 2, 6)
    medium_income = trapezoid_set(income, 2, 6, 8, 12)
    high_income = trapezoid_set(income, 8, 12, 14, 18)
    very_high_income = trapezoid_set(income, 14, 18, float('inf'), float('inf'))
    return low_income, medium_income, high_income, very_high_income


def fuzzification_outcome(outcome):
    low_outcome = trapezoid_set(outcome, float('-inf'), 0, 2, 3)
    medium_outcome = trapezoid_set(outcome, 2, 3, 7, 8)
    high_outcome = trapezoid_set(outcome, 7, 8, float('inf'), float('inf'))
    return low_outcome, medium_outcome, high_outcome


def inference(income, outcome):
    low_inc, med_inc, high_inc, vhigh_inc = fuzzification_income(income)
    low_out, med_out, high_out = fuzzification_outcome(outcome)
    high = [0]
    low = [0]

    if low_inc > 0 and low_out > 0:
        high.append(min(low_inc, low_out))
    if low_inc > 0 and med_out > 0:
        high.append(min(low_inc, med_out))
    if low_inc > 0 and high_out > 0:
        high.append(min(low_inc, high_out))

    if med_inc > 0 and low_out > 0:
        low.append(min(med_inc, low_out))
    if med_inc > 0 and med_out > 0:
        low.append(min(med_inc, med_out))
    if med_inc > 0 and high_out > 0:
        high.append(min(med_inc, high_out))

    if high_inc > 0 and low_out > 0:
        low.append(min(high_inc, low_out))
    if high_inc > 0 and med_out > 0:
        low.append(min(high_inc, med_out))
    if high_inc > 0 and high_out > 0:
        low.append(min(high_inc, high_out))

    if vhigh_inc > 0 and low_out > 0:
        low.append(min(vhigh_inc, low_out))
    if vhigh_inc > 0 and med_out > 0:
        low.append(min(vhigh_inc, med_out))
    if vhigh_inc > 0 and high_out > 0:
        low.append(min(vhigh_inc, high_out))

    return max(low), max(high)


# ========= Durulaştırma =========
def defuzzyfication(income, outcome):
    low, high = inference(income, outcome)
    y = (40 * low + 80 * high) / (low + high)
    return y


# ============= Gelir Üyelik Fonksiyonu ==================
low_income_set = [0, 2, 6]
low_income_degree = [1, 1, 0]

med_income_set = [2, 6, 8, 12]
med_income_degree = [0, 1, 1, 0]

high_income_set = [8, 12, 14, 18]
high_income_degree = [0, 1, 1, 0]

vhigh_income_set = [14, 18, 20]
vhigh_income_degree = [0, 1, 1]

plot1 = plt.figure(1)
plt.ylabel('µ(x)')
plt.xlabel('Gelir')
plt.plot(low_income_set, low_income_degree, label="Düşük")
plt.plot(med_income_set, med_income_degree, label="Orta")
plt.plot(high_income_set, high_income_degree, label="Yüksek")
plt.plot(vhigh_income_set, vhigh_income_degree, label="Çok Yüksek")
plt.legend()

# ============== Gider Üyelik Fonksiyonu ==================
low_outcome_set = [0, 2, 3]
low_outcome_degree = [1, 1, 0]

med_outcome_set = [2, 3, 7, 8]
med_outcome_degree = [0, 1, 1, 0]

high_outcome_set = [7, 8, 12]
high_outcome_degree = [0, 1, 1]

plot2 = plt.figure(2)
plt.ylabel('µ(x)')
plt.xlabel('Gider')
plt.plot(low_outcome_set, low_outcome_degree, label="Düşük")
plt.plot(med_outcome_set, med_outcome_degree, label="Orta")
plt.plot(high_outcome_set, high_outcome_degree, label="Yüksek")
plt.legend()

# ============== Uygunluk Üyelik Fonksiyonu ==============
plot3 = plt.figure(3)
ax = plot3.add_axes([0, 0, 1, 1])
ax.bar([1, 40, 80, 100], [0, 1, 1, 0])
plt.ylabel("µ(x)")
plt.xlabel('Uygunluk')
plt.show()

# ===================== XLS Dosya Okuma =====================
workbook = xlrd.open_workbook("Student.xls")
worksheet = workbook.sheet_by_index(0)
data = []
for i in range(1, worksheet.nrows):
    income = worksheet.cell_value(i, 1)
    outcome = worksheet.cell_value(i, 2)
    std = student(i, defuzzyfication(income, outcome))
    data.append(std)

data.sort(key=lambda x: x.degree, reverse=True)

# ===================== XLS Dosyaya Yazma =====================
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('Sonuc')
for i in range(0, 20):
    sheet.write(i, 0, data[i].index)

workbook.save('Result.xls')
