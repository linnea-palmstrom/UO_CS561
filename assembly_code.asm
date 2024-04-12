# A simple unit test for the new Int methods
# Expected output 17 0 -17 5
.class Calc:Obj
.method $constructor
    # Calculate 5 * 3 + 2

    const "Expect 17: "
    call String:print
    pop
    const 5
    const 3
    call Int:mul
    const 2
    call Int:plus
    call Int:print
    pop
    pop
    pop

    # Calculate 3 - 2 - 1

    const "\nExpect 0: "
    call String:print
    pop
    const 3
    const 2
    call Int:sub
    const 1
    call Int:sub
    call Int:print
    pop
    pop
    pop

    # Calculate 3 - 5 * 4

    const "\nExpect -17: "
    call String:print
    pop
    const 3
    const 5
    const 4
    call Int:mul
    call Int:sub
    call Int:print
    pop
    pop
    pop

    # Calculate 15 / 3

    const "\nExpect 5: "
    call String:print
    pop
    const 15
    const 3
    call Int:div
    call Int:print
    pop
    pop

    const "\n"
    call String:print
    pop
    const nothing
    return 0
