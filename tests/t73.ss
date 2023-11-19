impl A(){
    func getValue(){
        return 11
    }
}

struct B(){
    let a = alloc A
}

impl B(){
    func getValue(){
        return self.a
    }
}

let b = alloc B
let a = b.getValue()
return a.getValue()