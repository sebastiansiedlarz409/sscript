struct A(){
    let fieldA = 10
}

struct B(){
    let a = alloc A
}

let b = alloc B
return b.a.fieldA