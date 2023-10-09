struct A(){
    let numbers = [1,2,3]
}

struct B(){
    let a = alloc A
}

let b = alloc B
return b.a.numbers[2]