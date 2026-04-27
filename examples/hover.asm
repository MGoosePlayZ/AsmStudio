clockspeed 50
:main
get_mouse r1 r2
jgt :onepass r1 780
jmp :fail
:onepass
jlt :twopass r1 1140
jmp :fail
:twopass
jgt :threepass r2 360
jmp :fail
:threepass
jlt :fourpass r2 720
jmp :fail
:fourpass
set r3 1
jmp :finally
:fail
set r3 0
jmp :finally

:finally
draw_bg 30 30 30
draw_rect 780 360 360 360 255 255 255

add r8 r8 0.05

add r9 r8 2
add r10 r8 4

sin r4 r8
sin r5 r9
sin r6 r10

add r4 r4 1
mul r4 r4 127

add r5 r5 1
mul r5 r5 127

add r6 r6 1
mul r6 r6 127

jeq :hovered r3 1
draw_text "You have not hovered over the square" 610 110 40 255 255 255
jmp :upd
:hovered
draw_text "You have hovered over the square" 640 110 40 r4 r5 r6
:upd
update
jmp :main