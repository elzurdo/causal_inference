import streamlit as st

import numpy as np
import pandas as pd


# import matplotlib.pyplot as plt
# from pywaffle import Waffle

try:
    import daft
except:
    daft = None

paradox_mode = "Paradox Explained"
standard_mode = "Random Control Trial"
diy_mode = "TL;DR"

system_mode = st.sidebar.radio('Mode', [paradox_mode, standard_mode, diy_mode])

f""" 
## Simpson's *"Paradox"*
**This classic problem of data interpretation is an excellent example to learn about causal analysis.**
"""


if diy_mode != system_mode:
    f"(For a less verbose version of the demo use the ***{diy_mode}*** mode by using the radio button on the left sidebar.)"
else:
    f"(For a verbose version of the demo use the ***{paradox_mode}*** mode by using the radio button on the left sidebar.)"



text_intro = \
f"""
There is an interesting numerical quirk that may arise in an analysis, where 
 results of a population contradict with those of subpopulations.  

For example, imagine that you are analysing the recovery rate of a drug, where
patients are separated to treatment and control groups. 

You find that males treatment group performs better than the male control group, and 
you reach a similar conclusion for the females.  Curiously, though, when you aggregate all the results you get the exact opposite finding!

Here you'll examine tables containing mock results to better understand 
the problem ... and its solution. Along the way you will learn about confounding factors 
and how to adjust for them in the context of causal analysis.

This is an interactive demo! You might find it useful to play around with numbers to solidify your understanding.
Feel free throughout to play with the dials on the left. 

For the full explanation continue in the current ***{paradox_mode}*** mode and later you will 
be suggested to use the ***{standard_mode}*** mode.  
"""

if diy_mode != system_mode:
    text_intro



# --- default values ---
treatments_default = 100
male_frac_default = 0.5  # Gender split
success_rate_default = 0.7

male_treatment_frac_paradox = 0.2
male_treatment_success_rate_paradox = 0.8
female_treatment_success_rate_paradox = 0.4


treatments = np.int(st.sidebar.number_input('Treatments:', format="%d", value=treatments_default))
controls = np.int(st.sidebar.number_input('Controls:', format="%d", value=treatments))

show_derivation = st.sidebar.checkbox('Show full derivations')

people = treatments + controls


if  diy_mode == system_mode:
    min_male_ratio = 0.1
    males_frac = st.sidebar.slider(f"male fraction (of {people})",
                                   min_value=min_male_ratio,
                                   max_value=1. - min_male_ratio, step=0.01,
                                   value=male_frac_default)
else:
    males_frac = male_frac_default
females_frac = 1. - males_frac

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
if diy_mode == system_mode:
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



rd_population = (male_treatment_success + female_treatment_success)/ treatments -  (male_control_success + female_control_success)/controls

ace = male_treatment_success / males_treatment * males_frac + female_treatment_success / females_treatment * (1. - males_frac)
ace -= male_control_success / males_control * males_frac + female_control_success / females_control * (1. - males_frac)

equation_rd = r'''
$$P(\text{recovery=True}|\text{treatment}) - P(\text{recovery=True}|\text{control})$$
'''
# equation_rd += f" = {rd_population:0.2f}"

right_arrow = r'''$\rightarrow$'''

f"""
In the following mock table we track patient recovery rates for a population of {people:,} split into to groups:   
* {treatments:,}  who receive treatment and 
* {controls:,} who do not (control)

We also have gender information with a total of {males:,} males and {females:,} females.  
(Feel free to update the values by using the widgets on the left sidebar.)  
"""

df

f"""
We will use the *Risk Difference* to describe recovery success rates, defined as:  
{equation_rd},  
where | symbolises *conditioned on* (in our case conditioned on a subsample of each group in turn).
"""

text_males_females_verbose_results = \
f"""
For each gender we calculate the recovery rates and Risk Differences:    
* males: {male_treatment_r * 100:0.1f}% for treatment and {male_control_r * 100:0.1f}% for control {right_arrow} **{(male_treatment_r-male_control_r)*100.:0.1f}%** difference
* females: {female_treatment_r * 100:0.1f}% for treatment and {female_control_r * 100:0.1f}% for control {right_arrow} **{(female_treatment_r-female_control_r)*100.:0.1f}%** difference

"""

text_population_verbose_rd_results = \
f"""
If we join all the results together, however, we obtain a negative Risk Difference of **{rd_population * 100:0.1f}**%! 
"""

rd_males = male_treatment_success / males_treatment - male_control_success / males_control
rd_females = female_treatment_success / females_treatment - female_control_success / females_control

equation_numerical_male = f"{male_treatment_success}/{males_treatment} - {male_control_success}/{males_control}"
equation_numerical_male += f"= {male_treatment_success / males_treatment:0.2f} - {male_control_success / males_control:0.2f}"
equation_numerical_male += f"= {rd_males:0.2f}"

equation_numerical_female = f"{female_treatment_success}/{females_treatment} - {female_control_success}/{females_control}"
equation_numerical_female += f"= {female_treatment_success / females_treatment:0.2f} - {female_control_success / females_control:0.2f}"
equation_numerical_female += f"= {rd_females:0.2f}"

equation_numerical = f"({male_treatment_success} + {female_treatment_success})/({treatments}) - ({male_control_success} + {female_control_success})/({controls})"
equation_numerical += f"= \n{(male_treatment_success + female_treatment_success)/ treatments:0.2f} - {(male_control_success + female_control_success)/controls:0.2f}"
equation_numerical += f"= {rd_population:0.2f}"

equation_ace_using_rd = r"$$RD_{\text{male}} P(\text{male}) + RD_{\text{female}} P(\text{female})$$"

ace_equation_numerical = f"{rd_males:0.2f}*{males_frac:0.2f} + {rd_females:0.2f}*{females_frac:0.2f}"
ace_equation_numerical += f"= {rd_males * males_frac + rd_females * females_frac:0.2f}"

if diy_mode != system_mode:
    text_males_females_verbose_results

    if show_derivation:
        "Risk Difference derivations"
        st.latex("Males := " + equation_numerical_male)
        st.latex("Females := " + equation_numerical_female)

    text_population_verbose_rd_results

    if show_derivation:
        st.latex("Population := " + equation_numerical)

else:
    """
    To adjust for the Gender confounding factor we use the *Average Causal Effect* defined as:
    """

    equation_ace_using_rd


    "Risk Difference:"
    st.latex("Males := " + equation_numerical_male)
    st.latex("Females := " + equation_numerical_female)
    st.latex("Population := " + equation_numerical)
    """
    Average Causal Effect :  
    """
    st.latex("Population := " + ace_equation_numerical)


text_rd_explanation = \
f"""
In other words  
* The treatment of males improves the recovery rate by an absolute {(male_treatment_r-male_control_r)*100.:0.1f}%
* The treatment of females improves the recovery rate by an absolute {(female_treatment_r-female_control_r)*100.:0.1f}%
* The treatment of everyone **reduces** the recovery rate by an absolute {np.abs(rd_population) * 100:0.1f}%

Clearly this last statement does not make sense!  

This is the essence of the paradox. 

The solution? Like any magician will tell you, it's about perception ... 
Let's see what we are missing. 

*Suggestion*: Play with the **Controls** values on the left to see how the values change,
while the conclusion remains that same.   

For your convenience here is the same data and results:
"""

if diy_mode != system_mode:
    text_rd_explanation

    df






f"""
---
## The Problem: Confounding Factors 

Upon an examination look you'll notice two interesting aspects:
* Uneven distributions of the genders amongst the treatment and control groups.
* Even though males and females have the same Risk Difference each group has a different success rate.

The first point is the crucial one to understanding the difference between our scenario 
to what is common practice in *Random Control Trials* (RCT), which are considered the golden 
standard for quantifying the utility of a treatment.    

Whereas in a RCT, if we suspect different rates of recovery from a demographic, e.g, in 
our case gender, we would expect a 50% split in the distribution of participants.  

E.g, we would expect in the treatment to be {int(treatments/2):} males and {int(treatments/2)} females, 
and in the control group to be {int(controls/2)} males and {int(controls/2)} females.  

But in our case we see that:  
In the treatment group there are {males_treatment:,} males and {females_treatment:,} females.  
In the control group there are {males_control:,} males and {females_control:,} females.

This means that being assigned treatment or control depends on the gender.  

If we draw a *Graphical Model* where nodes are parameters and vertices are their relationships, 
we should expect the following:  
"""



# --- Graphical model approahch
if daft:
    pgm = daft.PGM(aspect=1.2, node_unit=1.75)
    pgm.add_node("gender", r"Gender", 3, 3)
    pgm.add_node("group", r"Group", 2, 2)
    pgm.add_node("outcome", r"Outcome", 4, 2)
    pgm.add_edge("gender", "group")
    pgm.add_edge("gender", "outcome")
    pgm.add_edge("group", "outcome")
    pgm.render()
    st.pyplot(pgm)

f"""
The vertices have arrows indicating causality. The arrow from *Gender* to *Group* signifies that group assignment depends on the gender.  (Note that a robot that specialises in correlations would not know how to decide the direction, 
this is domain expertise that we contribute to the model. We will discuss this top further later on.)

There are two more arrows pointing towards *Recovery*. We know the direction because the Recovery 
 (true or false) cannot determine on's gender or if they were given a treatment. (Again, this sort of statement sounds trivial 
in layman terms, but in terms of modelling it is a power device to go beyond correlations to learn about causal efects.)

If we agree that this is our model, it is clear that Gender is a confounding factor. 
The recovery success depends both on gender and the group assigned, where the group 
assignment depends on gender.   

Now that we know that Gender is a confounding factor, we can use this information to 
solve for the apparent paradox.  

---

## The Solution: Adjusting For Confounding Factors

Our problem was that we did not regard confounding effects of the Gender parameter which 
determines (probabilistically) Group and the Outcome. The solution to this is standard 
stratification. 

We already know:

RD Males = {equation_numerical_male}  
RD Females = {equation_numerical_female} 
 

What we have done here may be thought of as changing our original graphic model 
 to a similar one but without an arrow from Gender to Group, i.e, the group assignment 
 no longer depends on one's gender. This is what we would expect from a Random Control Trial.
"""

if daft:
    pgm = daft.PGM(aspect=1.2, node_unit=1.75)
    pgm.add_node("gender", r"Gender", 3, 3)
    pgm.add_node("group", r"Group", 2, 2)
    pgm.add_node("outcome", r"Outcome", 4, 2)
    pgm.add_edge("gender", "outcome")
    pgm.add_edge("group", "outcome")
    pgm.render()
    st.pyplot(pgm)



"""

For later:   
It is important to note here that we applied our common sense, and hence subjectivity. 
A robot, e.g, would examine the relationships between the groups selection (treatment or control) 
and gender (male or female) and would conclude that they are correlated. As causation, 
that required an expert drawing an arrow on the vertex between the nodes.


Here we see that *Recovery* depends both on *Treatment* **and** on *Gender*.  
What makes *Gender* and confounding factor is the fact that *Treatment* depends on 
*Gender*, too. 



"""

equation_gender = r'''RD Stratum = 
$$P(\text{recovery}|\text{treatment, stratum}) - P(\text{recovery}|\text{control, stratum})$$
'''

equation_ace = r"$$ACE = P(\text{recovery}|do(\text{treatment})) - P(\text{recovery}|do(\text{control}))$$"
equation_ace += f"={ace:0.2f}"





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