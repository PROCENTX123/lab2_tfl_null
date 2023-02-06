from primitives import NTerm, Term, Rule, Edge
from typing import List

class DFA:
  start_state = "[S]"
  final_state = "[F0]"

  def __init__(self, edges: List[Edge]):
    self.edges = edges
    states = []
    for edge in edges:
      states.append(edge._from)
      states.append(edge._to)
    self.states = set(states)


  def add_state(self, state: NTerm):
    self.states.add(state)

  def add_edge(self, e: Edge):
    self.edges.add(e)

  def __repr__(self):

    return f"States: {self.states}\n" + "\n".join([str(r) for r in self.edges])
    # return "States:\n" + str(self.states) + "\n" + "Edges:\n" + str(self.edges)
