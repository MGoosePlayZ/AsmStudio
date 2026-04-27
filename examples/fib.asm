clockspeed 8
set r1 1      -- prev
set r2 1      -- curr
set r3 100    -- limit

draw_bg 10 10 20
draw_text r1 50 50 40 255 255 255
update

:loop
draw_bg 10 10 20
draw_text r2 50 50 40 255 255 255
update
sleep 0.1
add r3 r1 r2  -- next = prev + curr
set r1 r2     -- prev = curr
set r2 r3     -- curr = next
jmp :loop