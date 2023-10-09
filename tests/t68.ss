struct A(){
    let numbers = [1,2,3]
}

struct B(){
    let a = alloc A
}

struct C(){
    let b = alloc B
}

let c = alloc C
c.b.a.numbers[0] = 99
return c.b.a.numbers[0]