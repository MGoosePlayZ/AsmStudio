-- Constants
clockspeed 296
set r26 960        -- cx
set r27 540        -- cy
set r28 280        -- perspective scale
set r29 5          -- z offset (near plane)
set r20 0          -- angle_x
set r21 0          -- angle_y
set r30 0.018      -- angle_x delta per frame
set r31 0.027      -- angle_y delta per frame

:main_loop
add r20 r20 r30
add r21 r21 r31
draw_bg 10 10 20

-- Precompute trig
sin r22 r20        -- sin_ax
cos r23 r20        -- cos_ax
sin r24 r21        -- sin_ay
cos r25 r21        -- cos_ay

-- Transform macro: Y-rot then X-rot then perspective → rnd px, py
-- For each vertex (vx, vy, vz):
--   tx = vx*cay - vz*say  |  tz = vx*say + vz*cay
--   ry = vy*cax - tz*sax  |  rz = vy*sax + tz*cax
--   w = rz + r29  |  px = cx + scale*tx/w  |  py = cy + scale*ry/w

-- V0 (-1, -1, -1)
mul r70 -1 r25
mul r71 -1 r24
sub r72 r70 r71
mul r73 -1 r24
mul r74 -1 r25
add r75 r73 r74
mul r76 -1 r23
mul r77 r75 r22
sub r78 r76 r77
mul r79 -1 r22
mul r80 r75 r23
add r81 r79 r80
add r82 r81 r29
div r83 r72 r82
mul r84 r83 r28
add r84 r84 r26
rnd r40 r84
div r86 r78 r82
mul r87 r86 r28
add r87 r87 r27
rnd r50 r87

-- V1 (1, -1, -1)
mul r70 1 r25
mul r71 -1 r24
sub r72 r70 r71
mul r73 1 r24
mul r74 -1 r25
add r75 r73 r74
mul r76 -1 r23
mul r77 r75 r22
sub r78 r76 r77
mul r79 -1 r22
mul r80 r75 r23
add r81 r79 r80
add r82 r81 r29
div r83 r72 r82
mul r84 r83 r28
add r84 r84 r26
rnd r41 r84
div r86 r78 r82
mul r87 r86 r28
add r87 r87 r27
rnd r51 r87

-- V2 (1, 1, -1)
mul r70 1 r25
mul r71 -1 r24
sub r72 r70 r71
mul r73 1 r24
mul r74 -1 r25
add r75 r73 r74
mul r76 1 r23
mul r77 r75 r22
sub r78 r76 r77
mul r79 1 r22
mul r80 r75 r23
add r81 r79 r80
add r82 r81 r29
div r83 r72 r82
mul r84 r83 r28
add r84 r84 r26
rnd r42 r84
div r86 r78 r82
mul r87 r86 r28
add r87 r87 r27
rnd r52 r87

-- V3 (-1, 1, -1)
mul r70 -1 r25
mul r71 -1 r24
sub r72 r70 r71
mul r73 -1 r24
mul r74 -1 r25
add r75 r73 r74
mul r76 1 r23
mul r77 r75 r22
sub r78 r76 r77
mul r79 1 r22
mul r80 r75 r23
add r81 r79 r80
add r82 r81 r29
div r83 r72 r82
mul r84 r83 r28
add r84 r84 r26
rnd r43 r84
div r86 r78 r82
mul r87 r86 r28
add r87 r87 r27
rnd r53 r87

-- V4 (-1, -1, 1)
mul r70 -1 r25
mul r71 1 r24
sub r72 r70 r71
mul r73 -1 r24
mul r74 1 r25
add r75 r73 r74
mul r76 -1 r23
mul r77 r75 r22
sub r78 r76 r77
mul r79 -1 r22
mul r80 r75 r23
add r81 r79 r80
add r82 r81 r29
div r83 r72 r82
mul r84 r83 r28
add r84 r84 r26
rnd r44 r84
div r86 r78 r82
mul r87 r86 r28
add r87 r87 r27
rnd r54 r87

-- V5 (1, -1, 1)
mul r70 1 r25
mul r71 1 r24
sub r72 r70 r71
mul r73 1 r24
mul r74 1 r25
add r75 r73 r74
mul r76 -1 r23
mul r77 r75 r22
sub r78 r76 r77
mul r79 -1 r22
mul r80 r75 r23
add r81 r79 r80
add r82 r81 r29
div r83 r72 r82
mul r84 r83 r28
add r84 r84 r26
rnd r45 r84
div r86 r78 r82
mul r87 r86 r28
add r87 r87 r27
rnd r55 r87

-- V6 (1, 1, 1)
mul r70 1 r25
mul r71 1 r24
sub r72 r70 r71
mul r73 1 r24
mul r74 1 r25
add r75 r73 r74
mul r76 1 r23
mul r77 r75 r22
sub r78 r76 r77
mul r79 1 r22
mul r80 r75 r23
add r81 r79 r80
add r82 r81 r29
div r83 r72 r82
mul r84 r83 r28
add r84 r84 r26
rnd r46 r84
div r86 r78 r82
mul r87 r86 r28
add r87 r87 r27
rnd r56 r87

-- V7 (-1, 1, 1)
mul r70 -1 r25
mul r71 1 r24
sub r72 r70 r71
mul r73 -1 r24
mul r74 1 r25
add r75 r73 r74
mul r76 1 r23
mul r77 r75 r22
sub r78 r76 r77
mul r79 1 r22
mul r80 r75 r23
add r81 r79 r80
add r82 r81 r29
div r83 r72 r82
mul r84 r83 r28
add r84 r84 r26
rnd r47 r84
div r86 r78 r82
mul r87 r86 r28
add r87 r87 r27
rnd r57 r87

-- ======== DRAW FACES ========
-- Backface cull: cross_z = (p1x-p0x)*(p2y-p0y) - (p1y-p0y)*(p2x-p0x)
-- draw if cross_z > 0  (screen-space CCW = facing camera, y-down)
-- vertex ordering per face uses right-hand rule for outward normal

-- FACE 0: FRONT v4,v5,v6,v7 — RED
sub r90 r45 r44
sub r91 r56 r54
mul r92 r90 r91
sub r93 r55 r54
sub r94 r46 r44
mul r95 r93 r94
sub r96 r92 r95
jge :skip_f0 r96 0       -- was jle, flipped
draw_tri r44 r54 r45 r55 r46 r56 220 60 60
draw_tri r44 r54 r46 r56 r47 r57 220 60 60
:skip_f0

-- FACE 1: BACK v0,v3,v2,v1 — BLUE
sub r90 r43 r40
sub r91 r52 r50
mul r92 r90 r91
sub r93 r53 r50
sub r94 r42 r40
mul r95 r93 r94
sub r96 r92 r95
jge :skip_f1 r96 0
draw_tri r40 r50 r43 r53 r42 r52 60 60 220
draw_tri r40 r50 r42 r52 r41 r51 60 60 220
:skip_f1

-- FACE 2: RIGHT v1,v2,v6,v5 — GREEN
sub r90 r42 r41
sub r91 r56 r51
mul r92 r90 r91
sub r93 r52 r51
sub r94 r46 r41
mul r95 r93 r94
sub r96 r92 r95
jge :skip_f2 r96 0
draw_tri r41 r51 r42 r52 r46 r56 60 200 60
draw_tri r41 r51 r46 r56 r45 r55 60 200 60
:skip_f2

-- FACE 3: LEFT v0,v4,v7,v3 — YELLOW
sub r90 r44 r40
sub r91 r57 r50
mul r92 r90 r91
sub r93 r54 r50
sub r94 r47 r40
mul r95 r93 r94
sub r96 r92 r95
jge :skip_f3 r96 0
draw_tri r40 r50 r44 r54 r47 r57 200 200 60
draw_tri r40 r50 r47 r57 r43 r53 200 200 60
:skip_f3

-- FACE 4: TOP v0,v1,v5,v4 — MAGENTA
sub r90 r41 r40
sub r91 r55 r50
mul r92 r90 r91
sub r93 r51 r50
sub r94 r45 r40
mul r95 r93 r94
sub r96 r92 r95
jge :skip_f4 r96 0
draw_tri r40 r50 r41 r51 r45 r55 200 60 200
draw_tri r40 r50 r45 r55 r44 r54 200 60 200
:skip_f4

-- FACE 5: BOTTOM v2,v3,v7,v6 — CYAN
sub r90 r43 r42
sub r91 r57 r52
mul r92 r90 r91
sub r93 r53 r52
sub r94 r47 r42
mul r95 r93 r94
sub r96 r92 r95
jge :skip_f5 r96 0
draw_tri r42 r52 r43 r53 r47 r57 60 200 200
draw_tri r42 r52 r47 r57 r46 r56 60 200 200
:skip_f5

update
jz :main_loop r0