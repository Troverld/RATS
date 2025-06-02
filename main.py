from AI1 import AI1
from AI2 import AI2
from AI3 import AI3

identifier=AI1()

question = identifier.identify_from_input("pcp.png")
answer = identifier.identify_from_input("pcp.pdf")

print("Question:", question)
print("Answer:", answer)

# question = r"""
# Recall that a context-free grammar \( G \) is called ambiguous if there is a string in \( L(G) \) that has two distinct parse trees. Let \( AMBIG_{CFG} = \{\langle G \rangle : G \text{ is an ambiguous CFG}\} \). Show that \( AMBIG_{CFG} \) is undecidable.
# """

# answer = r"""
# We present a many-one reduction from $PCP$ to $AMBIG_{CFG}$.

# For a $PCP$ instance $\left\{\left(a_{i}, b_{i}\right)\right\}_{i=1}^{n}$ where $a_{i}, b_{i} \in \Sigma^{*}$, we construct a context-free grammar (CFG) $G = \left(V, \Sigma', R, S\right)$ as follows:

# - $V = \{S, A, B, A', B'\}$.
# - $\Sigma' = \Sigma \cup [1,n]$. Each integer is treated as a distinct symbol.
# - The set of rules $R$ includes:
#   - $S \rightarrow A' \mid B'$.
#   - $A \rightarrow \epsilon$, $B \rightarrow \epsilon$.
#   - For each $1 \leq i \leq n$:
#     - $A \rightarrow i A a_i$.
#     - $B \rightarrow i B b_i$.
#     - $A' \rightarrow i A a_i$.
#     - $B' \rightarrow i B b_i$.

# The grammar $G$ does not accept the empty string $\epsilon$. For any string $w = st$ where $s \in [1,n]^+$ and $t \in \Sigma^*$, $G$ accepts $w$ by initially expanding $S$ to $A'$ if and only if $t = a_{s_{|s|}} \ldots a_{s_1}$; similarly, $G$ accepts $w$ by initially expanding $S$ to $B'$ if and only if $t = b_{s_{|s|}} \ldots b_{s_1}$. Consequently, $G$ accepts $w$ through two distinct parse trees precisely when the $PCP$ instance is a YES instance.
# """

patitor = AI2()

points = patitor.partitioning_points(question, answer)

print(points)

# points = r"""
# {
#     "points": [
#         {
#             "key": "Many-one reduction from PCP to AMBIG_CFG",
#             "description": "We present a many-one reduction from $PCP$ to $AMBIG_{CFG}$. For a $PCP$ instance $\left\{\left(a_{i}, b_{i}\right)\right\}_{i=1}^{n}$ where $a_{i}, b_{i} \in \Sigma^{*}$, we construct a context-free grammar (CFG) $G = \left(V, \Sigma', R, S\right)$."
#         },
#         {
#             "key": "Definition of CFG components: variables and alphabet",
#             "description": "- $V = \{S, A, B, A', B'\}$. - $\Sigma' = \Sigma \cup [1,n]$. Each integer is treated as a distinct symbol."
#         },
#         {
#             "key": "Production rules including start, epsilon, and indexed derivations",
#             "description": "The set of rules $R$ includes: - $S \rightarrow A' \mid B'$. - $A \rightarrow \epsilon$, $B \rightarrow \epsilon$. - For each $1 \leq i \leq n$: - $A \rightarrow i A a_i$. - $B \rightarrow i B b_i$. - $A' \rightarrow i A a_i$. - $B' \rightarrow i B b_i$."
#         },
#         {
#             "key": "Ambiguity equivalence to PCP solution via string acceptance conditions",
#             "description": "The grammar $G$ does not accept the empty string $\epsilon$. For any string $w = st$ where $s \in [1,n]^+$ and $t \in \Sigma^*$, $G$ accepts $w$ by initially expanding $S$ to $A'$ if and only if $t = a_{s_{|s|}} \ldots a_{s_1}$; similarly, $G$ accepts $w$ by initially expanding $S$ to $B'$ if and only if $t = b_{s_{|s|}} \ldots b_{s_1}$. Consequently, $G$ accepts $w$ through two distinct parse trees precisely when the $PCP$ instance is a YES instance."
#         }
#     ]
# }
# """

index=int(input())
prompt=input()

addresser=AI3()
addresser.address(question, answer, points, index, prompt)

#for point in points:
#    print(f"Key: {point['key']}, Description: {point['description']}")