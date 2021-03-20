# -*- coding: utf-8 -*-
import pandas as pd

# # Study question 1.3.2
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



