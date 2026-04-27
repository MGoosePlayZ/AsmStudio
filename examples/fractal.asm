clockspeed 91

-- Settings
set r1 1920        -- width
set r2 1080        -- height
set r3 48         -- max iterations

-- Complex plane bounds
set r4 -2.5       -- x_min
set r5 1.0        -- x_max
set r6 -1.25      -- y_min
set r7 1.25       -- y_max

-- Create coordinate arrays
arr_linspace r11 r4 r5 r1     
arr_linspace r12 r6 r7 r2     
arr_meshgrid r13 r14 r11 r12  

-- Z = 0, C = X + iY
arr_zeros r15 r2 r1   -- Z_real
arr_zeros r16 r2 r1   -- Z_imag
copy r17 r13          -- C_real
copy r18 r14          -- C_imag

-- iteration counter array
arr_zeros r19 r2 r1   

-- mask (1 = still computing)
arr_ones r20 r2 r1

set r21 0
:iter_loop
jge :calculate_colors r21 r3

-- Z = Z^2 + C
mul r22 r15 r15       
mul r23 r16 r16       
sub r24 r22 r23       
mul r25 r15 r16
mul r25 r25 2         
add r15 r24 r17
add r16 r25 r18

-- magnitude squared check
mul r26 r15 r15
mul r27 r16 r16
add r28 r26 r27

-- update mask (1 if |Z|^2 < 4)
arr_lt r20 r28 4

-- increment iteration count for pixels that haven't escaped yet
add r19 r19 r20

add r21 r21 1
jmp :iter_loop

:calculate_colors
-- Create 'Inside' mask: pixels that are still 1 in r20 after loop
-- These should be black (0,0,0)
-- Create 'Escaped' mask (1 - Inside mask)
set r60 1
sub r61 r60 r20       -- r61 is 1 for escaped pixels, 0 for inside

-- LIGHT BLUE for long escape, DARK BLUE for short escape
-- Normalize: (iteration / max_iterations) * 255
mul r31 r19 255
div r31 r31 r3

-- Apply escaped mask so 'inside' pixels stay at 0
mul r31 r31 r61

-- RGB logic for "Blue Gradient"
-- Red: 0
-- Green: r31 / 2 (gives a lighter/sky blue tint)
-- Blue: r31
arr_zeros r41 r2 r1   -- Red (Black)
copy r42 r31
div r42 r42 2         -- Green (Half intensity for light blue)
copy r43 r31          -- Blue (Full intensity)

-- combine and draw
arr_stack3 r51 r41 r42 r43
arr_transpose r52 r51
draw_array r52
:fin
update

jeq :fin r100 1
print "DONE"
set r100 1
jmp :fin