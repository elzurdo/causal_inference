import streamlit as st
import numpy as np
import pandas as pd

try:
    import daft
except:
    daft = None

import utils_text
import utils_viz

mode_calculator = "Calculator"
mode_tutorial = "Tutorial"

mode_chosen = st.sidebar.selectbox("Select mode", [mode_calculator, mode_tutorial], index=0)

st.write(utils_text.header())

if mode_calculator == mode_chosen:
    st.write(utils_text.disclaimer_calculator(mode_calculator, mode_tutorial))

with st.expander('Overview'):
    st.write(utils_text.intro_text())

# --- default values ---
treatments_default = 1000
controls_default = treatments_default
male_frac_default = 0.5     # P(male)  - Gender split 

male_treatment_frac_paradox = 0.8  # P(treatment|male)
male_treatment_success_rate_paradox = 0.5  # P(recovery|treatment, male)
female_treatment_success_rate_paradox = 0.9  # P(recovery|treatment, female)


treatments = int(st.sidebar.number_input('Treatments:', format="%d", value=treatments_default))
controls = int(st.sidebar.number_input('Controls:', format="%d", value=controls_default))

people = treatments + controls

min_male_ratio = 0.1
males_frac = st.sidebar.slider(f"male population fraction (i.e, of {people:,})",
                               min_value=min_male_ratio,
                               max_value=1. - min_male_ratio, step=0.01,
                               value=male_frac_default)

females_frac = 1. - males_frac
st.sidebar.write(f"{females_frac * 100.:0.1f}% of the population are females")
st.sidebar.write(f"{males_frac * 100.:0.1f}% of the population are males")

males = int(people * males_frac)
females = people - males

# --- Treatment split by gender ---
males_treatment_frac = st.sidebar.slider(f"male treatment fraction (i.e, of {treatments:,})", min_value=min_male_ratio, max_value=1. - min_male_ratio, step=0.01, value=male_treatment_frac_paradox)

males_treatment = int(treatments * males_treatment_frac)
females_treatment = treatments - males_treatment

st.sidebar.write(f"{(1. - males_treatment_frac) * 100.:0.1f}% of the treatment are females")
st.sidebar.write(f"{males_treatment_frac * 100.:0.1f}% of the treatment are males")


males_control = males - males_treatment
females_control = females - females_treatment

# --- Treatment success rates ---
success_rate_control = st.sidebar.checkbox('Modify group/cohort success rates')

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

male_treatment_r = np.round(male_treatment_r, 2)
female_treatment_r = np.round(female_treatment_r, 2)

male_control_r = np.round(male_control_r, 2)
female_control_r = np.round(female_control_r, 2)

# --- Table Format ---
male_treatment_success = int(male_treatment_r * males_treatment)
male_control_success   = int(male_control_r   * males_control)
female_treatment_success = int(female_treatment_r * females_treatment)
female_control_success   = int(female_control_r   * females_control)


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


st.markdown("# Data")

st_data_explanation = "The table below shows results of a mock clinical trial."
st_data_explanation += " Each of ther four rows is a different cohort males or females who have recovered or not. Columns indicate no. of participatns in each group (Treatment, Control), Gender and the Outcome."
st_data_explanation += " (🪄 Use the sliders on the left sidebar to change the values.)"
st.markdown(st_data_explanation)
# displaying the DataFrame
df

st.markdown("# Visualsation & Interpretation")
rd_population = (male_treatment_success + female_treatment_success)/ treatments -  (male_control_success + female_control_success)/controls
rd_males = male_treatment_success / males_treatment - male_control_success / males_control
rd_females = female_treatment_success / females_treatment - female_control_success / females_control
ace_population = rd_males * males_frac + rd_females * females_frac

#rd_males_str = f'<p style="color:#33ff33;font-size:24px;border-radius:2%;">bah</p>'

# rd_stats_str = r"$RD_\text{total}$   = " + f"{100. * rd_population:0.1f}%, "
# rd_stats_str += r"$RD_\text{male}$   = " + f"{100. * rd_males:0.1f}%, "
# rd_stats_str += r"$RD_\text{female}$ = " + f"{100. * rd_females:0.1f}%"
# ace_stats_str = r"$\\ ACE_\text{total}$   = " + f"{100. * ace_population:0.1f}%"
#
# stats_str = rd_stats_str + ace_stats_str

rd_pop_str = r"$RD_\text{pop}$"
rd_male_str = r"$RD_\text{male}$"
rd_female_str = r"$RD_\text{female}$"
stats_str = "In this case"
if np.isclose(rd_population, ace_population):
    stats_str += f" there is no Simpson's Paradox since {rd_pop_str} is the average of {rd_male_str} and {rd_female_str}."

str_solution = 'Visualise ACE'
str_visualise_details = 'Rate details'

if np.sign(rd_males) * np.sign(rd_females):
    if ~np.isclose(rd_population, ace_population):
        stats_str += f" we see Simpson's Paradox since {rd_pop_str} is not the average of {rd_male_str} and {rd_female_str}."

        if (rd_population > rd_males) & (rd_population > rd_females) & (np.sign(rd_males) == 1):
            stats_str += f"\ninterestingly we see that {rd_pop_str} > ({rd_male_str}, {rd_female_str})"
        if (rd_population < rd_males) & (rd_population < rd_females) & (np.sign(rd_males) == -1):
            stats_str += f"\ninterestingly we see that {rd_pop_str} < ({rd_male_str}, {rd_female_str})" 

        str_visualise_details = 'Detailed visualisation of problem'
        str_solution = "Visualise solution"


if mode_calculator == mode_chosen:
    interpretaion_str = "For each cohort ('population' superset and subsets 'male' and 'female')"
    interpretaion_str += f" we calculate the ***Risk Difference*** defined as\\{utils_text.equation_rd}"
    st.markdown(interpretaion_str)

    display_ace = st.checkbox(str_solution)

    if display_ace:
        ace_to_plot = ace_population
        str_visualise_details = 'Detailed visualisation of solution'
        stats_str += " The Average Casual Effect (ACE) is the correct population average."
    else:
        ace_to_plot = None
    fig_rds = utils_viz.plot_risk_difference_pop_cohorts(df, ace=ace_to_plot)
    st.pyplot(fig_rds)

    st.markdown(stats_str)

    with st.expander(str_visualise_details):
        str_details = "Each panel shows two cohort results (male, female) of the Control (top) and Treatment (bottom) groups: recovery rates against number counts."
        display_mode = "problem"
        if display_ace:
            display_mode = "solution"
        else:
            str_details += " The red lines inidcate the average recovery rate of the Treatment/Control"
        fig_problem_solution = utils_viz.plot_rates_vs_size_control_vs_treatment(df, display_mode=display_mode)
        st.markdown(str_details) 
        st.pyplot(fig_problem_solution)
        if not display_ace:
            st.markdown("\nIdentify whos average is higher 'Treatment' or 'Control'? Now tick the 'Visaulise solution' box above and compare results.")



    # with st.beta_expander('Visualise rates control vs. treatment'):
    #     fig_rates = utils_viz.plot_cohorts_control_treatment(df)
    #     st.pyplot(fig_rates)
    #
    # with st.beta_expander('Visualise rates against no. of participants'):
    #     fig_rates_participants = utils_viz.plot_rates_counts(df)
    #     st.pyplot(fig_rates_participants)

st.markdown("# Miscellaneous")
with st.expander('Equations Used'):
    st.write(utils_text.equations_explanation_rd())

    st.write(utils_text.equations_exaplanation_ace())

    st.write(utils_text.equations_exaplanation_ace_do_operation())

with st.expander("Simpson's Paradox: A Gateway To Causal Inference" ):
    st.write(utils_text.gateway())

with st.expander("Who was Simpson?"):
    st.write(utils_text.edward())

st.write(utils_text.created_by())

