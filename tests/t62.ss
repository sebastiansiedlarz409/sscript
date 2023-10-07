struct A(){
    let fieldA = 10
}

struct B(){
    let a = alloc A
}

impl B(){
    func getField(){
        return self.a.fieldA
    }
}

let b = alloc B
return b.getField()