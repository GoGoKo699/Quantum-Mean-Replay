#!/usr/bin/env python3
"""Finite twirl and charged-macroblock checks; these do not prove a lower bound.

All randomness has a fixed seed. --check tolerates last-bit linear algebra
differences; it checks the stored cases and numerical tolerances, not a proof.
"""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import numpy as np
from numpy.polynomial import Polynomial
rng=np.random.default_rng(20261102)
Z=np.diag([1.,-1.]); I=np.eye(2)

def haar(d):
    q,r=np.linalg.qr(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))
    return q@np.diag(np.diag(r)/np.abs(np.diag(r))).conj()

def oracle(p,a,b,c):
    x,y=np.sqrt(1-p),np.sqrt(p)
    R=np.array([[x,-y],[y,x]],complex)
    U=(1j**c)*np.linalg.matrix_power(Z,a)@R@np.linalg.matrix_power(Z,b)
    return np.block([[I,np.zeros((2,4))],[np.zeros((2,2)),U,np.zeros((2,2))],[np.zeros((2,4)),U.conj().T]])

def apply_window(p, rho, interleaves, final_projector=None):
    out=np.zeros_like(rho,complex)
    for a in range(2):
      for b in range(2):
       for c in range(4):
        W=oracle(p,a,b,c)
        d=rho.copy()
        for V in interleaves:
            d=W@V@d@V.conj().T@W.conj().T
        out+=d/16
    if final_projector is None:return out
    return np.trace(final_projector@out).real

v=haar(6)[:,0]; rho=np.outer(v,v.conj()); vv=haar(6)[:,0]; P=np.outer(vv,vv.conj())
records=[]
for calls in range(1,7):
    inter=[haar(6) for _ in range(calls)]
    nodes=(1+np.cos(np.pi*(np.arange(calls+1)+.5)/(calls+1)))/2
    vals=[apply_window(p,rho,inter,P) for p in nodes]
    poly=Polynomial.fit(nodes,vals,calls,domain=[0,1])
    tests=np.r_[0,1,rng.uniform(0,1,40)]
    residual=max(abs(poly(p)-apply_window(p,rho,inter,P)) for p in tests)
    records.append({'same_source_calls':calls,'predicted_max_degree':calls,'max_residual':float(residual)})

# Explicit outcome-adaptive windows: measure after first call; a P branch retires
# after 1 call, complementary branch makes a second call then retires. Each is an
# unnormalized CP submap. Compose fresh independent windows in a h=2 macroblock.
Pstop=np.diag([1,0,1,0,1,0]).astype(complex); Pgo=np.eye(6)-Pstop
V1,V2=haar(6),haar(6)
def branches(p,rho):
    short=np.zeros_like(rho,complex);long=np.zeros_like(rho,complex)
    for a in range(2):
      for b in range(2):
       for c in range(4):
        W=oracle(p,a,b,c)
        t=W@V1@rho@V1.conj().T@W.conj().T
        short+=Pstop@t@Pstop/16
        t=Pgo@t@Pgo
        long+=W@V2@t@V2.conj().T@W.conj().T/16
    return short,long

def macro(p):
    short,long=branches(p,rho)
    # If first window used 2 calls, macro done. Else run a fresh window.
    second_short,second_long=branches(p,short)
    out=long+second_short+second_long
    assert abs(np.trace(out)-1)<1e-10
    return np.trace(P@out).real
nodes=(1+np.cos(np.pi*(np.arange(4)+.5)/4))/2
poly=Polynomial.fit(nodes,[macro(p) for p in nodes],3,domain=[0,1])
residual=max(abs(poly(p)-macro(p)) for p in np.r_[0,1,rng.uniform(0,1,40)])
records.append({'adaptive_macro_threshold':2,'max_actual_calls':3,'predicted_max_degree':3,'max_residual':float(residual)})

# Omitting the random source phases should remove the polynomial cancellation.
# This is a negative control, not another valid lower-bound argument.
inter=[haar(6) for _ in range(2)]
def untwirled(p):
    W=oracle(p,0,0,0)
    d=rho.copy()
    for V in inter:
        d=W@V@d@V.conj().T@W.conj().T
    return np.trace(P@d).real
nodes=(1+np.cos(np.pi*(np.arange(3)+.5)/3))/2
poly=Polynomial.fit(nodes,[untwirled(p) for p in nodes],2,domain=[0,1])
negative=max(abs(poly(p)-untwirled(p)) for p in np.linspace(0,1,41))
if not all(r['max_residual']<1e-10 for r in records):
    raise SystemExit('twirled polynomial check failed')
if negative<1e-4:
    raise SystemExit('negative control did not expose nonpolynomial dependence')

result={
    'scope':'finite matrix and outcome-adaptive macroblock illustrations; not a proof certificate',
    'seed':20261102,
    'environment':{'python':platform.python_version(),'numpy':np.__version__},
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'records':records,
    'untwirled_negative_control_degree2_residual':float(negative),
    'finite_checks_pass':True,
}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--write',type=Path)
parser.add_argument('--check',type=Path)
args=parser.parse_args()
if args.check:
    expected=json.loads(args.check.read_text())
    if expected['seed']!=result['seed'] or expected['script_sha256']!=result['script_sha256']:
        raise SystemExit('reference seed or script identity differs')
    if len(expected['records'])!=len(records):
        raise SystemExit('reference case inventory differs')
    for saved,actual in zip(expected['records'],records):
        for key in actual:
            if key=='max_residual':
                if saved[key]>=1e-10:
                    raise SystemExit('reference contains a failed residual')
            elif saved[key]!=actual[key]:
                raise SystemExit('reference case parameters differ')
    if expected['untwirled_negative_control_degree2_residual']<1e-4:
        raise SystemExit('reference negative control failed')
encoded=json.dumps(result,indent=2,sort_keys=True)+'\n'
if args.write:
    args.write.write_text(encoded)
print(encoded,end='')
