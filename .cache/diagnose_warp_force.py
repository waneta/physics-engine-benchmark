import json
import numpy as np
from physics_benchmark.extended.model import build
from physics_benchmark.extended.rigid import Warp, Controller
s=build({'family':'grasp','dt':.001})
sim=Warp(s); controller=Controller(s)
b=s.model.body('cube').id; j=s.model.body_jntadr[b]; dof=s.model.jnt_dofadr[j]; mass=s.model.body_mass[b]
q,v,p,quat=sim.state(); w=np.zeros((s.model.nbody,6)); maxerr=0
for i in range(2000):
 u=controller.command(i,q,v,w,p)
 prev=v.copy(); w=sim.step(u); q,v,p,quat=sim.state()
 residual=mass*(v[dof:dof+3]-prev[dof:dof+3])-(w[b,:3]+mass*s.model.opt.gravity)*.001
 err=np.linalg.norm(residual)
 if err>max(maxerr*1.5,5e-6):
  cf=sim.d.qfrc_constraint.numpy()[0,dof:dof+3]
  print(json.dumps({'step':i,'residual':residual.tolist(),'force':w[b,:3].tolist(),'generalized_contact_force':cf.tolist(),'qacc':sim.d.qacc.numpy()[0,dof:dof+3].tolist(),'mass':mass,'body_ipos':s.model.body_ipos[b].tolist()}),flush=True)
  maxerr=err
print('max',maxerr)
