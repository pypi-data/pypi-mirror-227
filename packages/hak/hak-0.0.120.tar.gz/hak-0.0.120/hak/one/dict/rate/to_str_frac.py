from hak.one.dict.rate.make import f as rate
from hak.pxyf import f as pxyf
from hak.pf import f as pf

# __str__
f = lambda x: (
  f"{x['numerator']}"
  if x['denominator'] == 1 else
  f"{x['numerator']}/{x['denominator']}"
)

t_a = lambda: pxyf(rate(710, 113, {'a': 1}), '710/113', f)
t_b = lambda: pxyf(rate(2, 1, {'a': 1}), '2', f)

def t():
  if not t_a(): return pf('t_a failed')
  if not t_b(): return pf('t_b failed')
  return 1
