# -*- coding: utf-8 -*-
# > *Referring to Study question 1.5.2 (Figure 1.10) and the parameters listed therein ...*
#
#
# Fatal Syndrome  
# $Z = 
# \begin{cases}
#       z_0 & \text{absent}\\
#       z_1 & \text{present}
# \end{cases}
# $
#
# Outcome  
# $Y = 
# \begin{cases}
#       y_0 & \text{survival}\\
#       y_1 & \text{death}
# \end{cases}
# $
#
# Treatment  
# $X = 
# \begin{cases}
#       x_0 & \text{not treated}\\
#       x_1 & \text{treatment}
# \end{cases}
# $
#
#
# $P(Z=z_1)=r \ \ \rightarrow \ \ P(Z=z_0)=1-r$  
#
# $P(Y=y_1|Z=z_0, X=x_0) = p_1$  
# $P(Y=y_1|Z=z_0, X=x_1) = p_2$
#
# $P(Y=y_1|Z=z_1, X=x_0) = p_3$  
# $P(Y=y_1|Z=z_1, X=x_1) = p_4$
#
#
# $P(X=x_1|Z=z_0) = q_1$  
# $P(X=x_1|Z=z_1) = q_2$  
#
#
#

# # (a)
#
# > *Compute $P(y|do(x))$ for all values of $x$ and $y$, by simulating the intervention $do(x)$ on the model.*
#
# Continuing `1.5.2_syndrome` we now apply intervention on $X$. 
#
# $$P(y|do(x)) = \sum_z \frac{P(x,y,z)}{P(x|z)} = \\
# \frac{P(x,y,z_0)}{P(x|z_0)} + \frac{P(x,y,z_1)}{P(x|z_1)}
# $$
#
# | $x$ | $y$ | $\frac{P(x,y,z_0)}{P(x|z_0)}$ | $\frac{P(x,y,z_1)}{P(x|z_1)}$ |$P(y|do(x))$|
# | --- | --- | --- | --- |--- |
# |$x_0$|$y_0$|$\frac{(1-r)(1-q_1)(1-p_1)}{1-q_1}$|$\frac{r(1-q_2)(1-p_3)}{1-q_2}$|$(1-p_1)(1-r) +(1-p_3)r$
# |$x_0$|$y_1$|$.$| $.$
# |$x_1$|$y_0$|$.$| $.$
# |$x_1$|$y_1$|$.$|$.$|

# ## (b) 
#
# > *Compute $P(y|do(x))$ for all values of $x$ and $y$, using the adjustment formula (3.5)*
#
# Before: graph $G$ has probabilities $P$
# $$X \leftarrow Z \rightarrow Y  \leftarrow X$$
#
# After: graph $G_m$ has probabilities $P_m$
#
# $$Z \rightarrow Y  \leftarrow X$$
#
# $$P(y|do(x)) = \sum_z P(y|x,z)P(z) = \\ P(y|x,z_0)P(z_0) + P(y|x,z_1)P(z_1)$$
#
#
# | $x$ | $y$ | $P(y|x,z_0)P(z_0)$ | $P(y|x,z_1)P(z_1)$ |$P(y|do(x))$|
# | --- | --- | --- | --- |--- |
# |$x_0$|$y_0$|$(1-p_1)(1-r)$|$(1-p_3)r$|
# |$x_0$|$y_1$|$p_1(1-r)$| $p_3r$
# |$x_1$|$y_0$|$(1-p_2)(1-r)$| $(1-p_4)r$
# |$x_1$|$y_1$|$p_2(1-r)$|$p_4r$|

# ## (c) 
#
# [Risk Difference](https://en.wikipedia.org/wiki/Risk_difference)
#
# > *Compute the Average Causal Effect (ACE) and compare it to the Risk Difference*. What is the difference between ACE and the RD? What values of the parameters would minimize the difference?
#
# Average Causal Difference (ACE):  
# $$ACE = P(y_1|do(x_1)) − P(y_1|do(x_0)) = \\ 
# p_2(1-r) + p_4r -  p_1(1-r) - p_3r = \\ 
# (p_4 -p_3) r + (p_2 - p_1) (1-r)
# $$
#
#
# Risk Difference (RD):  
# $$RD = 
# P(y_1|x_1) − P(y_1|x_0) 
# $$
#
# We start with:  
# $$P(y|x) = \sum_z P(y,z|x) = \sum_z P(y,|x,z)P(z|x) = \frac{1}{P(x)} \sum_z P(y|x,z)P(x,z)$$
#
# where we used Bayes Theorm: $P(z|x)P(x) = P(x|z)P(z)=P(x,z)$
#
# We already know:  
# $P(x_0) = P(x_0, z_0) + P(x_0, z_1) = (1-q_1)(1-r) + (1-q_2)r$  
# $P(x_1) = P(x_1, z_0) + P(x_1, z_1) = (q_1)(1-r) + q_2r$
#
# So we have:  
# $$P(y_1|x_1) =  \frac{1}{P(x_1)} \left(P(y_1|x_1,z_0)P(x_1,z_0) + P(y_1|x_1,z_1)P(x_1,z_1) \right) =\\
# \frac{1}{q_1(1-r) + q_2r} \left(p_2q_1(1-r) + p_4q_2r \right)
# $$
#
# $$P(y_1|x_0) =  \frac{1}{P(x_0)} \left(P(y_1|x_0,z_0)P(x_0,z_0) + P(y_1|x_0,z_1)P(x_0,z_1) \right) =\\
# \frac{1}{(1-q_1)(1-r) + (1-q_2)r} \left(p_1(1-q_1)(1-r) + p_3(1-q_2)r \right)
# $$
#

# # (d) 
# > *Find a combination of parameters that exhibit Simpson’s reversal (as in Study question 1.5.2(c)) and show explicitly that the overall causal effect of the drug is obtained from the desegregated data.*

#
#
#
#
# Equations of invariance  
# * $P_m(y,|z,x)=P(y|z,x)$ because of the way $Y$ responds to both $X$ and $Y$ regardless of the manipulation of $X$.
# * $P_m(z)=P(z)$ because $Z$ is not affected by any other variable.  
#
#
# $$P(y|do(x)) = P_m(y|x)= ... = \sum_z P(y|x,z)P(z)$$
#
#
#
# | $x$ | $y$ | $P(x,y,z_0)$ | $ P(x,y,z_1)$ |$P(y|do(x))$|
# | --- | --- | --- | --- |--- |
# |$x_0$|$y_0$|$(1-r)(1-q_1)(1-p_1)$|$r(1-q_2)(1-p_3)$|
# |$x_0$|$y_1$|$(1-r)(1-q_1)p_1$| $r(1-q_2)p_3$
# |$x_1$|$y_0$|$(1-r)q_1(1-p_2)$| $rq_2(1-p_4)$
# |$x_1$|$y_1$|$p_2q_1(1-r)$|$p_4q_2r$|
