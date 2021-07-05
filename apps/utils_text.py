
def header():
    text = \
    f""" 
    ## 🧮 Simpson's Calculator - An Interactive Demo
    **Simpson's "Paradox" is a problem of data misinterpretation and serves as an excellent example to learn about causal analysis.**


    > *Causation is not merely an aspect of statistics - it is an addition to statistics* - Judea Pearl
    """

    return text

def disclaimer_calculator(mode_calculator, mode_tutorial):
    text = \
    f"This **{mode_calculator}** mode assumes that you are familiar with Simpson's Paradox, how it's resolved and are interested in testing the use case presented."
    text += \
    f"  (For an explanation of the phenomena change to the **{mode_tutorial}** option in the left sidebar.)"

    return text


def intro_text():
    text = \
    """
    There is an interesting numerical quirk that may arise in an analysis, where 
     results of a population contradict with those of subpopulations.  

    For example, imagine that you are analysing the recovery rate of a drug, where
    patients are separated to treatment and control groups. 

    You find that males treatment group performs better than the male control group, and 
    you reach a similar conclusion for the females.  Curiously, though, when you aggregate all the results you get the exact opposite finding!

    Here you'll examine tables containing mock, but plausible, results of a control triage to better understand 
    the problem ... and its solution. Along the way you will learn about confounding factors 
    and how to adjust for them in the context of causal analysis.

    This is an interactive demo! You might find it useful to play around with numbers to solidify your understanding.
    Feel free throughout to play with the dials on the left.  
    """

    return text

def equations_explanation_rd():
    equation_rd = r'''
    $$RD =  P(\text{recovery=True}|\text{group=treatment}) - P(\text{recovery=True}|\text{group=control})$$
    '''

    text = "The ***Risk Difference*** (**RD**) to used describe the recovery rate differences " \
           "between the groups:"
    text += r"$\\$" + f"{equation_rd}"

    return text

def equations_exaplanation_ace():
    equation_ace_using_rd = r"$$ACE = \sum_\text{strata}RD_\text{stratum}P(\text{stratum}) = RD_{\text{male}} P(\text{male}) + RD_{\text{female}} P(\text{female})$$"

    text = r"$\\$" + "The ***Average Causal Effect*** (**ACE**) is accounts for possible imbalances in the cohort ratios:"
    text += r"$\\$" + f"{equation_ace_using_rd}"

    # equation_ace = r"$$ACE = P(\text{recovery}|do(\text{treatment})) - P(\text{recovery}|do(\text{control}))$$"

    return text

def equations_exaplanation_ace_do_operation():
    equation_ace = r"$$ACE = P(\text{recovery=True}|do(\text{group=treatment})) - P(\text{recovery=True}|do(\text{group=control}))$$"

    text = r"$\\$" + "ACE is derived by applying **do-operation** surgery on a Graph Model:"
    text += r"$\\$" + f"{equation_ace}"


    return text


def gateway():
    text = """
    # Simpson's Paradox: A Gateway To Causal Inference

    Correlation does not imply causation. 
    It turns out, however, that with some simple ingenious tricks one can unveil causal relationships within standard observational data, 
    without having to resort to expensive random control trials. 

    A simple example of this is the Simpson's Paradox demonstrated here.
    This is a classical problem of data misinterpretation. 
    Understanding its solution is a gateway to realise that causality, at times, may be as simple as one or two lines of code. 
    """

    return text

def edward():
    text = """
    ![](https://upload.wikimedia.org/wikipedia/en/d/de/Edward_H._Simpson.jpg)

    > Edward Hugh Simpson CB (10 December 1922 – 5 February 2019) was a British codebreaker, statistician and civil servant. He was introduced to the thinking of mathematical statistics as a cryptanalyst at Bletchley Park (1942–45).   [Wikipedia](https://en.wikipedia.org/wiki/Edward_H._Simpson)
    """

    return text

def created_by():
    text = \
    """
    Created by: Eyal Kazin 
    ([site](https://elzurdo.github.io/), 
    [LinkedIN](https://www.linkedin.com/in/eyal-kazin-0b96227a/), 
    [@eyalkazin](https://twitter.com/eyalkazin))
    """

    return text
