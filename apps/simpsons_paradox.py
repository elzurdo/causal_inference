import streamlit as st

import numpy as np
import pandas as pd


# import matplotlib.pyplot as plt
# from pywaffle import Waffle

try:
    import daft
except:
    daft = None

paradox_mode = "Tutorial"
diy_mode = "TL;DR"

system_mode = st.sidebar.radio('Mode', [diy_mode, paradox_mode])

f""" 
## Simpson's *"Paradox"* - An Interactive Demo
**This classic problem of data interpretation is an excellent example to learn about causal analysis.**
"""

"""
> *Causation is not merely an aspect of statistics - it is an addition to statistics* - Judea Pearl
"""

if diy_mode != system_mode:
    alt_mode = str(diy_mode)
    verbosity_type = "less verbose"
    verbosity_prefix = ""
else:
    alt_mode = str(paradox_mode)
    verbosity_type = "verbose"
    verbosity_prefix = f"This **{diy_mode}** mode assumes that you are familiar with Simpson's Paradox and how it's resolved and are interested in testing the use case presented. "
f"({verbosity_prefix}For a {verbosity_type} version of the demo change to the ***{alt_mode}*** mode on the radio button in the left sidebar.)"



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

For the full explanation continue in the current ***{paradox_mode}*** mode.  
"""

if diy_mode != system_mode:
    text_intro

# --- default values ---
treatments_default = 1000
controls_default = treatments_default
male_frac_default = 0.5  # Gender split
success_rate_default = 0.7

male_treatment_frac_paradox = 0.2
male_treatment_success_rate_paradox = 0.8
female_treatment_success_rate_paradox = 0.4

if diy_mode == system_mode:
    show_derivation = False
else:
    show_derivation = st.sidebar.checkbox('Show full derivations')

treatments = np.int(st.sidebar.number_input('Treatments:', format="%d", value=treatments_default))
controls = np.int(st.sidebar.number_input('Controls:', format="%d", value=controls_default))

people = treatments + controls

min_male_ratio = 0.1
males_frac = st.sidebar.slider(f"male population fraction (i.e, of {people:,})",
                               min_value=min_male_ratio,
                               max_value=1. - min_male_ratio, step=0.01,
                               value=male_frac_default)

females_frac = 1. - males_frac
st.sidebar.write(f"{females_frac * 100.:0.1f}% of the population are females")
st.sidebar.write(f"{males_frac * 100.:0.1f}% of the population are males")

males = np.int(people * males_frac)
females = people - males


# --- Treatment split by gender ---
males_treatment_frac = st.sidebar.slider(f"male treatment fraction (i.e, of {treatments:,})", min_value=min_male_ratio, max_value=1. - min_male_ratio, step=0.01, value=male_treatment_frac_paradox)

males_treatment = np.int(treatments * males_treatment_frac)
females_treatment = treatments - males_treatment

st.sidebar.write(f"{(1. - males_treatment_frac) * 100.:0.1f}% of the treatment are females")
st.sidebar.write(f"{males_treatment_frac * 100.:0.1f}% of the treatment are males")


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
success_rate_control = st.sidebar.checkbox('Modify group success rates')

if success_rate_control:
    min_success_rate = 0.1

    male_treatment_r = st.sidebar.slider("male treatment success rate", min_value=min_success_rate, max_value=1. - min_success_rate, step=0.01, value=male_treatment_success_rate_paradox)
    male_control_r   = st.sidebar.slider("male control   success rate", min_value=min_success_rate, max_value=1. - min_success_rate, step=0.01, value=male_treatment_success_rate_paradox - 0.1)

    female_treatment_r = st.sidebar.slider("female treatment success rate", min_value=min_success_rate, max_value=1. - min_success_rate, step=0.01, value=female_treatment_success_rate_paradox)
    female_control_r   = st.sidebar.slider("female control   success rate", min_value=min_success_rate, max_value=1. - min_success_rate, step=0.01, value=female_treatment_success_rate_paradox - 0.1)

else:
    male_treatment_r = male_treatment_success_rate_paradox
    male_control_r = male_treatment_r - 0.1

    female_treatment_r = female_treatment_success_rate_paradox
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
             index=["group=treatment", "group=control", "gender","recovered"]).T



rd_population = (male_treatment_success + female_treatment_success)/ treatments -  (male_control_success + female_control_success)/controls

ace = male_treatment_success / males_treatment * males_frac + female_treatment_success / females_treatment * (1. - males_frac)
ace -= male_control_success / males_control * males_frac + female_control_success / females_control * (1. - males_frac)

equation_rd = r'''
$$RD =  P(\text{recovery=True}|\text{group=treatment}) - P(\text{recovery=True}|\text{group=control})$$
'''
# equation_rd += f" = {rd_population:0.2f}"

right_arrow = r'''$\rightarrow$'''

f"""
In the following mock table we track patient recovery rates for a population of {people:,} split into to two groups:   
* {treatments:,}  patients that receive treatment and 
* {controls:,} that do not (control)  

We also have gender information with a total of {males:,} males and {females:,} females.  

(*This is and interactive demo!*: on left sidebar you can update all values.)

"""

df

f"""
To assess performance of the treatment, we calculate the *Risk Difference* which compares the recovery success rates of the two groups, defined as:  
{equation_rd},  
where the pipe (|) symbolises *conditioned on* (in our case conditioned on group).
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
equation_numerical_male += f"= **{rd_males:0.2f}**"

equation_numerical_female = f"{female_treatment_success}/{females_treatment} - {female_control_success}/{females_control}"
equation_numerical_female += f"= {female_treatment_success / females_treatment:0.2f} - {female_control_success / females_control:0.2f}"
equation_numerical_female += f"= **{rd_females:0.2f}**"

equation_numerical = f"({male_treatment_success} + {female_treatment_success})/({treatments}) - ({male_control_success} + {female_control_success})/({controls})"
equation_numerical += f"= \n{(male_treatment_success + female_treatment_success)/ treatments:0.2f} - {(male_control_success + female_control_success)/controls:0.2f}"
equation_numerical += f"= **{rd_population:0.2f}**"

equation_ace_using_rd = r"$$ACE = \sum_\text{strata}RD_\text{stratum}P(\text{stratum}) = RD_{\text{male}} P(\text{male}) + RD_{\text{female}} P(\text{female})$$"

ace_equation_numerical = f"{rd_males:0.2f}*{males_frac:0.2f} + {rd_females:0.2f}*{females_frac:0.2f}"
ace_equation_numerical += f"= **{rd_males * males_frac + rd_females * females_frac:0.2f}**"

if diy_mode != system_mode:
    text_males_females_verbose_results

    if show_derivation:
        "Risk Difference derivations"
        st.write(r"$RD_\text{male}$ = " + equation_numerical_male)
        st.write(r"$RD_\text{female}$ = " + equation_numerical_female)

    text_population_verbose_rd_results

    if show_derivation:
        st.write(r"$RD_\text{population}$ = " + equation_numerical)

else:
    r"""
    Below we see that the sign of $RD_\text{population}$ contradicts with those of the genders.  
    To resolve this we adjust for the Gender confounding factor by calculating the *Average Causal Effect* defined as:
    """

    equation_ace_using_rd

    """
    
    """


    st.write(r"$RD_\text{male}$ = " + equation_numerical_male)
    st.write(r"$RD_\text{female}$ = " + equation_numerical_female)
    st.write(r"$RD_\text{population}$ = " + equation_numerical)
    st.write(r"$ACE_\text{population}$ = " + ace_equation_numerical)


text_rd_explanation = \
f"""
In other words  
* The treatment of males improves the recovery rate by an absolute {(male_treatment_r-male_control_r)*100.:0.1f}%
* The treatment of females improves the recovery rate by an absolute {(female_treatment_r-female_control_r)*100.:0.1f}%
* The treatment of everyone **reduces** the recovery rate by an absolute {np.abs(rd_population) * 100:0.1f}%

Clearly this last statement does not make sense!     
If the treatment helps males and females that means that it helps anyone regardless of if we know their gender.

This is the essence of the paradox. 

The solution? Like any magician will tell you, it's about perception ... 
Let's see what we are missing. 

*Suggestion*: Play with the **Controls** values on the left sidebar to see how the values change,
while the conclusion remains that same.   

"""

if diy_mode != system_mode:
    text_rd_explanation


""" 
*Challenge*: Try to guess what is required for the Population RD and ACE to agree. 
When ready modify the values on the left sidebar to see if you were correct!    
For your convenience here is the same data
"""

df


text_confounding = \
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
 
"""

if diy_mode != system_mode:
    text_confounding

# --- Graphical model approach

text_gender_to_group_rct = \
f"""
In the graph we see that Group variable **does not** depend on Gender. Males are {males_frac * 100:0.0f}% of the population as well as the groups. 
This means that we have Random Control Trial conditions. In RFC conditions you will also see that 
the Risk Difference of the population now equals that of their Average Causal Effect at {ace:0.2f}. 
*Suggestion:* Explore testing results by modifying ***male fraction*** and/or ***males fraction of treatment***.
"""

text_gender_to_group_non_rct = \
f"""
In the graph we see that Group depends on Gender because of an uneven split between 
the genders in the groups (males {males_frac * 100:0.0f}% of the population, while {males_treatment_frac * 100:0.0f}% of the treatment group). 
"""


rct_condition = males_treatment_frac == males_frac  # i.e, Random Control Trial Condition
gender_confounding = not ((male_treatment_r == female_treatment_r) & (male_control_r == female_control_r))


if not rct_condition:
    text_gender_to_group_non_rct = \
        f"""{text_gender_to_group_non_rct} *Suggestion:* set **males treatment fraction**=**males population fraction** to see what happens.
        """

if rct_condition == True:
    text_gender_to_group_edge = text_gender_to_group_rct
else:
    text_gender_to_group_edge = text_gender_to_group_non_rct


f"gender confounding: {gender_confounding}"


if daft:
    pgm = daft.PGM(aspect=1.2, node_unit=1.75)
    pgm.add_node("gender", r"Gender", 3, 3)
    pgm.add_node("group", r"Group", 2, 2)
    pgm.add_node("outcome", r"Outcome", 4, 2)
    if not rct_condition:
        pgm.add_edge("gender", "group")
    if gender_confounding:
        pgm.add_edge("gender", "outcome")
    pgm.add_edge("group", "outcome")
    pgm.render()

    """
    It is also convenient to represent the system in a *Graphical Model*.  
    Nodes are parameters and vertices are their relationships:
    """

    st.pyplot(pgm)





# The arrow from *Gender* to *Group* signifies that group assignment depends on the gender.  (Note that a robot that specialises in correlations would not know how to decide the direction,
# this is domain expertise that we contribute to the model. We will discuss this top further later on.)`

text_adjusting = \
f"""
The vertices have arrows indicating causality. 

{text_gender_to_group_edge}

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


if diy_mode:
    text_gender_to_group_edge

else:

    text_adjusting


    if daft:
        pgm = daft.PGM(aspect=1.2, node_unit=1.75)
        pgm.add_node("gender", r"Gender", 3, 3)
        pgm.add_node("group", r"Group", 2, 2)
        pgm.add_node("outcome", r"Outcome", 4, 2)
        pgm.add_edge("gender", "outcome")
        pgm.add_edge("group", "outcome")
        pgm.render()
        st.pyplot(pgm)


text_TODO= \
"""

For later:  

The importance of the story behind the data
 
It is important to note here that we applied our common sense, and hence subjectivity. 
A robot, e.g, would examine the relationships between the groups selection (treatment or control) 
and gender (male or female) and would conclude that they are correlated. As causation, 
that required an expert drawing an arrow on the vertex between the nodes.


Here we see that *Recovery* depends both on *Treatment* **and** on *Gender*.  
What makes *Gender* and confounding factor is the fact that *Treatment* depends on 
*Gender*, too. 

Note that this tutorial is aimed to be interactive and hence you can change the results to explore different outcomes. 

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