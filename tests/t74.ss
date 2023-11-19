impl A(){
    func getValue(){
        return 11
    }
}

struct B(){
    let a = alloc A
}

impl B(){
    func getValueA(){
        return self.a
    }
}

let b = alloc B
return b.getValueA().getValue()