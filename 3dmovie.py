#Usage: after creating the frames, do
#mogirfy -format png *.pbm
#convert -delay 30 *.png movie.gif

import math
import sys
import random

#"data" consists of tuples (x, y, z, r, g, b), where |z|<1, |y|<1, |z|<1, x^2+y^2<1.
#r<8, g<8, b<8
def gen_frames(data, n, dn):
    for i in range(300):
        c=math.cos(i*2*math.pi/300)
        s=math.sin(i*2*math.pi/300)
        frame=[[[7, 7, 7] for j in range(n)] for k in range(n)]
        depth=[[0.0 for j in range(n)] for k in range(n)]
        for pt in data:
            x=pt[0]
            y=pt[1]
            z=pt[2]
            if abs(x)<1 and abs(y)<1 and abs(z)<1 and x*x+y*y<1:
                nx=c*x+s*y
                ny=-s*x+c*y
                nz=z
                nnx=nx*(2-ny)/3
                nnz=nz*(2-ny)/3
                if depth[-(int)(nnz*n*0.5+n/2)][(int)(nnx*n*0.5+n/2)]<2-ny:
                    depth[-(int)(nnz*n*0.5+n/2)][(int)(nnx*n*0.5+n/2)]=2-ny
                    frame[-(int)(nnz*n*0.5+n/2)][(int)(nnx*n*0.5+n/2)]=[pt[3], pt[4], pt[5]]
        output=open(dn+"{0:03d}".format(i)+".ppm", "w")
        print("P3\n"+str(n)+" "+str(n)+"\n7\n", file=output)
        for row in frame:
            print(' '.join([' '.join([str(e1) for e1 in e]) for e in row]), file=output)
        output.close()
    return 0

#Drawing primitives using Frenet coordinate

class Loc:
    def __init__(self, pos, coord):
        self.pos=pos
        self.coord=coord
    def r(self, angle):
        c=math.cos(angle)
        s=math.sin(angle)
        ncoord0=[c*x+s*y for x, y in zip(self.coord[0], self.coord[1])]
        ncoord1=[-s*x+c*y for x, y in zip(self.coord[0], self.coord[1])]
        self.coord[0]=ncoord0
        self.coord[1]=ncoord1
    def r2(self, angle):
        c=math.cos(angle)
        s=math.sin(angle)
        ncoord1=[c*x+s*y for x, y in zip(self.coord[1], self.coord[2])]
        ncoord2=[-s*x+c*y for x, y in zip(self.coord[1], self.coord[2])]
        self.coord[1]=ncoord1
        self.coord[2]=ncoord2
    def fwd(self, sz, nstep, color):
        r=[]
        for i in range(nstep):
            r+=[[p+x*sz/nstep*i for p, x in zip(self.pos, self.coord[0])]+[color[0], color[1], color[2]]]
        npos=[p+x*sz for p, x in zip(self.pos, self.coord[0])]
        self.pos=npos
        return r
    def dup(self):
        npos=[x for x in self.pos]
        ncoord=[[x for x in y] for y in self.coord]
        return Loc(npos, ncoord)
    def ball(self, radius, color, n):
        r=[]
        for i in range(n):
            x=random.gauss(0, 0.5)
            y=random.gauss(0, 0.5)
            z=random.gauss(0, 0.5)
            rad=(x**2+y**2+z**2)**0.5
            if rad>0:
                x=x/rad*radius
                y=y/rad*radius
                z=z/rad*radius
                r+=[[self.pos[0]+x, self.pos[1]+y, self.pos[2]+z, color[0], color[1], color[2]]]
        return r


#Tree via L-system
data=[]

def x(p, n):
    if n==0 or p.pos[0]**2+p.pos[1]**2>(0.92-p.pos[2])**2/5:
        return p
    else:
        p=f(p, n-1)
        for i in range(4):
            p1=p.dup()
            p1.r2(i*2*math.pi/4)
            p1.r(1)
            p1.r2(random.random()*2*math.pi)
            x(p1, n-1)
        p=f(p, n-1)
        p.r2(random.random()*2*math.pi)
        if p.coord[0][2]<0.9:
            p.r(random.random()*0.5)    
        p=x(p, n-1)
        return p

def f(p, n):
    global data
    if  p.pos[0]**2+p.pos[1]**2>(0.92-p.pos[2])**2/5:
        data+=p.ball(0.03, [5, 0, 0], 200)
        return p
    if n<=0:
        data+=p.fwd(0.03, 8, [0, 3, 0])
        return p
    else:
        p=f(p, n-2)
        p.r2(random.random()*2*math.pi)
        if p.coord[0][2]<0.9:
            p.r(random.random()*0.3)    
        return f(p, n-1)

c=Loc([0, 0, -1], [[0, 0, 1], [0, 1, 0], [1, 0, 0]])
p=x(c, 6)
print(p.pos)
data+=p.ball(0.04, [7, 5, 0], 400)
gen_frames(data, 500, sys.argv[1])


##
##data=[]
###Get point set via IFS:
##pt=[0, 0, 0]
##for i in range(200000):
##    r=random.random()
##    x=pt[0]
##    y=pt[1]
##    z=pt[2]
##    c=math.cos(2)
##    s=math.sin(2)
##    if r>0.13:
##        nz=1+(z-1)*0.975
##        nx=0.975*(c*x+s*y)
##        ny=0.975*(-s*x+c*y)
##        pt=[nx, ny, nz]
##    elif r<0.03:
##        nz=-1+(z+1)*0.025
##        nx=0.02*x
##        ny=0.02*y
##        pt=[nx, ny, nz]
##    else:
##        ang=(int)(r*100)%8*math.sqrt(2)
##        c2=math.cos(ang)
##        s2=math.sin(ang)
##        c1=math.cos(0.45*math.pi)
##        s1=math.sin(0.45*math.pi)
##        tx=c*x+s*y
##        ty=-s*x+c*y
##        nx=0.4*(c1*tx+s1*(z+1))
##        ny=0.4*ty
##        nz=0.4*(-s1*tx+c1*(z+1))-0.95
##        nnx=c2*nx+s2*ny
##        nny=-s2*nx+c2*ny
##        pt=[nnx, nny, nz]
##    if i>1000:
##        data+=[pt]
##
##gen_frames(data, 300, "./output/")
