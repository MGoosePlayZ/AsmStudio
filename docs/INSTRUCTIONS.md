# Default Instructions

|              Instruction               | Description                                   |
|:--------------------------------------:|:----------------------------------------------|
|               `set A B`                | A = B                                         |
|              `add A B C`               | A = B + C                                     |
|              `sub A B C`               | A = B - C                                     |
|              `mul A B C`               | A = B * C                                     |
|              `div A B C`               | A = B / C                                     |
|              `mod A B C`               | A = B % C (Remainder)                         |
|              `pow A B C`               | A = B ** C (Power)                            |
|               `abs A B`                | A = abs(B)                                    |
|              `root A B C`              | A = C ** (1 / B)                              |
|              `log A B C`               | A = log(B) with base C                        |
|                `ln A B`                | A = natural log of B                          |
|               `exp A B`                | A = e ** B                                    |
|               `fact A B`               | A = B! (Factorial)                            |
|               `flr A B`                | A = floor(B)                                  |
|               `ceil A B`               | A = ceil(B)                                   |
|               `rnd A B`                | A = round(B)                                  |
|               `trnc A B`               | A = truncate(B)                               |
|              `min A B C`               | A = min(B, C)                                 |
|              `max A B C`               | A = max(B, C)                                 |
|             `rngflt A L H`             | A = random.uniform(L, H)                      |
|             `rngint A L H`             | A = random.randint(L, H)                      |
|                                        |                                               |
|              `and A B C`               | A = B & C                                     |
|               `or A B C`               | A = B \| C                                    |
|              `xor A B C`               | A = B ^ C                                     |
|              `nand A B C`              | Bitwise NOT-AND                               |
|              `nor A B C`               | Bitwise NOT-OR                                |
|              `xnor A B C`              | Bitwise NOT-XOR                               |
|              `shl A B C`               | A = B << C (Shift Left)                       |
|              `shr A B C`               | A = B >> C (Shift Right)                      |
|              `rol A B C`               | Rotate bits of B left by C                    |
|              `ror A B C`               | Rotate bits of B right by C                   |
|             `bitset A B C`             | Set bit at index C in B to 1                  |
|             `bitclr A B C`             | Set bit at index C in B to 0                  |
|             `bittog A B C`             | Toggle bit at index C in B                    |
|             `bitget A B C`             | Get value of bit at index C in B              |
|              `bitson A B`              | A = count of set bits in B                    |
|              `bitlen A B`              | A = number of bits required for B             |
|                                        |                                               |
|               `sin A B`                | A = sin(B)                                    |
|               `cos A B`                | A = cos(B)                                    |
|               `tan A B`                | A = tan(B)                                    |
|               `csc A B`                | A = 1 / sin(B)                                |
|               `sec A B`                | A = 1 / cos(B)                                |
|               `cot A B`                | A = 1 / tan(B)                                |
|                                        |                                               |
|               `cast A B`               | Convert B between string and number           |
|               `len A B`                | A = length of string B                        |
|            `strsub A B C D`            | A = B\[C:D] (Substring)                       |
|            `strfind A B C`             | A = index of C in B                           |
|           `strsplit A B C D`           | Split C at index D into A and B               |
|           `strjoin A B C D`            | A = B + D + C                                 |
|              `strrev A B`              | A = reversed B                                |
|             `strupper A B`             | A = B in uppercase                            |
|             `strlower A B`             | A = B in lowercase                            |
|             `strtrim A B`              | A = B with whitespace removed                 |
|              `typeof A B`              | A = type name of B                            |
|              `isint A B`               | A = 1 if B is int, else 0                     |
|             `isfloat A B`              | A = 1 if B is float, else 0                   |
|              `isstr A B`               | A = 1 if B is string, else 0                  |
|              `islist A B`              | A = 1 if B is list, else 0                    |
|              `isarr A B`               | A = 1 if B is array, else 0                   |
|              `isnone A B`              | A = 1 if B is None, else 0                    |
|                                        |                                               |
|                `jmp A`                 | Jump to A                                     |
|              `jeq A B C`               | Jump to A if B == C                           |
|              `jne A B C`               | Jump to A if B != C                           |
|              `jgt A B C`               | Jump to A if B > C                            |
|              `jlt A B C`               | Jump to A if B < C                            |
|              `jge A B C`               | Jump to A if B >= C                           |
|              `jle A B C`               | Jump to A if B <= C                           |
|                `jz A B`                | Jump to A if B == 0                           |
|               `jnz A B`                | Jump to A if B != 0                           |
|               `sleep A`                | Sleeps for A seconds                          |
|                 `halt`                 | Stop execution                                |
|                  `--`                  | Comment                                       |
|                                        |                                               |
|               `print A`                | Print A with newline                          |
|              `println A`               | Print A without newline                       |
|              `input A B`               | Get input A with prompt B                     |
|                `clear`                 | Clear terminal screen                         |
|            `draw_bg R G B`             | Fill screen with RGB color                    |
|       `draw_rect X Y W H R G B`        | Draw colored rectangle                        |
|        `draw_img path X Y W H`         | Draw image                                    |
|             `draw_array A`             | Draw array                                    |
|       `draw_circ X Y Rad R G B`        | Draw colored circle                           |
|    `draw_line X1 Y1 X2 Y2 T R G B`     | Draw line with thickness T                    |
|       `draw_text T X Y S R G B`        | Draw text T at (X,Y) with size S              |
|   `draw_tri X1 Y1 X2 Y2 X3 Y3 R G B`   | Draw triangle from 3 points                   |
|                `update`                | Refresh display                               |
|            `get_mouse X Y`             | Store mouse coordinates in X and Y            |
|            `get_press A K`             | Set A to 1 if key K is pressed                |
|           `get_click L M R`            | Store mouse clicks                            |
|             `get_scroll A`             | Store scrollwheel velocity                    |
|                                        |                                               |
| `sound Type Freq Dur Atk Dec Sus Rel ` | Plays a Sound (sine, square, triangle, noise) |
|                                        |                                               |
|             `clockspeed A`             | Sets the steps per tick to A                  |
|                                        |                                               |
|             `list_new L V`             | A = \[L]                                      |
|            `list_get A L I`            | A = L\[I]                                     |
|            `list_set L I V`            | L\[I] = C                                     |
|            `list_push L V`             | L.append(V)                                   |
|              `list_pop L`              | L.pop()                                       |
|             `list_len A L`             | A = L.len()                                   |
|          `list_slice A L S E`          | A = L\[S:E]                                   |
|          `list_insert L I E`           | L.insert(I, E)                                |
|           `list_remove L I`            | L.remove(I)                                   |
|             `list_clear L`             | L.clear()                                     |
|           `list_extend L V`            | L.extend(V)                                   |
|            `list_range A L`            | A = range(L)                                  |
|                                        |                                               |
|           `arr_zeros A W H`            | A = np.zeros((W, H)),                         |
|            `arr_ones A W H`            | A = np.ones((W, H)),                          |
|            `arr_shape A B`             | A = np.shape(B),                              |
|           `arr_get A B W H`            | A = B\[W,H],                                  |
|           `arr_set A W H B`            | A\[W, H] = B,                                 |
|             `arr_fill A V`             | A.fill(V),                                    |
|             `arr_sum A B`              | A = np.sum({1}),                              |
|            `arr_mean A B C`            | A = np.mean(B, C),                            |
|             `arr_flat A B`             | A = B.flatten(),                              |
|          `arr_rshape A B W H`          | A = B.reshape(W, H),                          |
|            `arr_rand A W H`            | A = np.random.rand(W, H),                     |
|                `arr_lt`                | A = B < C                                     |
|                `arr_gt`                | A = B > C                                     |
|              `arr_where`               | A = np.where(B, C, D)                         |
|             `arr_linspace`             | A = np.linspace(B, C, D)                      |
|             `arr_meshgrid`             | A, B = np.meshgrid(C, D)                      |
|              `arr_stack3`              | A = np.dstack((B, C, D))                      |
|            `arr_transpose`             | A = np.transpose(B, (1,0,2))                  |
|                                        |                                               |
|               `copy A B`               | A = B.copy()                                  |