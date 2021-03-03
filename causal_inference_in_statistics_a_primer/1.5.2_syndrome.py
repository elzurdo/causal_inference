# -*- coding: utf-8 -*-
# **Study question 1.5.2**
#
# > *Assume that a population of patients contains a fraction r of individuals who suffer from
# a certain fatal syndrome Z, which simultaneously makes it uncomfortable for them to take
# a life-prolonging drug X (Figure 1.10). Let $Z = z_1$ and $Z = z_0$ represent, respectively, the
# presence and absence of the syndrome, $Y = y_1$ and $Y = y_0$ represent death and survival,
# respectively, and $X = x_1$ and $X = x_0$ represent taking and not taking the drug. Assume that
# patients not carrying the syndrome, $Z = z_0$, die with probability $p_2$ if they take the drug
# and with probability $p_1$ if they don’t. Patients carrying the syndrome, $Z = z_1$, on the other
# hand, die with probability $p_3$ if they do not take the drug and with probability $p_4$ if they do
# take the drug. Further, patients having the syndrome are more likely to avoid the drug, with
# probabilities $q_1 = P(x_1|z_0)$ and $q_2 = P(x_1 |z_1 )$.*
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

# # (a)
#
# > Based on this model, compute the joint distributions P(x, y, z), P(x, y), P(x, z), and P(y, z) for all values of x, y, and z, in terms of the parameters (r, p1, p2, p3, p4, q1, q2). [Hint: Use the product decomposition of Section 1.5.2.]
#
# ## $P(x,y,z)$  
#
# Calculate $P(x,y,z)$ based on $r,p_1...p_4, q_1, q_2$.
#
#
# $$P(x_1,...,x_n)=\prod_iP(x_i|pa_i)$$  
#
# $pa_i$ - value of the parents of variable $X_i$.
#
# $$P(x,y,z) = P(y|x,z)P(x|z)P(z)$$
#
#
#
# | $x$ | $y$ | $z$ |$P(z)$|$P(x|z)$|$P(y|x,z)$|$P(x,y,z)$|
# | --- | --- | --- | ---- | ------ | -------- |--------- | 
# |$x_0$|$y_0$|$z_0$|$1-r$|$1-q_1$|$1-p_1$|$(1-r)(1-q_1)(1-p_1)$|
# |$x_0$|$y_0$|$z_1$| $r$ |$1-q_2$|$1-p_3$|$r(1-q_2)(1-p_3)$|
# |$x_0$|$y_1$|$z_0$|$1-r$|$1-q_1$|$p_1$|$(1-r)(1-q_1)p_1$|
# |$x_0$|$y_1$|$z_1$| $r$|$1-q_2$|$p_3$|$r(1-q_2)p_3$|
# |$x_1$|$y_0$|$z_0$|$1-r$|$q_1$|$1-p_2$|$(1-r)q_1(1-p_2)$|
# |$x_1$|$y_0$|$z_1$| $r$ |$q_2$|$1-p_4$|$rq_2(1-p_4)$|
# |$x_1$|$y_1$|$z_0$|$1-r$|$q_1$|$p_2$|$p_2q_1(1-r)$|
# |$x_1$|$y_1$|$z_1$| $r$ |$q_2$|$p_4$|$p_4q_2r$|
#
#
# Note that here I use:  
# $P(x_0|z_0) + P(x_1|z_0) = 1 \rightarrow P(x_0|z_0) = 1-q_1$,     
# $P(x_0|z_1) + P(x_1|z_1) = 1 \rightarrow P(x_0|z_1) = 1-q_2$.   
# The reason for this is that when conditioning on $z$ (e.g, $z_0$), $x$ has only two options, i.e, the sum of the probabilities need to be 1. 
#
#
# ## $P(x,y)$
#
# Here we will use the *The Law Of Total Probability*.  
# For any set of events $B_1, ...,B_n$ such that exactly one of the events must be true (an exhaustive, mutually exclusive set, called a *partition*) we have
#
# $$P(A) = P(A,B_1) + ... + P(A,B_n)$$
#
#
# So the weighted sum of conditional probabilities:  
# $$P(A)=P(A|B_1)P(B_1) + ... + P(A|B_n)P(B_n)$$  
#
# This decomposition is called: *conditionalising on $B$* or *the law of alternatives* or *extending the conversation*.
#
# $$P(x,y)=P(y|x)P(x) = \\ \sum_z P(y|x,z)P(x|z) P(z) = \\ P(y|x,z_0)P(x|z_0)P(z_0) + P(y|x,z_1)P(x|z_1)P(z_1) = \\ P(x,y,z_0) + P(x,y,z_1)$$
#
#
# | $x$ | $y$ | $P(x,y,z_0)$ | $ P(x,y,z_1)$ |$P(x,y)$|
# | --- | --- | --- | --- |--- |
# |$x_0$|$y_0$|$(1-r)(1-q_1)(1-p_1)$|$r(1-q_2)(1-p_3)$|
# |$x_0$|$y_1$|$(1-r)(1-q_1)p_1$| $r(1-q_2)p_3$
# |$x_1$|$y_0$|$(1-r)q_1(1-p_2)$| $rq_2(1-p_4)$
# |$x_1$|$y_1$|$p_2q_1(1-r)$|$p_4q_2r$|

# ## $P(x, z)$
#
# $$P(x,z) = P(x,z,y_0) + P(x,z,y_1)$$
#
# But in our case, since, 
#
# $P(x_1|z_0) = q_1$  
# $P(x_1|z_1) = q_2$  
# $P(x_0|z_0) = 1 - q_1$  
# $P(x_0|z_1) = 1 - q_2$,
#
# it would be more practical to do  
#
# $$P(x,z) = P(x|z)P(z)$$
#
# | $x$ | $z$ | $P(x|z)$ | $ P(z)$ |$P(x,z)$|
# | --- | --- | --- | --- |--- |
# |$x_0$|$z_0$| $1-q_1$| $1-r$
# |$x_0$|$z_1$| $1-q_2$| $r$
# |$x_1$|$z_0$| $q_1$| $1-r$
# |$x_1$|$z_1$| $q_2$| $r$
#
#
# ## $P(y, z)$
#
# $$P(y, z) = P(x_0, y, z) + P(x_1, y, z)$$
#
# | $y$ | $z$ | $P(x_0, y, z)$ | $ P(x_1, y, z)$ |$P(y,z)$|
# | --- | --- | --- | --- |--- |
# |$y_0$|$z_0$|$(1-r)(1-q_1)(1-p_1)$|$(1-r)q_1(1-p_2)$
# |$y_0$|$z_1$|$r(1-q_2)(1-p_3)$|$rq_2(1-p_4)$
# |$y_1$|$z_0$|$(1-r)(1-q_1)p_1$|$p_2q_1(1-r)$
# |$y_1$|$z_1$|$r(1-q_2)p_3$|$p_4q_2r$

# # (b)
#
# > *Calculate the difference $P(y_1|x_1) − P(y_1|x_0)$ for three populations: 
# (1) those carrying the syndrome, 
# (2) those not carrying the syndrome, and 
# (3) the population as a whole.*
#
#
# ## With Syndrom
#
# $$Z=z_1$$
#
# In order to calculate $P(y_1|x_1, z_1) − P(y_1|x_0, z_1)$, I first use   
# $$P(y|x,z) = \frac{P(y,x|z)}{P(x|z)} = \frac{P(x, y,z)}{P(x|z)P(z)}$$  
#
# So we have  
#
# $$P(y_1|x_1, z_1) − P(y_1|x_0, z_1) = \\ \frac{P(x_1, y_1,z_1)}{P(x_1|z_1)P(z_1)} - \frac{P(x_0, y_1,z_1)}{P(x_0|z_1)P(z_1)} = \\   \frac{p_4q_2r}{q_2r}  -  \frac{r(1-q_2)p_3}{(1-q_2)r}  = p_4 - p_3$$ 
#
# ... actually, I did not need the full derivation, because I was given $P(y|x,z)$ in the setup. But it's still nice to see it work in action!  
#
#
# ## Without Syndrom
#
# $$Z=z_0$$
#
# $$P(y_1|x_1, z_0) − P(y_1|x_0, z_0) = p_2- p_1$$
#
#
# ## Whole Population
#
# $$P(y_1|x_1) - P(y_1|x_0)$$
#
# We use
#
# $$P(y|x) = \frac{P(x,y)}{P(x)} = \sum_z \frac{P(x,y,z)}{P(x)}$$  
#
# and 
#
#
# $$P(x) = P(x,z_0) + P(x, z_1) = P(x|z_0)P(z_0) + P(x|z_1)P(z_1)$$  
#
# Hence we have  
#
# $$P(x_0) = P(x_0|z_0)P(z_0) + P(x_0|z_1)P(z_1) = (1-q_1)(1-r) + (1-q_2)r$$ 
# $$P(x_1) = P(x_1|z_0)P(z_0) + P(x_1|z_1)P(z_1) = q_1(1-r) + q_2r$$ 
#
#
# Resulting in:  
#
# $$P(y_1|x_1) - P(y_1|x_0) = \\ \sum_{z=z_0, z_1} \frac{P(x_1,y_1,z)}{P(x_1)} - \frac{P(x_0,y_1,z)}{P(x_0)} = \frac{p_2q_1(1-r) + p_4q_2r}{q_1(1-r) + q_2r} - \frac{(1-r)(1-q_1)p_1 + r(1-q_2)p_3}{(1-q_1)(1-r) + (1-q_2)r}
# $$

# # (c) 
#
# > *Using your results for (b), find a combination of parameters that exhibits Simpson’s reversal.*

# # Resources
# * [Pearl's Primer preview, page 31](http://bayes.cs.ucla.edu/PRIMER/primer-ch1.pdf)
# * [Brian Callander's solution](https://www.briancallander.com/posts/causal_inference_in_statistics_primer/question_1_5_2.html)  
# * [jneuer's solution](https://github.com/jneuer/pearl-primer/blob/master/Ch01/Sec1.5/10-sq-1.5.2.jpg)  
# * [fredthedead's solution](https://github.com/fredthedead/causal-inference-in-statistics-solutions/blob/master/ch-1.ipynb)


