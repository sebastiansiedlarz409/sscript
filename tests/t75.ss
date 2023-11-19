impl A(){
    func getValue(){
        return 11
    }
}

struct B(){
    let a = alloc A
}

struc C(){
    let b = alloc B
}

impl C(){
    func getValueB(){
        return self.b
    }
}

let c = alloc C
return c.getValueB().a.getValue()