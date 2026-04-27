clockspeed 1000

print "BREAKOUT - Left/Right arrows"

set r1 960    -- ball x
set r2 750    -- ball y
set r3 9      -- ball dx
set r4 -13    -- ball dy
set r5 860    -- paddle left edge
set r6 0      -- score
set r7 3      -- lives
set r8 37     -- entropy seed
set r10 200   -- paddle width
set r11 12    -- ball radius
set r19 50    -- bricks remaining
set r20 100   -- half paddle width

arr_ones r12 5 10

:main_loop
add r8 r8 17
draw_bg 10 10 20

-- Input
set r9 0
get_press r9 K_LEFT
jz :chk_right r9
sub r5 r5 18
max r5 r5 0
:chk_right
set r9 0
get_press r9 K_RIGHT
jz :do_physics r9
add r5 r5 18
min r5 r5 1720

:do_physics
add r1 r1 r3
add r2 r2 r4

-- Walls
jgt :chk_rwall r1 11
abs r3 r3
:chk_rwall
jlt :chk_twall r1 1909
abs r3 r3
mul r3 r3 -1
:chk_twall
jgt :chk_paddle r2 11
abs r4 r4

:chk_paddle
jlt :chk_bottom r2 988
jgt :chk_bottom r2 1030
jlt :chk_bottom r1 r5
add r9 r5 r10
jgt :chk_bottom r1 r9
abs r4 r4
mul r4 r4 -1
sound 'square' 300 0.05 0 0 1 0
sub r9 r1 r5
sub r9 r9 r20
div r9 r9 12
set r3 r9
jnz :chk_bottom r3
set r3 5

:chk_bottom
jlt :chk_brick r2 1092
sub r7 r7 1
jgt :do_respawn r7 0
draw_bg 10 10 20
draw_text "GAME OVER" 630 460 90 255 60 60
draw_text r6 870 590 60 255 255 255
update
:gameover
jmp :gameover

:do_respawn
sound 'square' 220 0.12 0 0 1 0
sleep 0.4
set r1 960
set r2 750
set r3 9
set r4 -13
mod r9 r8 5
sub r9 r9 2
add r3 r3 r9

:chk_brick
jlt :do_render r2 100
jge :do_render r2 375
jlt :do_render r1 60
jge :do_render r1 1860
sub r13 r1 60
sub r14 r2 100
div r13 r13 180
div r14 r14 55
flr r13 r13
flr r14 r14
jlt :do_render r13 0
jge :do_render r13 10
jlt :do_render r14 0
jge :do_render r14 5
arr_get r16 r12 r14 r13   -- row=r14, col=r13
jz :do_render r16
arr_set r12 r14 r13 0
sub r19 r19 1
add r6 r6 10
sound 'square' 660 0.04 0 0 1 0
mul r4 r4 -1
jgt :do_render r19 0
draw_bg 10 10 20
draw_text "YOU WIN!" 680 460 90 60 255 120
draw_text r6 870 590 60 255 255 255
update
:win_loop
jmp :win_loop

:do_render
set r14 0
:brow_loop
jge :brow_end r14 5
set r13 0
:bcol_loop
jge :bcol_end r13 10
arr_get r16 r12 r14 r13
jz :next_brick r16
mul r17 r13 180
add r17 r17 60
mul r18 r14 55
add r18 r18 100
jeq :bcolor0 r14 0
jeq :bcolor1 r14 1
jeq :bcolor2 r14 2
jeq :bcolor3 r14 3
draw_rect r17 r18 170 45 60 130 255
jmp :next_brick
:bcolor0
draw_rect r17 r18 170 45 255 55 55
jmp :next_brick
:bcolor1
draw_rect r17 r18 170 45 255 150 30
jmp :next_brick
:bcolor2
draw_rect r17 r18 170 45 220 200 30
jmp :next_brick
:bcolor3
draw_rect r17 r18 170 45 55 200 60
:next_brick
add r13 r13 1
jmp :bcol_loop
:bcol_end
add r14 r14 1
jmp :brow_loop
:brow_end

draw_rect r5 1000 r10 20 180 180 210
draw_circ r1 r2 r11 255 220 50
draw_text r6 50 30 45 255 255 255
draw_text r7 1830 30 45 255 120 120
update
jmp :main_loop