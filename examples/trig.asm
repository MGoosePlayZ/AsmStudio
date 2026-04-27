clockspeed 200
:loop
add r1 r1 2
div r2 r1 100
sin r3 r2
mul r3 r3 100
add r3 r3 540
cos r4 r2
mul r4 r4 100
add r4 r4 540
tan r5 r2
mul r5 r5 100
add r5 r5 540
cot r6 r2
mul r6 r6 100
add r6 r6 540
sec r7 r2
mul r7 r7 100
add r7 r7 540
csc r8 r2
mul r8 r8 100
add r8 r8 540
draw_circ r1 r3 5 255 0 0
draw_circ r1 r4 5 255 255 0
draw_circ r1 r5 5 0 255 0
draw_circ r1 r6 5 0 255 255
draw_circ r1 r7 5 0 0 255
draw_circ r1 r8 5 255 0 255
update
jne :loop r1 1920
:fin
jmp :fin