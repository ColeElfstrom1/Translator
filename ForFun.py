def fibonacci(index):
    memory = [1, 1]
    bit = 0

    while index > 2:
        bit = 1 - bit
        memory[bit] = memory[0] + memory[1]
        index -= 1
    
    return memory[bit]
