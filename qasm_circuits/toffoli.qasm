OPENQASM 3.0;
include "stdgates.inc";

gate toffoli a, b, c {ccx a, b, c;}
qubit[3] q;
bit[3] c;

toffoli q[2], q[1], q[0];
p(pi / 2) q[0];
ch q[0], q[1];
c = measure q;
