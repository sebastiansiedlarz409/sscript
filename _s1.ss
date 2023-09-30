struct Rectangle(){
    let field = 0
    let a = 2
    let b = 3
}

impl Rectangle(){
    func calcField(count){
        logln("Licze pole")
        self.field = self.a*self.b*count
    }
}

let rect = alloc Rectangle
rect.calcField(2)
logln(rect.field)