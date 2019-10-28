Ry q0 90
RotateXY q1 90+gamma1 90
RotateXY q2 90+gamma1 -90
RotateXY q3 90+gamma1 -90
CPhase q0,q2 180
CPhase q1,q3 180
Rx q0 gamma1
RotateXY q1 90+gamma1 -90
Ry q2 90
CPhase q0,q1 180
CPhase q2,q3 180
Rx q1 -gamma2
Rx q3 -gamma2
CPhase q0,q1 180
CPhase q2,q3 180
Ry q1 90
Ry q2 -90
CPhase q0,q2 180
CPhase q1,q3 180
Rx q0 alpha1
Rx q1 alpha1
Rx q2 -alpha2
Rx q3 -alpha2
CPhase q0,q2 180
CPhase q1,q3 180
Ry q2 90
Ry q3 90