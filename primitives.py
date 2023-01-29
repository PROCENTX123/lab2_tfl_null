import re
from typing import Union, List


def _strip_brackets(s):
  return re.findall(r'\[(.*?)\]', s.strip())


class NTerm:

  def __init__(self, label: str = "[]"):
    # print(label)
    self.label = _strip_brackets(label)[0]

  def __repr__(self):
    return f"[{self.label}]" if self.label else ""

  def is_final(self):
    return self.label == "F0"

  def is_start(self):
    return self.label == "S"

  def __eq__(self, other):
    return self.label == other.label

  def __hash__(self):
    return hash(str(self))


class Term:

  def __init__(self, symb: str):
    self.symb = symb

  def __repr__(self):
    return self.symb

  def __eq__(self, other):
    return self.symb == other.symb

  def __hash__(self):
    return hash(str(self))


class Rule:

  def __init__(self, left: NTerm, right: List[Union[NTerm, Term]]):
    self.left = left
    self.right = right

  def __repr__(self):
    right_j = "".join([str(r) for r in self.right])
    return f"{self.left} -> {right_j}"

  def __eq__(self, other):
    return (self.left == other.left) and (self.right == other.right)

  def __hash__(self):
    return hash(str(self))


class Edge:
  _from: NTerm
  _to: NTerm
  sym: Term

  def __init__(self, e_from: NTerm, e_to: NTerm, sym: Term):
    self._from = e_from
    self._to = e_to
    self.sym = sym

  def __repr__(self):
    return f"{self._from} -> {self.sym}{self._to}"
    # return str([self.e_from, self.e_to, self.sym])

  def __eq__(self, other):
    return (self._from == other._from) and (self._to == other._to) and (self.sym == other.sym)

  def __hash__(self):
    return hash(str(self))

EPSILON_SYMBOL = 'ε'


class Epsilon:

  def __init__(self):
    self.symb = EPSILON_SYMBOL

  def __repr__(self):
    return self.symb

  def __eq__(self, other):
    return (self.symb == other.symb)

  def __hash__(self):
    return hash(str(self))
