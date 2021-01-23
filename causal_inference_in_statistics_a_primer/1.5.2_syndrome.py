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
# Note that here I use:  
# $P(x_0|z_0) + P(x_1|z_0) = 1 \rightarrow P(x_0|z_0) = 1-q_1$,     
# $P(x_0|z_1) + P(x_1|z_1) = 1 \rightarrow P(x_0|z_1) = 1-q_2$.   
# The reason for this is that when conditioning on $z$ (e.g, $z_0$), $x$ has only two options, i.e, the sum of the probabilities need to be 1. 
#
#
# ## $P(x,y)$
#
# Here we will use the 
#
# The Law Of Total Probability
# For any set of events $B_1, ...,B_n$ such that exactly one of the vents must be true (an exhaustive, mutually exclusive set, called a *partition*) we have
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
# |$x_1$|$y_1$|$p_2q_1(1-r)$|$p_4q_2r$

# # Resources
# * [Brian Callander's solution](https://www.briancallander.com/posts/causal_inference_in_statistics_primer/question_1_5_2.html)  
# * [jneuer's solution](https://github.com/jneuer/pearl-primer/blob/master/Ch01/Sec1.5/10-sq-1.5.2.jpg)  
# * [fredthedead's solution](https://github.com/fredthedead/causal-inference-in-statistics-solutions/blob/master/ch-1.ipynb)
