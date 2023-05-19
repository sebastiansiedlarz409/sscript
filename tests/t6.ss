func pow(a, b){
    let i = 0
    let c = a
    b = b - 1
    while(i ls b){
        c = c * a
        i = i + 1
    }
    return c
}

return pow(2, 9)