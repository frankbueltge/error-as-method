# arrow pointing right
r = 2 ** 0.5
lo, hi, a = -r/2, r/2, -4*r
PIECES = {
 "L1": [(0,-2*r),(2*r,0),(0,0)], "L2": [(0,0),(2*r,0),(0,2*r)],
 "Q": [(-r,lo),(0,lo),(0,hi),(-r,hi)],
 "S1": [(a,lo),(a+r,hi),(a,hi)], "M": [(a,lo),(a+2*r,lo),(a+r,hi)],
 "P": [(a+r,hi),(a+2*r,lo),(a+3*r,lo),(a+2*r,hi)], "S2": [(a+2*r,hi),(a+3*r,lo),(a+3*r,hi)],
}
