from math import *

def genstl(data, fn):
    out=open(fn, "w")
    print("solid s", file=out)
    for trip in data:
        print("facet normal 0.0 0.0 0.0\nouter loop", file=out)
        for i in range(3):
            print("vertex "+" ".join(["{:.6e}".format(float(trip[i][j])) for j in range(3)]), file=out)
        print("endloop\nendfacet", file=out)
    print("endsolid", file=out)
    out.close()
    return 0

data=[]
for i in range(40):
    v0=[100, 100, 0]
    v1=[cos(i*2*pi/40)*100+100, sin(i*2*pi/40)*100+100, 0]
    v2=[cos((i+1)*2*pi/40)*100+100, sin((i+1)*2*pi/40)*100+100, 0]
    v3=[100, 100, 100]
    data+=[[v1, v2, v0], [v3, v2, v1]]

genstl(data, "cone.stl")
