clockspeed 5000

print "SNAKE - Direct Start"

arr_zeros r1 18 32   -- grid: 18 rows x 32 cols
set r2 16    -- head col
set r3 9     -- head row
set r4 1     -- dx (starting right)
set r5 0     -- dy
set r6 4     -- length
set r7 0     -- score
set r8 0     -- frame counter
set r9 37    -- entropy seed
set r10 25   -- food col
set r11 5    -- food row

-- Pre-place initial snake body
arr_set r1 9 13 1
arr_set r1 9 14 2
arr_set r1 9 15 3
arr_set r1 9 16 4

:main_loop
draw_bg 15 15 25
add r15 r8 r6 -- Head expiry value

set r14 0
:grow_loop
jge :grow_end r14 18
set r13 0
:gcol_loop
jge :gcol_end r13 32

-- Food?
jne :chk_snake r13 r10
jne :chk_snake r14 r11
mul r21 r13 60
mul r22 r14 60
draw_rect r21 r22 58 58 210 45 45
jmp :gcol_next

:chk_snake
arr_get r20 r1 r14 r13
jle :gcol_next r20 r8
mul r21 r13 60
mul r22 r14 60
jeq :draw_head r20 r15
draw_rect r21 r22 58 58 40 160 65
jmp :gcol_next
:draw_head
draw_rect r21 r22 58 58 120 255 130

:gcol_next
add r13 r13 1
jmp :gcol_loop
:gcol_end
add r14 r14 1
jmp :grow_loop
:grow_end

draw_text r7 20 20 45 255 255 255
update
sleep 0.08

set r12 0
get_press r12 K_LEFT
jz :chk_up r12
jeq :chk_up r4 1
set r4 -1
set r5 0
jmp :do_move

:chk_up
set r12 0
get_press r12 K_UP
jz :chk_right r12
jeq :chk_right r5 1
set r4 0
set r5 -1
jmp :do_move

:chk_right
set r12 0
get_press r12 K_RIGHT
jz :chk_down r12
jeq :chk_down r4 -1
set r4 1
set r5 0
jmp :do_move

:chk_down
set r12 0
get_press r12 K_DOWN
jz :do_move r12
jeq :do_move r5 -1
set r4 0
set r5 1

:do_move
add r2 r2 r4
add r3 r3 r5
add r8 r8 1
add r9 r9 17

-- Wall collision
jlt :game_over r2 0
jge :game_over r2 32
jlt :game_over r3 0
jge :game_over r3 18

-- Self collision
arr_get r12 r1 r3 r2
jgt :game_over r12 r8

-- Food check
jne :no_food r2 r10
jne :no_food r3 r11
add r6 r6 1
add r7 r7 10
sound 'square' 660 0.04 0 0 1 0
add r9 r9 131
mod r10 r9 30
add r10 r10 1
add r9 r9 97
mod r11 r9 16
add r11 r11 1

:no_food
add r12 r8 r6
arr_set r1 r3 r2 r12
jmp :main_loop

:game_over
sound 'square' 220 0.2 0 0 1 0
sleep 0.1
sound 'square' 180 0.3 0 0 1 0
draw_bg 15 15 25
draw_text "GAME OVER" 560 430 90 255 60 60
draw_text r7 830 550 60 255 255 255
update
:go_loop
jmp :go_loop