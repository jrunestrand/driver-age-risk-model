# What age should driving be capped in the US?

## Question
It is a widely known fact that older drivers oftentimes are not fit to drive, but there is no cap on age. Why? People in the US eligbile for a license until 16 because their brains are not fully developed and the risk is too high. This short project aims to find the age at which drivers are equally as risky as 16, with the implication that any age past that should not be driving.

## Data
- **Source:** FHWA Highway Statistics, Table NHTS-12.3.1 — https://www.fhwa.dot.gov/policyinformation/statistics/2007/nhts1231.cfm
- Published 2007, based on the 2001 National Household Travel Survey combined with NHTSA FARS fatality data
- Metric: driver fatalities per 100 million vehicle-miles traveled (VMT), broken out by driver age bracket
- **Limitation:** this specific age-bucketed table does not appear to have a more recently published equivalent. National fatality rates have declined since 2007 (the 2023 national rate is 1.26 per 100M VMT), so the absolute values here likely run somewhat high relative to current reality. However, the takeaway should be about the pattern, since it is unlikely that older drivers have improved drastically compared to younger ones.

## Method
1. Split each age bracket into a numeric midpoint (accounting for the first bracket being 4 years wide vs. 5 years for the rest)
2. Fit a quadratic curve to fatality rate vs. age — R² = 0.775132401964177
   - Poor fit: since the data is asymmetric, parabola does not fit well
   - Regardless, the parabola results in an equal risk age of 77
3. Fit a degree-6 polynomial — R² = 0.996341333204572
   - Substantially better fit
   - Resulted in a equal risk age of 81
4. Solved algebraically for the non-trivial root where each model's curve returns the same fatality rate as age 16
5. Weighted each age bracket's per-mile rate by its share of national VMT to estimate the expected annual fatalities per group

## Findings
- Quadratic model: age 77 has an equivalent per-mile fatality rate to a 16-year-old
- Degree-6 polynomial model: age  81
- Total Fatalities — Although the 85+ cateogory has by far the highest ratio of fatalities per mile driven, 20 - 24 year old still cause the most fatalities overall. This is becasue while older drivers are much worse, they drive much less

## Limitations & next steps
- Single variable model only based on age, a truly actuarial model would factor in other vairables
- This project theoretically proposes an age cap based purely on quantatifying data from one study. There are many more factors to consider and other ways to go about reducing these fatalities (drivers test every 5 years starting at 65, etc)