from cfg import CFG
from dfa import DFA
from primitives import Term, NTerm
import copy
from typing import List

class Triplet():
  def __init__(self, p: NTerm, n_term: NTerm, q: NTerm):
    self.p = p
    self.q = q
    self.n_term = n_term

  def __eq__(self, other):
    return self.q == other.q and self.p == other.p and self.n_term == other.n_term

  def __hash__(self):
    return hash(str(self))
    
  def __repr__(self):
    return f"< {self.p}, {self.n_term}, {self.q}>"

class TripletHolder:
  def __init__(self, left: Triplet, right: List[Triplet]):
    self.left = left
    self.right = right

  def __eq__(self, other):
    return self.left == other.left and self.right == other.right
    
  def __repr__(self):
    res = ""
    for r in self.right:
      res += str(r) + ' '
    return f"{self.left} -> " + res + " \n"

  def __hash__(self):
    return hash(str(self))

class Intersection():

  def __init__(self, state_from, n_term, state_to, term):
    self._from = state_from
    self._to = state_to
    self.n_term = n_term
    self.term = term
    self.left = Triplet(self._from, self.n_term, self._to)
    
  def __repr__(self):
    return f"< {self._from}, {self.n_term}, {self._to} > -> {self.term} \n"

def check_existing_triplets(triplet, triplets, inter):
  triplets = list(triplets)
  total_count = len(triplets) + len(inter)
  right_found, left_found = False, False
  for i in range(total_count):
    search_candidate = triplets[i] if i < len(triplets) else inter[i - len(triplets)]
    if (triplet.right[0] == search_candidate.left):
      left_found = True
    if ((triplet.right[1] == search_candidate.left)):
      right_found = True
    if (right_found and left_found):
      break
  return right_found and left_found

def get_reachable_edges(dfa):
  return [
    (e._from, e._to)
    for e in dfa.edges
  ]

def is_valid_duplicate(triplet, truplets, inter):
  if triplet.left == triplet.right[0] == triplet.right[1]:
    total_set = truplets | set(inter)
    for t in total_set:
      if t.left == triplet.left and not (t.right == triplet.right):
        return True
  else:
    return True
  return False

def filter_unreachable_truplets(triplets, reachable_edges):
  res = set()
  for t in triplets:
    t_edge = (t.left.p, t.left.q)
    if t_edge in reachable_edges:
      res.add(t)
  return res

def filter_intersection(inter, triplets):
  res_inter = set()
  for i in inter:
    for t in triplets:
      if i.left in t.right:
        res_inter.add(i)
  return res_inter
  
# pseudocod
def first_check(triplets, inter, reachable_edges):
  inter_lst = list(inter)

  # filter using DFA
  filtered_1 = filter_unreachable_truplets(
      triplets,
      reachable_edges
  )
  
  filtered_triplets = set(filtered_1)
  filtered_triplets_copy = copy.deepcopy(filtered_triplets)
  changed = True
  while changed:
    changed = False
    filtered_triplets = copy.deepcopy(filtered_triplets_copy)
    # print(f"Left triplets: {len(filtered_triplets)}")
    for triplet in filtered_triplets:
      if not (check_existing_triplets(triplet, filtered_triplets, inter_lst)):
        filtered_triplets_copy.remove(triplet)
        changed = True
      if not is_valid_duplicate(triplet, filtered_triplets, inter_lst):
        filtered_triplets_copy.remove(triplet)
        changed = True
    
    
  return filtered_triplets

def make_intersection(cfg: CFG, dfa: DFA):
  inter = set()
  composite_rules = set()
  first_set_nont = set()
  for r in cfg.rules:
    if len(r.right) == 1 and isinstance(r.right[0], Term):
      first_set_nont.add(r.left)
      term = r.right[0]
      for edge in dfa.edges:
        if edge.sym == term:
          inter.add(Intersection(edge._from, r.left, edge._to, term))
    else:
      composite_rules.add(r)

  terminal_only_nonterms = set()
  for nont in first_set_nont:
      for r in composite_rules:
          if r.left == nont:
              break
      else:
          terminal_only_nonterms.add(nont)
  triplets = set()
  for rule in composite_rules:
    for p in dfa.states:
        for q in dfa.states:
            for z in dfa.states:
              left_triplet = Triplet(p, rule.left, q)
              right1_triplet = Triplet(p, rule.right[0], z)
              right2_triplet = Triplet(z, rule.right[1], q)
              triplets.add(TripletHolder(left_triplet, [right1_triplet, right2_triplet]))
              
  triplets = first_check(triplets, inter, get_reachable_edges(dfa))
  inter = filter_intersection(inter, triplets)
  return triplets | inter
