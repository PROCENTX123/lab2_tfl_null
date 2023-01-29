"""
CFG
Context-free grammar:
Rule
[S] -> [Ga][T]|[S][S]
[T] -> b|[S][Gb]
[Ga] -> a
[Gb] -> b

DFA
Edge
Regular grammar:
[S] -> abc[S]|d[F0]
[F0] -> b
"""
from primitives import NTerm, Term, Rule, Edge, EPSILON_SYMBOL, Epsilon
from typing import Union

from cfg import CFG
from dfa import DFA
import re


def _split_alt(s):
  return s.split("|")

def get_term_n_term(t):
  return NTerm(t) if len(t) > 1 else Term(t)

def split_terms_and_nterms(string):
  results = []
  split_list = [r for r in re.split(r'(\[[^\]]*\])', string) if r]
  for item in split_list:
    if not item.startswith('[') and len(item) > 1:
      results.extend(item)
    else:
      results.append(item)
  return results


def parse(input, is_cfg=False) -> Union[CFG, DFA]:
  lines = [l.strip() for l in input.split("\n") if l]
  if is_cfg:
    return parse_cfg(lines)
  else:
    return parse_dfa(lines)


def parse_cfg(input: list[str]):
  rules = []
  for rule_str in input:
    if rule_str:
      left, right = rule_str.split("->")
      left_nterm = NTerm(left)

      for r in _split_alt(right):
        r = r.strip()
        terms_nterms = split_terms_and_nterms(r)
        right_side = []
        for t in terms_nterms:
          if t:
            if t[0] == "[":
              right_side.append(NTerm(t))
            elif t[0] == EPSILON_SYMBOL:
              right_side.append(Epsilon())
            else:
              right_side.append(Term(t))
        rules.append(Rule(left_nterm, right_side))
  return CFG(rules)


def parse_dfa(input: list[str]):
  edges = set()
  for rule_str in input:
    if rule_str:
      # print(rule_str)
      left, right = rule_str.split("->")
      left_nterm = NTerm(left)

      for r in _split_alt(right):
        r = r.strip()
        if not left_nterm.is_final():
          front, back = r.split('[')
          term_symbols = [Term(n) for n in front]
          right_nterm = NTerm('[' + back)
          for t in term_symbols:
            edges.add(Edge(left_nterm, right_nterm, t))
        else:
          # print(r)
          terms_nterms = split_terms_and_nterms(r)
          # print(terms_nterms)
          term, n_term = None, NTerm()
          for t in terms_nterms:
            if t[0] == "[":
              n_term = NTerm(t)
            else:
              term = Term(t)
            if not (left_nterm.is_final() and n_term == NTerm()):
              edges.add(Edge(left_nterm, n_term, term))
  return DFA(edges)
