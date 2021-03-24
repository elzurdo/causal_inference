# -*- coding: utf-8 -*-
import pandas as pd

# # Study question 1.3.2: Genders in High School
#
# > *Consider Table 1.5 showing the relationship between gender and education level in the U.S. adult population.     
# (a) Estimate $P($High School$)$.    
# (b) Estimate P(High School OR Female).    
# (c) EstimateP(HighSchool|Female).     
# (d) Estimate P(Female | High School).* 

# +
df = \
pd.DataFrame({'gender': (['male'] * 4) + (['female'] * 4), 
              'highest': ['never', 'high school', 'college', 'graduate'] * 2,
              'occurence': [112, 231, 595, 242, 136,189,763,172]
             })

total = df["occurence"].sum()

df

# +
# P(Highschool)

highest = "high school"
df.query("highest == @highest")["occurence"].sum() / df["occurence"].sum()
# -

# $$P(A \ \text{OR} \  B) = P(A) + P(B) - P(A,B)$$

# +
# P(High School OR Female)

highest1 = "high school"
gender = "female"
df.query("(highest == @highest) | (gender == @gender)")["occurence"].sum() / total

# +
# P(High School) + P(Female) - P(High School, Female)
p_hs = df.query("(highest == @highest)")["occurence"].sum() / total
p_fm = df.query("(gender == @gender)")["occurence"].sum()  / total
p_hs_fm = df.query("(highest == @highest) & (gender == @gender)")["occurence"].sum() / total

p_hs + p_fm - p_hs_fm

# +
# P(Female | High School)

df.query("(highest == @highest) & (gender == @gender)")["occurence"].sum() / df.query("(gender == @gender)")["occurence"].sum()
# -

# P(HighSchool|Female)
df.query("(highest == @highest) & (gender == @gender)")["occurence"].sum() / df.query("(highest == @highest)")["occurence"].sum()


# # Study question 1.3.3
# > *Consider the casino problem described in Section 1.3.7* 
#
# $P(11|craps) = \frac{1}{18}$  
# $P(11|roulette) = \frac{1}{38}$
#
# $$P(number) = \sum_{game} P(number|game)P(game) $$
#
# $$P(game|number) = \frac{P(number|game)P(game)}{P(number)}$$
#
#
# > (a) Compute $P(“craps”|“11”)$ assuming that there are twice as many roulette tables as craps games at the casino.
#
#
# $P(roulette) = 2 P(craps)$  
# $P(roulette) + P(craps) = 1$  
# $\rightarrow P(roulette) = \frac{2}{3}, P(craps) = \frac{1}{3}$
#
#
# $$P(11) = P(11|craps)P(craps) + P(11|roulette)P(roulette) = 1/18 \cdot 1/3 + 1/38 \cdot 2/3 = 0.036$$
#
# $$P(craps|11) = \frac{P(11|craps)P(craps)}{P(11)} = \frac{1/18 \cdot 1/3}{1/18 \cdot 1/3 + 1/38 \cdot 2/3 } = 0.5135 $$

(1/18 * 1/3)/(1/18 * 1/3 + 1/38 * 2/3)

# > (b) Compute P(“roulette”|“10”) assuming that there are twice as many craps games as roulette tables at the casino.
#



# # Study question 1.3.4
# > *Suppose we have three cards. Card 1 has two black faces, one on each side; Card 2 has two white faces; and Card 3 has one white face and one back face. You select a card at random and place it on the table. You find that it is black on the face-up side. What is the probability that the face-down side of the card is also black?*
#
#
# > *(a) Use your intuition to argue that the probability that the face-down side of the card is also
#  black is 0.5 .*
#
#
# $c_1: \ bb$  
# $c_2: \ ww$  
# $c_3: \ wb$  
#
# Intuition says that if the down facing is black, that means that we are down to two cards, $c_1$ and $c_3$. Given two cards we could argue that each has 50% to be the card. If it is $c_1$ then the results of down will be $b$ and if $c_3$ it will be $w$.   
#
# > *Why might it be greater than 0.5 ?*
#
# Perhaps we need to consider the fact that $c_1$ should get more weight considering it had to defeat $c_2$ to have black been showed up.  
#
# Using the 100 doors Monty Hall analogy, if we change the questions slightly to have a scenario  
#
# $c_A: \ bb$  
# $c_B: \ ww$  
# $c_C: \ ww$  
# $c_D: \ ww$  
# $c_E: \ ww$  
# ...  
# $c_Y: \ ww$  
# $c_Z: \ wb$,  
# our intuition now dictates to favour $c_A$ over $c_Z$.   
#
# > (b) *Express the probabilities and conditional probabilities that you find easy to estimate (for example, P(CD = Black)), in terms of the following variables:
# I = Identity of the card selected (Card 1, Card 2, or Card 3) CD = Color of the face-down side (Black, White)
# CU = Color of the face-up side (Black, White)
# Find the probability that the face-down side of the selected card is black, using your estimates above.*   
#
# I use slightly different notation.   
#
# $P(\text{card}_i) = \frac{1}{3} = P(c_1), P(c_2), P(c_3)$  
#
# $P(up=b)=P(down=b) = \sum_{c_i}P(up=b|c_i)P(c_i) =\\ P(up=b|c_1)P(c_1) + P(up=b|c_2)P(c_2) + P(up=b|c_3)P(c_3)=\\ 1 * \frac{1}{3} + \frac{1}{2} * \frac{1}{3} = \frac{1}{2}$
#
#
# $$P(down=b|up=b)= P(bb | up=b) = P(c_1|up=b)=$$  
# $$\frac{P(up=b|c_1)P(c_1)}{P(up=b)} = \\ \frac{1 \times 1/3}{1/2} = \frac{2}{3}$$

# I also tried this approach, but it is trivial since $P(up=b)=P(down=b)\equiv Y$:  
#
# $$P(down=b|up=b) = \frac{P(up=b|down=b)P(down=b)}{P(up=b)}$$  
#  
# $$\rightarrow X = \frac{X Y}{Y}$$
#
#

# > (c) *Use Bayes’ theorem to find the correct probability of a randomly selected card’s back
# being black if you observe that its front is black?*
#
#




# # Study question 1.3.5: Monty Hall Switch Bayes Benefit Proof
# Monty Hall
#
# > *Prove, using Bayes’ theorem, that switching doors improves your chances of winning the car in the Monty Hall problem.*
#
# The clue is in page W.  
#
# $X$ - the chosen door  
# $Y$ - the door with the car  
# $Z$ - the door opened by the host   
#
# Without loss of generality, we need to solve for   
# $$P(Y=B| X=A, Z=C) > P(Y=A| X=A, Z=C)$$  
#
# Using Bayes' Theorem  
#
# $P(Y=B| X=A, Z=C) = \frac{P(X=A, Z=C | Y=B)P(Y=B)}{P(X=A, Z=C)}$    
# $P(Y=A| X=A, Z=C) = \frac{P(X=A, Z=C | Y=A)P(Y=A)}{P(X=A, Z=C)}$   
#
# Most comonents here are equal so we need to prove:  
# $$P(X=A, Z=C | Y=B) > P(X=A, Z=C | Y=A)$$ 
#
# In the case where $Y=B$, the host has only one choice.  
# In the case where $Y=A$, the host has two choices.   
#
# $$P(X=A, Z=C | Y=B) = 2 \times P(X=A, Z=C | Y=A)$$ 



# # Study question 1.3.6
# > (a) *Prove that, in general, both $𝜎_{XY}$ and $𝜌_{XY}$ vanish when $X$ and $Y$ are independent. [Hint: Use Eqs. (1.16) and (1.17).]*
#
# $X \perp \!\!\! \perp Y \rightarrow E(X,Y) = E(X)E(Y)$  
# So if 
# $$\sigma_{XY} \equiv E[(X-E(X))(Y-E(Y))]$$  
# then   
# $\sigma_{X \perp \!\! \perp Y} = E[X \cdot Y - X\cdot E(Y) - Y\cdot E(X) + E(X)E(Y)]= \\ E(X)E(Y) - E(X)E(Y) - E(X)E(Y) + E(X)E(Y) = 0$

# > (b) *Give an example of two variables that are highly dependent and, yet, their correlation coefficient vanishes.*
#
#



# # Study question 1.3.7
# > *Two fair coins are flipped simultaneously to determine the payoffs of two players in the town’s casino. Player 1 wins a dollar if and only if at least one coin lands on head. Player 2 receives a dollar if and only if the two coins land on the same face. Let $X$ stand for the payoff of Player 1 and $Y$ for the payoff of Player 2.*
#
# > (a) *Find and describe the probability distributions $P(x), \ P(y), \ P(x,y), \ P(y|x), \ P(x|y)$*
#
# Assuming Heads=1, Tails=0:  
#
# | A | B | X | Y |
# | --- | --- | --- | --- |
# |0|0| 0| 1
# |0|1| 1| 0
# |1|0| 1|0
# |1|1|1| 1
#
# Here we see that   
# $X = A \text{ OR } B$   
# $Y = A \text{ XNOR } B \equiv A\cdot B + \bar{A}\cdot\bar{B}$  
#
# |$X$|$P(X)$|
# | --- | --- |
# |$0$|$\frac{1}{4}$
# |$1$|$\frac{3}{4}$
#
# |$Y$|$P(Y)$|
# | --- | --- |
# |$0$|$\frac{1}{2}$
# |$1$|$\frac{1}{2}$
#
# |$X$|$Y$| $P(X,Y)$|
# | --- | --- | --- |
# |$0$|$0$|$0$
# |$0$|$1$|$\frac{1}{4}$
# |$1$|$0$|$\frac{1}{2}$
# |$1$|$1$|$\frac{1}{4}$
#
#
# |$X$|$Y$| $P(Y|X)$|
# | --- | --- | --- |
# |$0$|$0$|$0$
# |$0$|$1$|$1$
# |$1$|$0$|$\frac{2}{3}$
# |$1$|$1$|$\frac{1}{3}$
#
# Note that for $P(Y|X)$ the normalisation is at fixed $X$, i.e,    
# $P(Y=0|X=0) + P(Y=1|X=0) = 1$ and  
# $P(Y=0|X=1) + P(Y=1|X=1) = 1$
#
# |$X$|$Y$| $P(X|Y)$|
# | --- | --- | --- |
# |$0$|$0$|$0$
# |$0$|$1$|$\frac{1}{2}$
# |$1$|$0$|$1$
# |$1$|$1$|$\frac{1}{2}$  
#
# Note that for $P(X|Y)$ the normalisation is at fixed $Y$, i.e,    
# $P(X=0|Y=0) + P(X=1|Y=0) = 1$ and  
# $P(X=0|Y=1) + P(X=1|Y=1) = 1$

# > (b) *Using the descriptions in (a), compute the following measures:* 
#
# $E[X] = \sum_{x=0,1} X P(X) = 1 \cdot P(x=1) = \frac{3}{4}$  
# $E[Y] = \sum_{y=0,1} Y P(Y) = 1 \cdot P(y=1) = \frac{1}{2}$
#
# $E[Y|x=0] = \sum_{y=0,1} Y P(Y|x=0) = 1 \cdot P(y=1|x=0) = 1 \cdot 1 = 1$  
# $E[Y|x=1] = \sum_{y=0,1} Y P(Y|x=1) = 1 \cdot P(y=1|x=1) = 1 \cdot \frac{1}{3} = \frac{1}{3}$  
# $E[X|y=0] = \sum_{x=0,1} X P(X|y=0) = 1 \cdot P(x=1|y=0) = 1 \cdot \frac{1}{2} = \frac{1}{2}$   
# $E[X|y=1] = \sum_{x=0,1} X P(X|y=1) = 1 \cdot P(x=1|y=1) = 1 \cdot \frac{1}{2} = \frac{1}{2}$  
#
# below is incorrect ... missing $P(X)$ terms in sums ...
#
# $Var(X) = E[(X - \mu_X)^2 ] = E[ (X - \frac{3}{4})^2 ] = 
# \sum_{x=0,1} P(X)(X - \frac{3}{4})^2 = \sum_{x=0,1} (X^2 - \frac{3}{2}X + \frac{9}{16}) P(X)
# =  \frac{9}{16}\frac{1}{4} + (1 - \frac{3}{2} + \frac{9}{16}) \frac{3}{4} = \frac{9}{64} + \frac{1}{16} = \frac{13}{64} \approx 0.2$ 
#

# ## Study question 1.5.4
#
# > *Define the structural model that corresponds to the Monty Hall problem, and use it to describe the joint distribution of all variables.*
#
# $X$ - the chosen door  
# $Y$ - the door with the car  
# $Z$ - the door opened by the host  
#
# $$X\rightarrow Z \leftarrow Y$$
#
# $$P(X,Y,Z) = P(Z|X,Y)P(X)P(Y)$$
#
# Structural Model:   
#
# $U = \{X,Y\}, \ V=\{Z\}, \ F=\{f_Z\}$
#
# $D = \{A, B, C \}$
#
# $f_Z: 
# Z= \text{choose one of} \begin{cases}
#  D - \{Y\} \ \ \ \text{      if  X = Y},\\
#  D - \{X, Y\} \text{  if  X \ne Y}\\
# \end{cases}$
#
#
# For joint distributions we'll look at examples: 
#
# E.g, when $X=Y$   
# $P(Z=A|X=A, Y=A) = 0$    
# $P(Z=B|X=A, Y=A) = 1/2$   
# $P(Z=C|X=A, Y=A) = 1/2$   
#
# When $X\ne Y$
#
# $P(Z=A|X=A, Y=B) = 0$    
# $P(Z=B|X=A, Y=B) = 0$   
# $P(Z=C|X=A, Y=B) = 1$  
#

# +
df = pd.DataFrame({"X": (["A"] * 9) + (["B"] * 9) + (["C"] * 9) , "Y": ((["A"] * 3) + (["B"] * 3) + (["C"] * 3) )* 3, "Z": ["A", "B", "C"] * 9})

df["P(Z|X,Y)"] = None
p_x = 1./3
p_y = 1./3

df.loc[df.query("X == Y == Z").index, "P(Z|X,Y)"] = 0
df.loc[df.query("X == Y != Z").index, "P(Z|X,Y)"] = 0.5
df.loc[df.query("X != Y == Z").index, "P(Z|X,Y)"] = 0
df.loc[df.query("Z == X != Y").index, "P(Z|X,Y)"] = 0
df.loc[df.query("X != Y").query("Z != Y").query("Z != X").index, "P(Z|X,Y)"] = 1

df["P(X, Y, Z)"] = df["P(Z|X,Y)"] * p_x * p_y

print(f"Testing normalisation of P(X,Y,Z) {df['P(X, Y, Z)'].sum()}")

df
