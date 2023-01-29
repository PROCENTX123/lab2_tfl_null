from primitives import NTerm, Term, Rule, Edge, Epsilon
from collections import defaultdict
import itertools
import copy


def print_rules(rules):
  for rule in rules:
    print(rule)
  print(len(rules))


class CFG:

  def __init__(self, rules: list[Rule]):
    self.rules = rules
    print("Assignment")
    print_rules(self.rules)

    split_long_rules = []
    for r in self.rules:
      long_ = self.split_long_rule(r)
      split_long_rules.extend(long_)
    print("split_long_rules")
    print_rules(split_long_rules)
    # print_rules(len(split_long_rules))

    # raise
    no_long_rules = self.remove_long_rule(split_long_rules)
    print_rules(no_long_rules)
    print("no_long_rules")

    parents, children = self.build_tree(no_long_rules)
    eps_gen_nterms = self.NTerm_eps_generating(children)
    # print("EPS GEN")
    # print(eps_gen_nterms)
    no_eps_rules = self.construct_all_combinations(eps_gen_nterms,
                                                   no_long_rules)
    print_rules(no_eps_rules)
    print("no_eps_rule")

    parents, children = self.build_tree(no_eps_rules)
    # print(children)
    chain_rules = self.make_chain(children, no_eps_rules)
    print_rules(chain_rules)
    print("no_chain_rule")
    # chain_rules = [
    #   Rule(NTerm('[S]'), [Term('a'), NTerm('[S1]')]),
    #   Rule(NTerm('[S]'), [Term('a'), NTerm('[Z]')]),
    #   Rule(NTerm('[X]'), [Term('a'), NTerm('[Y]')]),
    #   Rule(NTerm('[X]'), [Term('b'), NTerm('[Y]')]),
    #   Rule(NTerm('[Y]'), [Term('a'), NTerm('[Y]')]),
    #   Rule(NTerm('[Y]'), [Term('b'), NTerm('[Y]')]),
    #   Rule(NTerm('[Y]'), [Term('c'), Term('c')]),
    #   Rule(NTerm('[Z]'), [NTerm('[Z]'), NTerm('[X]')]),
    #   Rule(NTerm('[S1]'), [NTerm('[X]'), NTerm('[S2]')]),
    #   Rule(NTerm('[S1]'), [Term('y'), NTerm('[X]')]),
    #   Rule(NTerm('[S1]'), [Term('y')]),
    #   Rule(NTerm('[S2]'), [Term('y'), NTerm('[X]')]),
    #   Rule(NTerm('[S2]'), [Term('y')]),
    # ]

    no_unused_rules = self.del_unused_symbols(chain_rules)
    print_rules(no_unused_rules)
    print("no_unused_rules")

    replacement_rules = self.replace_terms(no_unused_rules)
    print_rules(replacement_rules)
    print("Done")

  def get_nterm(self, rules):
    list_nterm = set()
    for rule in rules:
      list_nterm.add(rule.left)
      for r in rule.right:
        if isinstance(r, NTerm):
          list_nterm.add(r)
    return list(list_nterm)

  def __repr__(self):
    return "\n".join([str(r) for r in self.rules])

  # def get_term(self, rules: list[Rule]):
  #   list_term = []
  #   for rule in rules:
  #     pass


  def split_long_rule(self, rule: Rule):
    new_rules = list()
    # print("RULE BEGIN")
    # print(rule)
    len_right_rule = len(rule.right)
    list_new_nterms = [rule.left] + self.new_NTerms_in_long_rule(
      rule.left, len_right_rule)

    if len_right_rule == 1:
      new_rules.append(rule)
    for itter in range(len_right_rule - 1):
      if itter != len_right_rule - 2:
        new_rule = Rule(list_new_nterms[itter],
                        [rule.right[itter], list_new_nterms[itter + 1]])
      else:
        new_rule = Rule(list_new_nterms[itter], rule.right[-2:])
      new_rules.append(new_rule)
    # print("RULE END")
    # print(new_rules)
    return set(new_rules)

  def new_NTerms_in_long_rule(self, left_rule_label, len_right_rule):
    new_nterms = []
    for i in range(len_right_rule - 2):
      new_nterm_label = f"[{left_rule_label.label}{i+1}]"
      new_nterm = NTerm(new_nterm_label)
      new_nterms.append(new_nterm)
    return new_nterms

  def remove_long_rule(self, rules):
    new_rules = []
    for i in range(len(rules)):
      rule = rules[i]
      if len(rule.right) > 2:
        rule_split = self.split_long_rule(rule)
        new_rules.extend(rule_split)
      else:
        new_rules.append(rule)
    return set(new_rules)

  def NTerm_eps_generating(self, children):
    is_eps_generate = defaultdict(bool)
    for c in children:
      is_eps_generate[c] = False

    found = True
    parent_keys = list(is_eps_generate.keys())
    while found:
      found = False
      for key in parent_keys:
        all_children_eps = self.are_all_my_children_eps(
          key, children.get(key), is_eps_generate)
        if ((Epsilon() in children.get(key)) or
            (all_children_eps)) and not is_eps_generate[key]:
          is_eps_generate[key] = True
          found = True
    return [k for k, v in is_eps_generate.items() if v]

  def construct_all_combinations(self, eps_gen_nterms, rules):
    new_rules = []
    for rule in rules:
      # print("BEGIN RULE")
      # print(rule)
      right = rule.right
      if not (len(rule.right) == 1 and isinstance(rule.right[0], Epsilon)):
        comb_seq = [
          1 if (isinstance(n, Term) or n not in eps_gen_nterms) else 0
          for n in right
        ]
        count_zeros = len([k for k in comb_seq if k == 0])
        lst = list(itertools.product([0, 1], repeat=count_zeros))

        tails = []
        for c in lst:
          c = list(c)
          c_ = []
          for i in range(len(comb_seq)):
            if comb_seq[i] == 1:
              c_.append(right[i])
            else:
              is_present = c[0]
              if is_present:
                c_.append(right[i])
              del c[0]
          if c_:
            tails.append(c_)
        temp_ = []
        for tail in tails:
          temp_.append(Rule(rule.left, tail))
        # print(temp_)
        new_rules.extend(temp_)
    return set(new_rules)

  def make_chain(self, children, extended_rules):
    list_nterm = self.get_nterm(extended_rules)
    tuples = set(((n_term, n_term) for n_term in list_nterm))
    found = True
    while found:
      found = False
      for rule in extended_rules:
        left_nterm = rule.left
        tail = rule.right
        if len(tail) == 1 and isinstance(tail[0], NTerm):
          r = tail[0]
          for chain_candidate in list(tuples):
              if chain_candidate[1] == left_nterm:
                  pair = (chain_candidate[0], r)
                  if not pair in tuples:
                      tuples.add(pair)
                      found = True

    result = set()
    for rule in extended_rules:
        left = rule.left
        tail = rule.right
        if not (len(tail) == 1 and isinstance(tail[0], NTerm) and (left, tail[0]) in tuples):
            result.add(rule)
    copy_rules = copy.deepcopy(result)
    for chain_candidate in tuples:
        for rule in copy_rules:
            left = rule.left
            tail = rule.right
            if chain_candidate[1] == left:
                result.add(Rule(chain_candidate[0], tail))
    return set(result)

  def del_unused_symbols(self, rules):
    set_of_gen = set()
    found = True
    while found:
      found = False
      for rule in rules:
        # print("RULE BEGIN")
        # print(rule)
        # print([type(c) for c in rule.right])
        if all([not isinstance(c, NTerm) for c in rule.right]):
          if not rule.left in set_of_gen:
            set_of_gen.add(rule.left)
            found = True
        elif all([c in set_of_gen for c in rule.right
                  if isinstance(c, NTerm)]):
          if not rule.left in set_of_gen:
            set_of_gen.add(rule.left)
            found = True
    res_rules = []
    for rule in rules:
      right_nterms = [c for c in rule.right if isinstance(c, NTerm)]
      if all([rterm in set_of_gen for rterm in right_nterms]):
        res_rules.append(rule)
    return set(res_rules)

  def replace_terms(self, rules):
    new_rules = []
    terminal_replace = {}
    counter = 1
    for rule in rules:
      terms = [c for c in rule.right if isinstance(c, Term)]
      if len(rule.right) == 2 and terms:
        # if terms:
        if len(terms) == 2:
          # never executes because 'cc' is one term
          t = terms[0]
          if not terminal_replace.get(t):
            new_nterm = NTerm(f"[{t.symb.upper()}{counter}]")
            terminal_replace[t] = new_nterm
          else:
            new_nterm = terminal_replace[t]
          new_rules.extend(
            [Rule(new_nterm, [t]),
             Rule(rule.left, [new_nterm, new_nterm])])
        elif len(terms) == 1:
          t_i = 0 if isinstance(rule.right[0], Term) else 1
          nt_i = 1 - t_i
          t = rule.right[t_i]
          if not terminal_replace.get(t):
            new_nterm = NTerm(f"[{t.symb.upper()}{counter}]")
            terminal_replace[t] = new_nterm
          else:
            new_nterm = terminal_replace[t]
          new_rules.extend([
            Rule(new_nterm, [t]),
            Rule(rule.left, [new_nterm, rule.right[nt_i]])
          ])
        counter += 1
      else:
        new_rules.append(rule)
    return set(new_rules)

  def build_tree(self, rules):
    child = {}
    parent = {}
    for rule in rules:
      left = rule.left
      rights = rule.right
      if left not in child:
        child[left] = set(rights)
      else:
        child[left].update(rights)
      for right in rights:
        if right not in parent:
          parent[right] = set([left])
        else:
          parent[right].add(left)
    return parent, child

  def are_all_my_children_eps(self, me, my_children, is_eps_generate):
    children_not_eps = [c for c in my_children if not is_eps_generate[c]]
    # if not children_not_eps or (len(children_not_eps) == 1 and
    #                             (isinstance(children_not_eps[0], NTerm)
    #                              and children_not_eps[0] == me)):
    if not children_not_eps:
      return True
    return False
