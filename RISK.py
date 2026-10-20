#what age is equaly likely to cause fatal crash as a 16yr old driver
#plot data and find associated curve to answer this

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

age_ranges = ["16-19", "20-24", "25-29", "30-34", 
        "35-39", "40-44", "45-49", "50-54", "55-59",
        "60-64", "65-69", "70-74", "75-79", "80-84",
        "85+"]

range_low = np.array([16, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
             80, 85])
range_length = np.array([4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5])

deaths_per_VMT = [3.29, 2.07, 1.15, 0.84, 0.85, 0.79, 0.82, 0.77, 0.86,
                  0.83, 1.03, 1.45, 2.63, 4.52, 11.12]

data = pd.DataFrame({"Ages": age_ranges, "deaths_per_VMT":deaths_per_VMT})


print(data)


data["midpoint"] = range_low + 0.5 * range_length

def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

x = data["midpoint"]
y = data["deaths_per_VMT"]

params, _ = curve_fit(quadratic, x, y)
a, b, c = params

##print(f"Fitted curve: y = {a:.5f}x^2 + {b:.3f}x + {c:.3f}") ##dont need this right now


target_value = quadratic(16, a, b, c)   # the y-value that equals 16
c_adjusted = c - target_value #adjust c so when quadratic is solved has zeros of 16, x

numerator = -b +np.sqrt(b**2 - 4*a*(c_adjusted))
denominator = 2*a
terminal_age_quadratic = math.floor(numerator / denominator)

print("Fitting with a quadratic: ", terminal_age_quadratic) #age which has same fatality rate as legal age to drive (16)


x_smooth = np.linspace(16, 90, 200)
y_smooth = quadratic(x_smooth, a, b, c)

quad_r2_score = r2_score(y, quadratic(x, a, b, c))
print("R2 scored for quadratic", quad_r2_score)


plt.scatter(x, y, color='red', label="Actual data")
plt.plot(x_smooth, y_smooth, label="Fitted quadratic")
plt.xlabel("Age (midpoint)")
plt.ylabel("Fatalities per 100 million VMT")
plt.axhline(target_value, color='green', linestyle='--', label=f"y at age 16 ({target_value:.2f})")
plt.legend()
plt.show()

## quadratic barely fits the curve
## lets try polynomial of degree n

poly_deg = 6

coeffs = np.polyfit(x, y, deg=poly_deg)
poly = np.poly1d(coeffs)

target_value = poly(16)

roots = (poly - target_value).roots
real_roots = roots[np.isreal(roots)].real


other_roots = real_roots[~np.isclose(real_roots, 16)]
if len(other_roots) > 0 :
    terminal_age_quartic = None if len(other_roots == 0 ) else math.floor(other_roots[0])
    print("Fitting with a polynomial of degree n:", terminal_age_quartic)
else : 
    print("No other root")
    terminal_age_quartic = None


x_smooth = np.linspace(16, 90, 200)
y_smooth = poly(x_smooth)


quart_r2_score = r2_score(y, poly(x))
print("R2 score for polynomial of degree n: ", quart_r2_score)

plt.scatter(x, y, color='red')
plt.plot(x_smooth, y_smooth)
plt.xlabel("Age (midpoint)")
plt.ylabel("Fatalities per 100 million VMT")
plt.axhline(target_value, color='green', linestyle='--', label=f"y at age 16 ({target_value:.2f})")
plt.legend()
plt.show()


##calculating expected fatalites
##Total VMT from this year is about 3.03 trillion or 3.03 * 10^12
total_vmt_2023 = 3.03e12   # total miles driven nationally

# Each age bracket's share of that VMT, using your original data's percentages
pct_vmt = np.array([3.60, 7.60, 9.70, 11.80, 12.30, 13.10, 10.40, 9.80,
                     6.40, 5.10, 3.60, 2.60, 1.70, 0.07, 0.20]) / 100

data["pct_vmt"] = pct_vmt
data["vmt_miles"] = data["pct_vmt"] * total_vmt_2023 ##VMT per age group
## for fatalities, must divide deaths per VMT by 100 million then multiply by miles
data["expected_fatalities"] = (data["deaths_per_VMT"] / 1e8) * data["vmt_miles"]

data["expected_fatalities_floor"] = np.floor(data["expected_fatalities"]).astype(int)

print(data[["Ages", "deaths_per_VMT", "expected_fatalities_floor"]])

print(f"\nQuadratic model answer: age {terminal_age_quadratic}")
print(f"Higher degree (n = {poly_deg}) model answer: age {math.floor(other_roots[0]) if len(other_roots) else 'none found'}")
