# -*- coding: utf-8 -*-
# > *Referring to Study question 1.5.2 (Figure 1.10) and the parameters listed therein ...*
#
# $$Y \leftarrow X \leftarrow Z \rightarrow Y$$
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
# |$x_0$|$y_1$|$\frac{(1-r)(1-q_1)p_1}{1-q_1}$|$\frac{r(1-q_2)p_3}{1-q_2}$| $(1-p_1)(1-r) + p_3 r$
# |$x_1$|$y_0$|$\frac{(1-r)q_1(1-p_2)}{q_1}$| $\frac{rq_2(1-p_4)}{q_2}$| $(1-p_2)(1-r) + (1-p_4)r$
# |$x_1$|$y_1$|$\frac{p_2q_1(1-r)}{q_1}$|$\frac{p_4q_2r}{q_2}$|$p_2(1-r) + p_4r$|
#
# We notice in $P(y|do(x))$ there are no $q$ terms, i.e, no $P(X|Z)$ due to conditioning on $Z$. 

# # (b) 
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

# # (c) 
#
# [Risk Difference](https://en.wikipedia.org/wiki/Risk_difference)
#
# > *Compute the Average Causal Effect (ACE) and compare it to the Risk Difference (RD). What is the difference between ACE and the RD?* 
#
# Average Causal Effect (ACE):  
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
# $$P(y|x) = \sum_z P(y,z|x) = \sum_z P(y|x,z)P(z|x) = \frac{1}{P(x)} \sum_z P(y|x,z)P(x,z)$$
#
# where we used Bayes Theorm: $P(z|x)P(x) = P(x|z)P(z)=P(x,z)$
#
# We already know:  
# $P(x_0) = P(x_0, z_0) + P(x_0, z_1) = (1-q_1)(1-r) + (1-q_2)r$  
# $P(x_1) = P(x_1, z_0) + P(x_1, z_1) = q_1(1-r) + q_2r$
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
#
# > *What values of the parameters would minimize the difference?*
#
# ## Solution 1  
# We will set $P(X|Z)=P(X)$, or $P(X=x_1|z_0)$ = $P(X=x_1|z_1)$, i.e., $q_1=q_2\equiv q$. This means that the treatment ($x_1$) and control ($x_0$) sizes differ, but independently from $Z$.  
# If we set  we are ensuring that $P(X=x_1|Z)$ does not depend on $z$:  
#
# $$P(y_1|x_1) =  
# \frac{1}{q(1-r) + qr} \left(p_2q(1-r) + p_4qr \right) = p_2(1-r) + p_4r 
# $$
#
# $$P(y_1|x_0) =  \frac{1}{(1-q)(1-r) + (1-q)r} \left(p_1(1-q)(1-r) + p_3(1-q)r \right) = p_1(1-r) + p_3r
# $$
#
# $$ RD = P(y_1|x_1) -  P(y_1|x_0) = \\  p_2(1-r) + p_4r - \left(  p_1(1-r) + p_3r \right) = \\
# \left(p_4 - p_3 \right) r + \left( p_2 - p_1 \right)(1-r) = ACE
# $$
#
# ## Solution 2  
# We set $p_1=p_3 \equiv P_{m}(y_1|x_0), p_2=p_4 \equiv P_{m}(y_1|x_1)$. 
# This means that the outcome by conditioned on group $P(y|x)$ differs between treatment ($x_1$) and control ($x_0$) but is independent from $Z$
#
# From here we see: 
#
# $$ACE = (p_2 - p_1) r + (p_2 - p_1) (1-r) = p_2 - p_1 = P_{m}(y_1|x_1) - P_{m}(y_1|x_0) = RD$$ 
# i.e, $P(Z)$ ($r$) terms have no impact. 
#
# Examining from the second derivation:  
# $$P(y_1|x_1) =  \frac{1}{q_1(1-r) + q_2r} \left(p_2q_1(1-r) + p_2q_2r \right) = p_2
# $$
#
# $$P(y_1|x_0) =  \frac{1}{(1-q_1)(1-r) + (1-q_2)r} \left(p_1(1-q_1)(1-r) + p_1(1-q_2)r \right) = p_1
# $$

# # (d) 
# > *Find a combination of parameters that exhibit Simpson’s reversal (as in Study question 1.5.2(c)) and show explicitly that the overall causal effect of the drug is obtained from the desegregated data.*

# Simpson's **reversal** may be obtained with combinations that have:  
# $$(p_4 > p_3 >> p_2 > p_1) \& (q_1 > q_2)$$ regardless of the value of $r$
#
# Let's examine 
# * $p_1 = p$
# * $p_2 = 2p$
# * $p_3 = 20p$
# * $p_4 = 30p$
# * $q_2 = q$
# * $q_1 = 2q$

# $$ACE = (30 - 20)p r + (2 - 1)p (1-r) = 10pr + p - pr = p(9r + 1)$$
#
#
# E.g, 
# * $p=0.02$
# * $r = 0.4$
#
# $$ACE = 0.3 (9 * 0.2 + 1) = 0.092  $$

# This is a bit over the top, but I was interested in looking for a nice expression for $RD$ (but it is really ugly ...):  
#
#
# Solving for treatment:  
# $$P(y_1|x_1) =  
# \frac{1}{q_1(1-r) + q_2r} \left(p_2q_1(1-r) + p_4q_2r \right) = \\
# \frac{1}{2q(1-r) + qr} \left(2p2q(1-r) + 30pqr \right) = \\
# \frac{1}{2q - qr} \left(4pq + 26pqr \right) = \\
# \frac{1}{2 - r} 2p\left(2 + 13r \right)
# $$
#
# Solving for placebo: 
# $$P(y_1|x_0) = 
# \frac{1}{(1-2q)(1-r) + (1-q)r} \left(p(1-2q)(1-r) + 20p(1-q)r \right)= \\
# \frac{1}{(1-2q)(1-r) + (1-q)r} p\left(1 - r - 2q + 2qr + 20r - 20qr \right) = \\
# \frac{1}{(1-2q)(1-r) + (1-q)r} p\left(1 + 19r - 2q - 18qr \right)
# $$
#

# +
p = 0.02
r = 0.4
q = 0.3

p_y1_x1 = 2*p*(2 + 13 *r)/(2-r)

p_y1_x0 = p*(1 + 19*r - 2*q - 18*q*r) /( (1-2*q) * (1-r) + (1-q)*r )

print(f"ACE = P(y_1|do(x_1)) - P(y_1|do(x_0)) = p(9r + 1) = {p*(9*r + 1):0.3}")
print(f"RD = P(y_1|x_1) - P(y_1|x_0) = {p_y1_x1:0.3f} - {p_y1_x0:0.3f} = {p_y1_x1 - p_y1_x0:0.3f} ")
