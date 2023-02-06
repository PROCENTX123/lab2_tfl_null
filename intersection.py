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

# def check_inter_triplets(triplet, inter_lst):
#   check = any([
#     (not isinstance(triplet.right[0], Term) and triplet.right[0] != i.left)
#     or
#     (not isinstance(triplet.right[1], Term) and triplet.right[1] != i.left)
#     for i in inter_lst
#   ])
#
#   return check

# def check_inter_triplets(triplet, inter_lst):
#   triplet_0, triplet_1 = triplet[0], triplet[1]
#   found_0 = False
#   for i in inter_lst:
#     if i.left == triplet_0:
#       found_0 = True
#   found_1 = False
#   for i in inter_lst:
#     if i.left == triplet_1:
#       found_1 = True
#
#   return not (found_0 and found_1)

def check_inter_triplets(triplet, inter_lst):
  return any([triplet.right[0] != i.left or triplet.right[0] != i.left for i in inter_lst])



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
    # fixme | set(iter)
    total_set = truplets #| set(inter)
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

def resolve_inter(inter, triplets_holders):
  result = []
  inter_to_resolve = dict()
  triplets_holders = list(triplets_holders)
  for i in inter:
    found = False
    for t_h in triplets_holders:
      if t_h.left == i.left:
        found = True
        break
    if not found:
      inter_to_resolve[i.left] = i.term
  for i in range(len(triplets_holders)):
    temp = []
    t_h_curr = triplets_holders[i]
    for triplet in t_h_curr.right:
      if triplet in inter_to_resolve:
        temp.append(inter_to_resolve[triplet])
      else:
        temp.append(triplet)
    result.append(TripletHolder(t_h_curr.left, temp))
  return result


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
      if not (check_inter_triplets(triplet, inter_lst)):
        filtered_triplets_copy.remove(triplet)
        changed = True
      elif not (check_existing_triplets(triplet, filtered_triplets, inter_lst)):
        filtered_triplets_copy.remove(triplet)
        changed = True
      elif not is_valid_duplicate(triplet, filtered_triplets, inter_lst):
        filtered_triplets_copy.remove(triplet)
        changed = True
    
    
  return filtered_triplets



def find_transitions(edges):
    def dfs(start, vertex, graph, visited, transitions):
        visited.add(start)
        # print(start, vertex)
        for neighbor in graph.get(vertex, []):
          transitions.add((start, neighbor))
          if neighbor not in visited:
              transitions.add((vertex, neighbor))
              dfs(start, neighbor, graph, visited, transitions)

    graph = {}
    edges_removed, edges_left = [e for e in edges if e[0] == e[1]], [e for e in edges if e[0] != e[1]]
    for start, end in edges_left:
        if start not in graph:
            graph[start] = []
        graph[start].append(end)

    visited = set()
    transitions = set()
    for vertex in graph:
        visited = set()
        dfs(vertex, vertex, graph, visited, transitions)
    edges_removed = set(edges_removed)

    return transitions | edges_removed

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
              
  triplets = first_check(triplets, inter, find_transitions(get_reachable_edges(dfa)))
  inter = filter_intersection(inter, triplets)
  triplets = set(resolve_inter(inter, triplets))
  return triplets | inter


# < [S], [S], [B]> -> < [S], [Ga], [S]> < [S], [T], [B]>
