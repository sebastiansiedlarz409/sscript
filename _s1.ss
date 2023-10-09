struct A(){
    let numbers = [1,2,3]
}

struct B(){
    let a = alloc A
}

let b = alloc B
b.a.numbers[0] = 3
return b.a.numbers[0]