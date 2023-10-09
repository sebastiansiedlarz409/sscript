struct A(){
    let numbers = [1,2,3]
}

struct B(){
    let a = alloc A
}

struct C(){
    let b = alloc B
}

impl C(){
    func getElement(index){
        return self.b.a.numbers[index]
    }
}

let c = alloc C
return c.getElement(1)