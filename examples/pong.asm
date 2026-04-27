clockspeed 108
-- Initialization
print "Welcome to Pong!"
print "Player 1: w key/s key to move"
print "Player 2: up arrow/down arrow to move"
set r1 960 -- Ball X
set r2 540 -- Ball Y
set r3 12 -- Ball DX
set r4 0 -- Ball DY
set r5 465 -- P1 Y
set r6 465 -- P2 Y
set r7 0 -- P1 Score
set r8 0 -- P2 Score
set r10 150 -- Paddle Height
set r11 20 -- Paddle Width
set r12 75 -- Half Paddle Height
set r13 930 -- Clamp Limit
set r14 6 -- Bounce intensity divisor
set r15 37 -- Entropy Seed
:main_loop
add r15 r15 17 -- Line 16: Update entropy every frame
draw_bg 20 20 20
-- Player 1 Input
set r9 0
get_press r9 K_w
jz :p1_down r9
sub r5 r5 15
max r5 r5 0
:p1_down
set r9 0
get_press r9 K_s
jz :p2_input r9
add r5 r5 15
min r5 r5 r13
:p2_input
-- Player 2 Input
set r9 0
get_press r9 K_UP
jz :p2_down r9
sub r6 r6 15
max r6 r6 0
:p2_down
set r9 0
get_press r9 K_DOWN
jz :physics r9
add r6 r6 15
min r6 r6 r13
:physics
add r1 r1 r3
add r2 r2 r4
-- Wall Bounce
jgt :bounce_bot r2 0
set r4 10
sound 'square' 440 0.05 0 0 1 0
:bounce_bot
jlt :p1_col r2 1065
set r4 -10
sound 'square' 440 0.05 0 0 1 0
:p1_col
-- Paddle 1 Collision
jne :p2_col r1 60
jlt :p2_col r2 r5
add r9 r5 r10
jgt :p2_col r2 r9
set r3 12
sound 'square' 440 0.05 0 0 1 0
sub r9 r2 r5
sub r9 r9 r12
div r4 r9 r14
:p2_col
-- Paddle 2 Collision
jne :score_check r1 1860
jlt :score_check r2 r6
add r9 r6 r10
jgt :score_check r2 r9
set r3 -12
sound 'square' 440 0.05 0 0 1 0
sub r9 r2 r6
sub r9 r9 r12
div r4 r9 r14
:score_check
jgt :p1_score r1 0
add r8 r8 1
sound 'square' 440 0.05 0 0 1 0
sleep 0.05
sound 'square' 660 0.05 0 0 1 0
set r1 960 -- Respawn Ball X
set r2 540 -- Respawn Ball Y
set r3 12 -- Reset DX
mod r4 r15 21 -- Randomize DY (0 to 20)
sub r4 r4 10 -- Offset DY (-10 to 10)
:p1_score
jlt :render r1 1920
add r7 r7 1
sound 'square' 440 0.05 0 0 1 0
sleep 0.05
sound 'square' 660 0.05 0 0 1 0
set r1 960 -- Respawn Ball X
set r2 540 -- Respawn Ball Y
set r3 -12 -- Reset DX
mod r4 r15 21 -- Randomize DY (0 to 20)
sub r4 r4 10 -- Offset DY (-10 to 10)
:render
draw_rect 40 r5 r11 r10 255 255 255
draw_rect 1860 r6 r11 r10 255 255 255
draw_circ r1 r2 15 0 255 0
draw_text r7 800 50 60 255 255 255
draw_text r8 1080 50 60 255 255 255
update
jz :main_loop r0