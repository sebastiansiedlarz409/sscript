impl A(){
    func getValue(){
        return 1
    }
}

struct B(){
    let a = alloc A
}

let b = alloc B
return b.a.getValue()