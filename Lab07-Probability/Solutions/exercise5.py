
p_toothache = 0.108+0.016+0.012+0.064
print(p_toothache)

p_cavity = 0.108+0.012+0.072+0.008
print(p_cavity)

# the symbol ^ means "and"
# the symbol v means "or"
# the symbol ~ means "not"
# the symbol | means "given"
# the symbol = means "equal to"
# the symbol -> means "implies"
# the symbol <-> means "if and only if"

p_toothache_and_cavity = 0.108+0.012
print(p_toothache_and_cavity)

p_toothache_or_cavity = p_toothache + p_cavity - p_toothache_and_cavity
print(p_toothache_or_cavity)

p_toothache_given_cavity = p_toothache_and_cavity / p_cavity
print(p_toothache_given_cavity)

p_toothache_and_cavity = 0.108+0.012
print(p_toothache_and_cavity)

p_toothache_and_catch = 0.108 + 0.016
p_cavity_and_toothache_and_catch = 0.108
p_cavity_given_toothache_catch = p_cavity_and_toothache_and_catch / p_toothache_and_catch
print(p_cavity_given_toothache_catch)

p_cavity_and_catch = 0.108 + 0.072
p_toothache_given_cavity_catch = 0.108 / p_cavity_and_catch
print(p_toothache_given_cavity_catch)

# Once we know the person has a cavity, knowing whether the probe catches does not change the likelihood of a toothache. That is what conditional independence means: the variables are unrelated once a third variable is known.
# In this case, knowing whether the probe catches does not change the likelihood of a toothache once we know the person has a cavity.
# Yes, toothache is conditionally independent of catch given cavity.