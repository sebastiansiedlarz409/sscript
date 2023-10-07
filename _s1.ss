struct A(){
    let fieldA = 10
}

struct B(){
    let a = alloc A
}

let b = alloc B

b.a.fieldA = 11

return b.a.fieldA