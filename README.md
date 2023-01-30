### Compiler final project, related to spring 2023
We've put a lot of effort on this project and we're happy it is working correctly :) thanks to @arad_fir

This compiler get input language and generate the intermediate code in C programming language. We used PLY to create this compiler. Backpatch method is used to  fulfill unspecified labels.

#### Example:
Input is Fibonacci code that is accepted by the grammar language
```
program a var a, b, c, n : int begin
    a := 1;
    b := 1;
    n := 0;
    while n < 10 do begin
        c := b;
        b := a + b;
        a := c;
        n := n + 1;
        print(n);
        print(a)
    end
end
```
As we expected the output is code in C programming language
```
#include <stdio.h>
int a, b, c, n;

float T_1, T_2, T_3, T_4, T_5, T_6, T_7, T_8, T_9, T_10, T_11, T_12, T_13, T_14, T_15;
int main() {
 L_1:   T_1 = 1;
 L_2:   a = T_1;
 L_3:   T_2 = 1;
 L_4:   b = T_2;
 L_5:   T_3 = 0;
 L_6:   n = T_3;
 L_7:   T_4 = n;
 L_8:   T_5 = 10;
 L_9:   if (T_4 < T_5) goto L_11;
 L_10:  goto L_28;
 L_11:  T_6 = b;
 L_12:  c = T_6;
 L_13:  T_7 = a;
 L_14:  T_8 = b;
 L_15:  T_9 = T_7 + T_8;
 L_16:  b = T_9;
 L_17:  T_10 = c;
 L_18:  a = T_10;
 L_19:  T_11 = n;
 L_20:  T_12 = 1;
 L_21:  T_13 = T_11 + T_12;
 L_22:  n = T_13;
 L_23:  T_14 = n;
 L_24:  printf("%f\n", (float)T_14);
 L_25:  T_15 = a;
 L_26:  printf("%f\n", (float)T_15);
 L_27:  goto L_7;
 L_28:  return 0;
}
```
