import math

space_m = 32
m = 31

space_H0 = math.log2(space_m)
H0 = math.log2(m)

H_space_mono = 4.352755973064407
H_space_bi_o = 7.909908859755906
H_space_bi = 3.1651231291096873

H_mono = 4.4529625721687855
H_bi_o = 8.26007225640357
H_bi = 3.2801519521547213

print("R_space_mono:", H_space_mono/space_H0)
print("R_space_bi_o:", H_space_bi_o/space_H0)
print("R_space_bi:", H_space_bi/space_H0)

print("R_mono:", H_mono/H0)
print("R_bi_o:", H_bi_o/H0)
print("R_bi:", H_bi/H0)

