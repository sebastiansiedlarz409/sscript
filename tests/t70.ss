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
    func setElement(index, value){
        self.b.a.numbers[index] = value
    }
}

let c = alloc C
c.setElement(1,4)
return c.getElement(1)