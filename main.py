from parser import parse_cfg, parse
from intersection import make_intersection
# fixme CFG with double states e.g. [D][D]
#
# input_cfg = """
# [S] -> [Ga][T]|[S][S]
# [T] -> b|[S][Gb]
# [Ga] -> a
# [Gb] -> b
# """

# output_cfg = """
# [S] -> [Ga][T]
# [S] -> [S][S]
# [T] -> b
# [T] -> [S][Gb]
# [Ga] -> a
# [Gb] -> b
# """.strip()

# input_dfa = """
# [S] -> a[S]|b[F0]
# [F0] -> b|b[F0]
# """

# test_dfa = parse(input_dfa, False)
# print("TEST Output: {}\n".format(str(test_dfa)),
#       "CORRECT Output: {}\n".format(input_dfa))

# test_cfg = parse(input_cfg, True)


# for i in make_intersection(test_cfg, test_dfa):
#   # pass
#   print(i)

# print("TEST Output: {}\n".format(str(parse(input_cfg, True))),
#       "CORRECT Output: {}\n".format(output_cfg))

# print("TEST Output: {}\n".format(str(parse(input_dfa, False))),
#       "CORRECT Output: {}\n".format(input_dfa))

# input_cfg1 = """
# [S] -> a[X]b[X]
# """

# print("TEST Output: {}\n".format(str(parse(input_cfg1, True))),
#       "CORRECT Output: {}\n".format(input_cfg1))

# test_cfg = parse(input_cfg1, True)


# # print("Testing new_NTerms_in_long_rule")
# # Test1
# # print(test_cfg.new_NTerms_in_long_rule(test_cfg.rules[0].left, 4))

# print("Testing split_long_rule")
# print("TEST Output:")
# for r in test_cfg.rules:
# # print(r.right)
#   for r_ in test_cfg.split_long_rule(r):
#     print(r_)

# print("Correct Output:")
# print("""
# S -> aS0
# S0 -> XS1
# S -> bX
# """)


#Test remove_long_rules
# input_cfg2 = """
# [S] -> a[X]b[X]|a[Z]
# [X] -> a[Y]|b[Y]
# [Y] -> [X]|cc
# [Z] -> [Z][X]
# """

# test_cfg = parse(input_cfg2, True)
# test_cfg.remove_long_rule()
# print("TEST Output: {}\n".format(str(test_cfg)),
#       "CORRECT Output: {}\n".format(input_cfg2))


# Testing Set/Hash
# from primitives import Rule, NTerm
# a = Rule(
#   NTerm("[S]"), [NTerm("[S]"), NTerm("[S]")]
# )
# b = Rule(
#   NTerm("[S]"), [NTerm("[S]"), NTerm("[S]")]
# )
# print(a == b)
# print([a, b])
# print(set([a, b]))

#Testing build tree
# input_cfg3 = """
# [S] -> [A][B][C]d
# [A] -> a|ε
# [B] -> [A][C]
# [C] -> c|ε
# """


# test_cfg = parse(input_cfg3, True)


# parent, children = test_cfg.build_tree()
# for k, v in parent.items():
#   print(k, v)
# for k, v in children.items():
#   print(k, v)








# test tracking
# input_cfg4 = """
# [S] -> [A][B][C][S]
# [S] -> [S][D]
# [A] -> ε
# [B] -> [A][C]
# [C] -> ε
# [D] -> d
# """

# test for all() vs any()
# input_cfg5 = """
# [S] -> [A][B][C]
# [S] -> [D][S]
# [A] -> ε
# [B] -> [A][C]
# [C] -> c
# [D] -> d
# """

# test tracking
# input_cfg6 = """
# [S] -> [A][B][C][S]
# [S] -> [S][D]
# [A] -> ε
# [B] -> [A][C]
# [C] -> ε
# [D] -> d
# """


# test_cfg = parse(input_cfg6, True)
# parents, children = test_cfg.build_tree()
# # for k, v in parent.items():
# #   print(k, v)
# for k, v in children.items():
#   print(k, v)
# # print(parents)
# print(test_cfg.NTerm_eps_generating(children))
#
# input_cfg7 = """
# [S] -> [A][B]d
# [A] -> a|ε
# [B] -> b
# """
#
# input_cfg8 = """
# [S] -> [A][B][C]d
# [A] -> a|ε
# [B] -> [A][C]
# [C] -> c|ε
# """

# test_cfg = parse(input_cfg8, True)
# parents, children = test_cfg.build_tree()
# for k, v in parent.items():
#   print(k, v)
# for k, v in children.items():
#   print(k, v)
# print(parents)
# eps_gen = test_cfg.NTerm_eps_generating(children)
# for t in test_cfg.construct_all_combinations(eps_gen):
#   print(t)


# A - 0
# B - 0
# C - 0
# S - 1

# A - 1
# B - 0
# C - 0
# S - 1


#test chain_rule
# input_cfg9 ="""
# [A] -> [B]|a
# [B] -> [C]|b
# [C] -> [D][D]|c
# """

# test_cfg = parse(input_cfg9, True)
# parents, children = test_cfg.build_tree()
# for k, v in children.items():
#   print(k, v)
# chain_set = test_cfg.make_chain(children, set())
# for i in list(chain_set):
#   print(i)

#test useles_rule
# input_cfg10= """
# [S] -> [A]c
# [A] -> [S][D]
# [D] -> a[D]
# [A] -> a
# """
# test_cfg = parse(input_cfg10, True)
# norm_set = test_cfg.del_unused_symbols()
# print(norm_set)

#
input_cfg11 = """
[S] -> a|a[S]
"""
# [S] -> a[S1]
# [X] -> a[Y]|b[Y]
# [Y] -> a[Y]|b[Y]|cc
# [S1] -> [X][S2]|y[X]|y
# [S2] -> y[X]|y


# test_cfg = parse(input_cfg11, True)
# for r in test_cfg.replace_terms(test_cfg.rules):
#   print(r)
# 1 000 1
# 1 100 1
# 1 010 1
# 1 001 1
# 1 110 1
# 1 101 1
# 1 110 1
# 1 111 1

# print(lst)


# input_final_cfg = """
# [S] -> a[X]b[X]|a[Z]
# [X] -> a[Y]|b[Y]|ε
# [Y] -> [X]|cc
# [Z] -> [Z][X]
# """

# test_cfg = parse(input_final_cfg, True)

input_cfg = ''
input_dfa = ''

with open('input.txt') as f:
  flag_dfa = False
  header = 0
  for line in f:
    if ':' in line:
      header += 1
      continue
    if line.isspace() == True:
      continue
    if header == 1:
      input_cfg = input_cfg + line
    else:
      input_dfa = input_dfa + line



#FINAL TEST
# input_cfg = """
# [S] -> [Ga][T]|[S][S]
# [T] -> b|[S][Gb]
# [Ga] -> a
# [Gb] -> b
# """


# input_dfa = """
# [S] -> a[S]|b[F0]
# [F0] -> b|b[F0]
# """

test_dfa = parse(input_dfa, False)
# print("TEST Output: {}\n".format(str(test_dfa)),
#       "CORRECT Output: {}\n".format(input_dfa))

test_cfg = parse(input_cfg, True)

for i in make_intersection(test_cfg, test_dfa):
  print(i)


