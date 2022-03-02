OPENQASM 3;
include "stdgates.inc";
gate majority a, b, c {
    cx c, b;
    cx c, a;
    h c;
    tdg a;
    t b;
    t c;
    cx a, b;
    cx c, a;
    cx b, c;
    tdg a;
    cx b, a;
    tdg a;
    tdg b;
    t c;
    cx c, a;
    s a;
    cx b, c;
    cx a, b;
    h c;
}
gate unmaj a, b, c {
    h c;
    tdg a;
    t b;
    t c;
    cx a, b;
    cx c, a;
    cx b, c;
    tdg a;
    cx b, a;
    tdg a;
    tdg b;
    t c;
    cx c, a;
    s a;
    cx b, c;
    cx a, b;
    h c;
    cx c, a;
    cx a, b;
}
qubit[1] cin;
qubit[4] a;
qubit[4] b;
qubit[1] cout;
bit[5] ans;
uint[4] a_in = 1;  
uint[4] b_in = 15; 
reset cin;
reset a;
reset b;
reset cout;
for i in [0: 3] {
  if(bool(a_in[i])) x a[i];
  if(bool(b_in[i])) x b[i];
}
majority cin[0], b[0], a[0];
for i in [0: 2] { majority a[i], b[i + 1], a[i + 1]; }
cx a[3], cout[0];
for i in [2: -1: 0] { unmaj a[i],b[i+1],a[i+1]; }
unmaj cin[0], b[0], a[0];
measure b[0:3] -> ans[0:3];
measure cout[0] -> ans[4];