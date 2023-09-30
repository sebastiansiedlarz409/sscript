struct Rectangle(){
    let field = 0
    let a = 2
    let b = 3
}

impl Rectangle(){
    func calcField(){
        self.field = 1
        logln("Licze pole")
    }
}

let rect = alloc Rectangle
rect.calcField()
logln(rect.field)