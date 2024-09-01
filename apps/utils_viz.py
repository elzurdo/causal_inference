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


# TODO: deprecate
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

# TODO deprecate
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


def plot_difference_metric(diff, xval=0, color=None, dx=0.15, fontsize=12, hatch=None):
    plt.bar(xval, diff, color=color, hatch=hatch)

    color_diff, yval_frac = "green", 0.002
    if diff < 0:
        color_diff, yval_frac = "red", 0.015
    elif diff == 0:
        color_diff = "orange"
    yval = diff + np.sign(diff) * yval_frac

    plt.annotate(f"{diff * 100:0.1f}%", xy=(xval - dx, yval), color=color_diff,
                 fontsize=fontsize)

#def plot_risk_difference(rate_control, rate_treatment, xval=0, color=None, dx=0.15, fontsize=12):
#    rate_diff = rate_treatment - rate_control
#    plot_difference_metric(xval, rate_diff, xval=0, color=None, dx=0.15, fontsize=12)

def plot_risk_difference_pop_cohorts(df_data, color_population="lightgray", color_male="orange",
                                     color_female="purple", fontsize=12, ace=None):
    xvals_all, xlabels = [0, 1, 2], ["RD\npopulation", "RD\nmales", "RD\nfemales"]
    yvals = []
    if ace is not None:
        xvals_all.append(3)
        xlabels.append("ACE\npopluation")
        plot_difference_metric(ace, xval=3, color="darkgray", hatch="/")
        yvals.append(ace)

    n_control = df_data["group=control"].sum()
    n_treatment = df_data["group=treatment"].sum()
    rate_control = df_data.query("recovered==True")["group=control"].sum() / n_control
    rate_treatment = df_data.query("recovered==True")[
                         "group=treatment"].sum() / n_treatment
    plot_difference_metric(rate_treatment - rate_control, color=color_population)
    yvals.append(rate_treatment - rate_control)

    query_gender = "gender == 'male'"
    n_control = df_data.query(query_gender)["group=control"].sum()
    n_treatment = df_data.query(query_gender)["group=treatment"].sum()
    rate_control = df_data.query(query_gender).query("recovered==True")[
                       "group=control"].sum() / n_control
    rate_treatment = df_data.query(query_gender).query("recovered==True")[
                         "group=treatment"].sum() / n_treatment
    plot_difference_metric(rate_treatment - rate_control, xval=1, color=color_male)
    yvals.append(rate_treatment - rate_control)

    query_gender = "gender == 'female'"
    n_control = df_data.query(query_gender)["group=control"].sum()
    n_treatment = df_data.query(query_gender)["group=treatment"].sum()
    rate_control = df_data.query(query_gender).query("recovered==True")[
                       "group=control"].sum() / n_control
    rate_treatment = df_data.query(query_gender).query("recovered==True")[
                         "group=treatment"].sum() / n_treatment
    plot_difference_metric(rate_treatment - rate_control, xval=2, color=color_female)
    yvals.append(rate_treatment - rate_control)

    plt.xticks(xvals_all, xlabels, fontsize=fontsize * 0.8)

    yval_buffer = 0.02
    ymin = np.min(yvals) - yval_buffer
    ymax = np.max(yvals) + yval_buffer
    plt.ylim(ymin, ymax)

    ax = plt.gca()
    # grid
    ax.grid(axis='y', alpha=0.3)
    ax.grid(False, axis='x')
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    return plt.gcf()

def plot_rates_vs_size_control_vs_treatment(df_data, display_mode="problem", rate_width = 0.03, alpha=0.5):
    hatch_male = "."
    hatch_female = "/"

    color_male = "orange"
    color_female = "purple"
    label_male = "males"
    label_female = "females"

    fig, axs = plt.subplots(nrows=2, ncols=1)

    if "problem" == display_mode:
        color_male = "gray"
        color_female = "gray"
        hatch_male = None
        hatch_female = None
        label_male = None
        label_female = None

    query_gender = "gender == 'male'"
    n_control = df_data.query(query_gender)["group=control"].sum()
    n_treatment = df_data.query(query_gender)["group=treatment"].sum()
    rate_control = df_data.query(query_gender).query("recovered==True")[
                       "group=control"].sum() / n_control
    rate_treatment = df_data.query(query_gender).query("recovered==True")[
                         "group=treatment"].sum() / n_treatment
    axs[0].bar(rate_control, n_control, width=rate_width, color=color_male,
               label=label_male, alpha=alpha, hatch=hatch_male)
    axs[1].bar(rate_treatment, n_treatment, width=rate_width, color=color_male,
               alpha=alpha, hatch=hatch_male)

    query_gender = "gender == 'female'"
    n_control = df_data.query(query_gender)["group=control"].sum()
    n_treatment = df_data.query(query_gender)["group=treatment"].sum()
    rate_control = df_data.query(query_gender).query("recovered==True")[
                       "group=control"].sum() / n_control
    rate_treatment = df_data.query(query_gender).query("recovered==True")[
                         "group=treatment"].sum() / n_treatment
    axs[0].bar(rate_control, n_control, width=rate_width, color=color_female,
               label=label_female, alpha=alpha, hatch=hatch_female)
    axs[1].bar(rate_treatment, n_treatment, width=rate_width, color=color_female,
               alpha=alpha, hatch=hatch_female)

    n_control = df_data["group=control"].sum()
    n_treatment = df_data["group=treatment"].sum()
    y_min = 0
    y_max = n_treatment

    if "problem" == display_mode:
        rate_control = df_data.query("recovered==True")[
                           "group=control"].sum() / n_control
        rate_treatment = df_data.query("recovered==True")[
                             "group=treatment"].sum() / n_treatment
        axs[0].plot([rate_control, rate_control], [y_min, y_max], color="red",
                    label="Control average")
        axs[1].plot([rate_treatment, rate_treatment], [y_min, y_max], color="red", label="Treatment average")

    axs[0].set_xlim(0., 1.)
    axs[1].set_xlim(0., 1.)
    axs[0].set_ylim(y_min, y_max)
    axs[1].set_ylim(y_min, y_max)

    axs[0].grid(axis='y', alpha=0.3)
    axs[0].grid(False, axis='x')
    # Hide the right and top spines
    axs[0].spines['right'].set_visible(False)
    axs[0].spines['top'].set_visible(False)

    axs[1].grid(axis='y', alpha=0.3)
    axs[1].grid(False, axis='x')
    # Hide the right and top spines
    axs[1].spines['right'].set_visible(False)
    axs[1].spines['top'].set_visible(False)

    axs[0].set_ylabel("no. of participants")
    axs[1].set_ylabel("no. of participants")
    axs[1].set_xlabel("recovery rate")

    ax0_2 = axs[0].twinx()
    ax0_2.spines['right'].set_visible(False)
    ax0_2.spines['top'].set_visible(False)
    ax0_2.set_yticks([])
    ax0_2.set_ylabel("Control", fontsize=20, rotation=270)

    ax1_2 = axs[1].twinx()
    ax1_2.spines['right'].set_visible(False)
    ax1_2.spines['top'].set_visible(False)
    ax1_2.set_yticks([])
    ax1_2.set_ylabel("Treatment", fontsize=20, rotation=270)

    axs[0].legend(loc="upper left")
    axs[1].legend(loc="upper left")
    plt.tight_layout()

    return fig


