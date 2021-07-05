import matplotlib.pyplot as plt
import numpy as np

FIG_WIDTH, FIG_HEIGHT = 8, 6

def plot_rates_control_treatment(rate_control, rate_treatment, xstart=0, width=0.3,
                                 color=None, alpha_control=0.7, alpha_treatment=0.3,
                                 rate_factor=100., xtick_vals=None, fontsize=20
                                 ):
    xvals = [xstart, xstart + width + 0.1 * width]
    plt.bar(xvals[0], rate_control * rate_factor, width=width, color=color,
            alpha=alpha_control)
    plt.bar(xvals[1], rate_treatment * rate_factor, width=width, color=color,
            alpha=alpha_treatment)

    rate_diff = rate_treatment - rate_control

    rate_high = rate_treatment
    rate_low = rate_control
    arrowstyle = "->"
    if rate_diff < 0:
        diff_color = "red"
        rate_high = rate_control
        rate_low = rate_treatment
        arrowstyle = "<-"
    elif rate_diff == 0:
        diff_color = "orange"
    else:
        diff_color = "green"

    plt.annotate("", xy=(xvals[1] + width / 1.5, rate_factor * rate_high),
                 xytext=(xvals[1] + width / 1.5, rate_factor * rate_low),
                 arrowprops=dict(arrowstyle=arrowstyle, color=diff_color, linewidth=2))
    plt.annotate( r"$RD=$"+ f"\n{rate_factor * (rate_diff):0.1f}%", xy=(
    xvals[1] + width / 1.4, rate_factor * np.mean([rate_high, rate_low])),
                 color=diff_color, fontsize=fontsize)

    if xtick_vals is not None:
        plt.xticks(xvals, xtick_vals, fontsize=fontsize * 0.8)

    return xvals


def plot_cohorts_control_treatment(df_data, width = 0.3, fontsize = 20, color_male="orange", color_female="purple"):
    plt.clf()
    plt.figure(figsize=(FIG_WIDTH * 2, FIG_HEIGHT))

    xvals_all = []

    col_control = "group=control"
    col_treatment = "group=treatment"

    query_recovered = "recovered==True"

    n_control = df_data[col_control].sum()
    n_treatment = df_data[col_treatment].sum()
    rate_control = df_data.query(query_recovered)[col_control].sum() / n_control
    rate_treatment = df_data.query(query_recovered)[
                         col_treatment].sum() / n_treatment
    xvals_all += plot_rates_control_treatment(rate_control, rate_treatment,
                                              color="darkgray")

    query_gender = "gender == 'male'"
    n_control = df_data.query(query_gender)[col_control].sum()
    n_treatment = df_data.query(query_gender)[col_treatment].sum()
    rate_control = df_data.query(query_gender).query(query_recovered)[
                       col_control].sum() / n_control
    rate_treatment = df_data.query(query_gender).query(query_recovered)[
                         col_treatment].sum() / n_treatment
    xvals_all += plot_rates_control_treatment(rate_control, rate_treatment,
                                              color=color_male,
                                              xstart=3 * width + 0.1 * width
                                              )

    query_gender = "gender == 'female'"
    n_control = df_data.query(query_gender)[col_control].sum()
    n_treatment = df_data.query(query_gender)[col_treatment].sum()
    rate_control = df_data.query(query_gender).query(query_recovered)[
                       col_control].sum() / n_control
    rate_treatment = df_data.query(query_gender).query(query_recovered)[
                         col_treatment].sum() / n_treatment
    xvals_all += plot_rates_control_treatment(rate_control, rate_treatment,
                                              color=color_female,
                                              xstart=6. * width + 0.2 * width
                                              )

    # plt.xlabel("group", fontsize=fontsize)

    plt.xticks(xvals_all, ["population\ncontrol", "population\ntreatment",
                           "males\ncontrol", "males\ntreatment",
                           "females\ncontrol", "females\ntreatment"
                           ], fontsize=fontsize * 0.8)

    # plt.xlim(- width, 2 * width)

    plt.ylabel("recovery rate %", fontsize=fontsize)

    ax = plt.gca()
    # grid
    ax.grid(axis='y', alpha=0.3)
    ax.grid(False, axis='x')
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    return plt.gcf()

def plot_rates_counts(df_data, rate_width=0.01, color_population="gray", color_male="orange", color_female="purple", alpha_control=0.7, alpha_treatment=0.3, fontsize=20):
    plt.clf()
    n_control = df_data["group=control"].sum()
    n_treatment = df_data["group=treatment"].sum()
    rate_control = df_data.query("recovered==True")["group=control"].sum() / n_control
    rate_treatment = df_data.query("recovered==True")[
                         "group=treatment"].sum() / n_treatment
    plt.bar(rate_control, n_control, width=rate_width, color=color_population,
            label="pop control", alpha=alpha_control)
    plt.bar(rate_treatment, n_treatment, width=rate_width, color=color_population,
            label="pop treatment", alpha=alpha_treatment)

    query_gender = "gender == 'male'"
    n_control = df_data.query(query_gender)["group=control"].sum()
    n_treatment = df_data.query(query_gender)["group=treatment"].sum()
    rate_control = df_data.query(query_gender).query("recovered==True")[
                       "group=control"].sum() / n_control
    rate_treatment = df_data.query(query_gender).query("recovered==True")[
                         "group=treatment"].sum() / n_treatment
    plt.bar(rate_control, n_control, width=rate_width, color=color_male,
            label="male control", alpha=alpha_control)
    plt.bar(rate_treatment, n_treatment, width=rate_width, color=color_male,
            label="male treatment", alpha=alpha_treatment)

    query_gender = "gender == 'female'"
    n_control = df_data.query(query_gender)["group=control"].sum()
    n_treatment = df_data.query(query_gender)["group=treatment"].sum()
    rate_control = df_data.query(query_gender).query("recovered==True")[
                       "group=control"].sum() / n_control
    rate_treatment = df_data.query(query_gender).query("recovered==True")[
                         "group=treatment"].sum() / n_treatment
    plt.bar(rate_control, n_control, width=rate_width, color=color_female,
            label="female control", alpha=alpha_control)
    plt.bar(rate_treatment, n_treatment, width=rate_width, color=color_female,
            label="female treatment", alpha=alpha_treatment)

    plt.xlim(0., 1)

    plt.xlabel("recovery rate", fontsize=fontsize)
    plt.ylabel("no. of participants", fontsize=fontsize)
    plt.legend(title="group")

    ax = plt.gca()
    # grid
    ax.grid(axis='y', alpha=0.3)
    ax.grid(False, axis='x')
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    return plt.gcf()

