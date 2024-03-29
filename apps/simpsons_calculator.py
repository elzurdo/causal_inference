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


with st.beta_expander('Overview'):
    st.write(utils_text.intro_text())

# --- default values ---
treatments_default = 1000
controls_default = treatments_default
male_frac_default = 0.5     # Gender split
success_rate_default = 0.7

male_treatment_frac_paradox = 0.2
male_treatment_success_rate_paradox = 0.8
female_treatment_success_rate_paradox = 0.4


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


df


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

stats_str = None
if np.isclose(rd_population,ace_population):
    stats_str = "No Simpson's Paradox"

str_solution = 'Visualise ACE'
str_visualise_details = 'Rate details'
if np.sign(rd_males) * np.sign(rd_females):
    if ~np.isclose(rd_population,ace_population):
        stats_str = "Simpson's Paradox!"

        if (rd_population > rd_males) & (rd_population > rd_females) & (np.sign(rd_males) == 1):
            stats_str = "Anti Simpson's Paradox!" + r" ($RD_\text{total}>RD_\text{male}, RD_\text{female}$)"
        if (rd_population < rd_males) & (rd_population < rd_females) & (np.sign(rd_males) == -1):
            stats_str = "Anti Simpson's Paradox!" + r" ($RD_\text{total}<RD_\text{male}, RD_\text{female}$)"

        str_visualise_details = 'Problem details'
        str_solution = "Visualise solution"


if mode_calculator == mode_chosen:
    st.markdown(stats_str)
    display_ace = st.checkbox(str_solution)

    if display_ace:
        ace_to_plot = ace_population
        str_visualise_details = 'Solution details'
    else:
        ace_to_plot = None
    fig_rds = utils_viz.plot_risk_difference_pop_cohorts(df, ace=ace_to_plot)
    st.pyplot(fig_rds)

    with st.beta_expander(str_visualise_details):
        display_mode = "problem"
        if display_ace:
            display_mode = "solution"
        fig_problem_solution = utils_viz.plot_rates_vs_size_control_vs_treatment(df, display_mode=display_mode)
        st.pyplot(fig_problem_solution)



    # with st.beta_expander('Visualise rates control vs. treatment'):
    #     fig_rates = utils_viz.plot_cohorts_control_treatment(df)
    #     st.pyplot(fig_rates)
    #
    # with st.beta_expander('Visualise rates against no. of participants'):
    #     fig_rates_participants = utils_viz.plot_rates_counts(df)
    #     st.pyplot(fig_rates_participants)

with st.beta_expander('Equations Used'):
    st.write(utils_text.equations_explanation_rd())

    st.write(utils_text.equations_exaplanation_ace())

    st.write(utils_text.equations_exaplanation_ace_do_operation())

with st.beta_expander("Simpson's Paradox: A Gateway To Causal Inference" ):
    st.write(utils_text.gateway())

with st.beta_expander("Who was Simpson?"):
    st.write(utils_text.edward())

st.write(utils_text.created_by())

