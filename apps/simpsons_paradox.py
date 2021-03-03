import streamlit as st

import numpy as np
import pandas as pd


import matplotlib.pyplot as plt
from pywaffle import Waffle


import daft


paradox_mode = "Paradox"
standard_mode = "Standard"
diy_mode = "Do it yourself!"

system_mode = st.sidebar.radio('Mode', [paradox_mode, standard_mode, diy_mode])

system_mode


""" 
---



## Simpon's *"Paradox"*

[description of the paradox]

There is an interesting numerical quirk that may arise in an analysis, where 
the results for a population appears to differ substantially than its subsets.  

For example, imagine that you are analysing the recovery rate of a treatment, where
patients are separated to treatment and control groups. 

You find that for the male participants the treatment group performs better than the control. Analysing the females you have the a similar finding.  But when you aggregate all the results you get the exact opposite finding!

Let's examine the following table containing mock results to better understand 
the problem ... and its solution!
"""


# --- default values ---
treatments_default = 100
male_frac_default = 0.5  # Gender split
success_rate_default = 0.7

male_treatment_frac_paradox = 0.2
male_treatment_success_rate_paradox = 0.8
female_treatment_success_rate_paradox = 0.4

if "Do it yourself!" == system_mode:
    treatments = np.int(st.sidebar.number_input('Treatments:', format="%d", value=treatments_default))
    controls = np.int(st.sidebar.number_input('Controls:', format="%d", value=treatments))

else:
    treatments = treatments_default
    controls = treatments

people = treatments + controls


if  "Do it yourself!" == system_mode:
    min_male_ratio = 0.1
    males_frac = st.sidebar.slider(f"male fraction (of {people})",
                                   min_value=min_male_ratio,
                                   max_value=1. - min_male_ratio, step=0.01,
                                   value=male_frac_default)
else:
    males_frac = male_frac_default

males = np.int(people * males_frac)
females = people - males


# --- Treatment split by gender ---
if  diy_mode == system_mode:
    males_treatment_frac = st.sidebar.slider(f"males fraction of treatment ({treatments:,})", min_value=min_male_ratio, max_value=1. - min_male_ratio, step=0.01, value=male_frac_default)
elif paradox_mode == system_mode:
    males_treatment_frac = male_treatment_frac_paradox
else:
    males_treatment_frac = male_frac_default

males_treatment = np.int(treatments * males_treatment_frac)
females_treatment = treatments - males_treatment

males_control = males - males_treatment
females_control = females - females_treatment


# fig = plt.figure(
#     FigureClass=Waffle,
#     rows=5,
#     columns=10,  # Either rows or columns could be omitted
#     values=[30, 16, 4]
# )
# st.pyplot(fig)

# --- Treatment success rates ---
if "Do it yourself!" == system_mode:
    min_success_rate = 0.1

    male_treatment_r = st.sidebar.slider("male treatment success rate", min_value=min_success_rate, max_value=1. - min_success_rate, step=0.01, value=success_rate_default)
    male_control_r   = st.sidebar.slider("male control   success rate", min_value=min_success_rate, max_value=1. - min_success_rate, step=0.01, value=success_rate_default - 0.1)

    female_treatment_r = st.sidebar.slider("female treatment success rate", min_value=min_success_rate, max_value=1. - min_success_rate, step=0.01, value=success_rate_default)
    female_control_r   = st.sidebar.slider("female control   success rate", min_value=min_success_rate, max_value=1. - min_success_rate, step=0.01, value=success_rate_default - 0.1)

elif paradox_mode == system_mode:
    male_treatment_r = male_treatment_success_rate_paradox
    male_control_r = male_treatment_r - 0.1

    female_treatment_r = female_treatment_success_rate_paradox
    female_control_r = female_treatment_r - 0.1
else:
    male_treatment_r = success_rate_default
    male_control_r = male_treatment_r - 0.1

    female_treatment_r = success_rate_default
    female_control_r = female_treatment_r - 0.1

# --- All Data ---


male_treatment_success = np.int(male_treatment_r * males_treatment)
male_control_success   = np.int(male_control_r   * males_control)
female_treatment_success = np.int(female_treatment_r * females_treatment)
female_control_success   = np.int(female_control_r   * females_control)


male_treatment_failure = males_treatment - male_treatment_success
male_control_failure   = males_control   - male_control_success
female_treatment_failure = females_treatment - female_treatment_success
female_control_failure   = females_control   - female_control_success

df = \
pd.DataFrame({0: [male_treatment_success, male_control_success, "male", True], 
              1: [male_treatment_failure, male_control_failure, "male", False],
              2: [female_treatment_success, female_control_success, "female", True],
              3: [female_treatment_failure, female_control_failure, "female", False]
             }, 
             index=["treatment", "control", "gender","recovered"]).T

df


f"""
In this mock sample we have a total population of {people:,} split into {treatments:,}  
who receive treatment and {controls:,} who do not (control). 

We also have a gender information with a total of {males:,} males and {females:,}
"""

rd_population = (male_treatment_success + female_treatment_success)/ treatments -  (male_control_success + female_control_success)/controls

ace = male_treatment_success / males_treatment * males_frac + female_treatment_success / females_treatment * (1. - males_frac)
ace -= male_control_success / males_control * males_frac + female_control_success / females_control * (1. - males_frac)

show_derivation = st.checkbox('Show derivation')

"Risk Difference of the full population:"
equation = r'''RD Population = 
$$P(\text{recovery}|\text{treatment}) - P(\text{recovery}|\text{control})$$
'''

equation += f" = {rd_population:0.2f}"

equation

equation_numerical = f"Population := ({male_treatment_success} + {female_treatment_success})/({treatments}) - ({male_control_success} + {female_control_success})/({controls})"
equation_numerical += f"= \n{(male_treatment_success + female_treatment_success)/ treatments:0.2f} - {(male_control_success + female_control_success)/controls:0.2f}"
equation_numerical += f"= {rd_population:0.2f}"

if show_derivation:
	equation_numerical


equation_gender = r'''RD Stratum = 
$$P(\text{recovery}|\text{treatment, stratum}) - P(\text{recovery}|\text{control, stratum})$$
'''

equation_gender

equation_numerical_male = f"RD Males = {male_treatment_success}/{males_treatment} - {male_control_success}/{males_control}"
equation_numerical_male += f"= {male_treatment_success/males_treatment:0.2f} - {male_control_success/males_control:0.2f}"
equation_numerical_male += f"= {male_treatment_success/males_treatment - male_control_success/males_control:0.2f}"

equation_numerical_male

equation_numerical_female = f"RD Females = {female_treatment_success}/{females_treatment} - {female_control_success}/{females_control}"
equation_numerical_female += f"= {female_treatment_success/females_treatment:0.2f} - {female_control_success/females_control:0.2f}"
equation_numerical_female += f"= {female_treatment_success/females_treatment - female_control_success/females_control:0.2f}"

equation_numerical_female

equation_ace = r"$$ACE = P(\text{recovery}|do(\text{treatment})) - P(\text{recovery}|do(\text{control}))$$"
equation_ace += f"={ace:0.2f}"
equation_ace

equation_ace_drivation = r"$$= P(\text{recovery}|\text{treatment, male})P(\text{male}) + P(\text{recovery}|\text{treatment, female})P(\text{female})$$"
equation_ace_drivation +=  r"$$- \left( P(\text{recovery}|\text{control, male})P(\text{male}) + P(\text{recovery}|\text{control, female})P(\text{female}) \right)$$"


equation_ace_numerical =  f"={male_treatment_success}/{males_treatment}" + r"$$\times$$"  + f"{males}/{people}"
equation_ace_numerical += f" + {female_treatment_success}/{females_treatment}" + r"$$\times$$"  + f"{females}/{people}"
equation_ace_numerical +=  f" - ({male_control_success}/{males_control}" + r"$$\times$$"  + f"{males}/{people}"
equation_ace_numerical +=  f" {female_control_success}/{females_control}" + r"$$\times$$"  + f"{females}/{people})"
equation_ace_numerical += f"={ace:0.2f}"


if show_derivation:
	equation_ace_drivation

	equation_ace_numerical


f"""
The solution lies in the fact that we have:  
* uneven distributions of the genders amongst treatment and control
* different success rates between the genders  

In the treatment group there are {males_treatment:,} males and {females_treatment:,} and 
the complementary {males_control:,} males, {females_control:,} females in the control group


adjustment ...
"""

# --- Graphical model approahch  

pgm = daft.PGM(aspect=1.2, node_unit=1.75)
pgm.add_node("cloudy", r"Gender", 3, 3)
pgm.add_node("rain", r"Treatment", 2, 2)
pgm.add_node("sprinkler", r"Recovery", 4, 2)
pgm.add_edge("cloudy", "rain")
pgm.add_edge("cloudy", "sprinkler")
pgm.add_edge("rain", "sprinkler")
pgm.render()
st.pyplot(pgm)

"""
Note that this tutorial is aimed to be interactive and hence you can change the results to explore different outcomes. 
"""

# --- More info ---

text_gateway = """
# Simpson's Paradox: A Gateway To Causal Inference


Correlation does not imply causation. 
It turns out, however, that with some simple ingenious tricks one can unveil causal relationships within standard observational data, 
without having to resort to expensive random control trials. 

A simple example of this is the Simpson's Paradox demonstrated here.
This is a classical problem of data interpretation. 
Understanding its solution is a gateway to realise that causality, at times, may be as simple as one or two lines of code. 

In this tutorial you will learn some basic concepts of causal inference  
demonstrating in an accessible manner using visualisations and data manipulations with `pandas`.

The objective is to show that with relatively minimal investment anyone can add causal inference to their toolbox to get more out of their data.
"""

expander_gateway = st.beta_expander("Simpson's Paradox: A Gateway To Causal Inference" )
expander_gateway.write(text_gateway)


text = """
![](https://upload.wikimedia.org/wikipedia/en/d/de/Edward_H._Simpson.jpg)

> Edward Hugh Simpson CB (10 December 1922 – 5 February 2019) was a British codebreaker, statistician and civil servant. He was introduced to the thinking of mathematical statistics as a cryptanalyst at Bletchley Park (1942–45).   [Wikipedia](https://en.wikipedia.org/wiki/Edward_H._Simpson)
"""


expander = st.beta_expander("Who was Simpson?")
expander.write(text)