impl A(){
    func getValue(){
        return 1
    }
}

struct B(){
    let a = alloc A
}

impl B(){
    func getValue(){
        return self.a.getValue()
    }
}

let b = alloc B
return b.getValue()