-- Configuration
clockspeed 10000
set r10 107        -- Number of bars
set r11 1920       -- Screen width
set r12 1080       -- Screen height
div r13 r11 r10

list_new r1 ""
set r2 0
:init_loop
    jge :main_loop r2 r10
    mul r3 r2 10
    add r3 r3 10
    list_push r1 r3
    add r2 r2 1
    jmp :init_loop

:main_loop
set r2 0
:shuffle_loop
    jge :init_sort r2 1000
    sub r3 r10 1
    rngint r4 0 r3    
    rngint r5 0 r3    
    list_get r6 r1 r4 
    list_get r7 r1 r5 
    list_set r1 r4 r7 
    list_set r1 r5 r6
    add r2 r2 1
    jmp :shuffle_loop

:init_sort
set r2 0              
:i_loop
    jge :main_loop r2 r10
    sub r3 r10 r2
    sub r3 r3 1       
    set r4 0          
    :j_loop
        jge :i_next r4 r3
        
        -- Get adjacent elements
        list_get r5 r1 r4    -- Bar A
        add r6 r4 1
        list_get r7 r1 r6    -- Bar B
        
        -- Compare
        jle :j_next r5 r7
        
        -- Swap logic
        list_set r1 r4 r7
        list_set r1 r6 r5

        sound "triangle" r7 0.08 0.01 0.01 0.6 0.01

        draw_bg 5 5 10
        set r20 0     
        :draw_loop
            jge :draw_done r20 r10
            list_get r21 r1 r20   
            mul r22 r20 r13       
            sub r23 r12 r21       

            jeq :draw_other r20 r6
            draw_rect r22 r23 r13 r21 255 255 255
            jmp :draw_inc
            
            :draw_other
            draw_rect r22 r23 r13 r21 50 255 50
            
            :draw_inc
            add r20 r20 1
            jmp :draw_loop
        :draw_done
        update
        
        :j_next
        add r4 r4 1
        jmp :j_loop
    :i_next
    add r2 r2 1
    jmp :i_loop