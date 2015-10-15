#! /usr/bin/env python
import numpy as n, pylab as p
import sys

m_e = 1e-27
c = 3e10
e = 5e-10
pc = 3e18 # cm

def gen_pulse_profile(fqs, ts, DM):
    pp = n.zeros((ts.size, fqs.size), dtype=n.float)
    ws = 2*n.pi*fqs
    dt = ts[1] - ts[0]
    for j,w in enumerate(ws):
        t = 2*n.pi*e**2/(m_e*c*w**2) * DM * pc
        i = int(n.around(t/dt))
        print i, j
        try: pp[i,j] += 1
        except(IndexError): pass
    return pp

def dedisperse(pp, fqs, ts, DM):
    dat,wgt = 0., 0.
    ws = 2*n.pi*fqs
    dt = ts[1] - ts[0]
    for j,w in enumerate(ws):
        t = 2*n.pi*e**2/(m_e*c*w**2) * DM * pc
        i = int(n.around(t/dt))
        try:
            dat += pp[i,j]
            wgt += 1
        except(IndexError): pass
    return dat/wgt

fqs = n.linspace(1.,2.,100) * 1e9
ts  = n.linspace(0.,1.,100)
   
DM = 137.
pp = gen_pulse_profile(fqs, ts, DM)
pp += n.random.normal(size=pp.shape, scale=0.88)**2
p.subplot(121)
p.imshow(pp, interpolation='nearest', aspect='auto')

dms = n.arange(500)
dat = []
for dm in dms:
    dat.append(dedisperse(pp, fqs, ts, dm))
p.subplot(122)
p.plot(dms, dat)

p.show()
#t = n.zeros(2*fqs.size, dtype=n.float)
#t[0] = 1.
#t += n.random.normal(size=t.size)*0.1

f = open('pulsar.dat','w')
f.write('#[Time s] ')
for fq in fqs: f.write('[%5.3f GHz] ' % (fq/1e9))
f.write('\n')
for i,t in enumerate(ts):
    f.write('%5.3f ' % (t))
    for d in pp[i]: f.write('%5.3f ' % (d))
    f.write('\n')
f.close()

