struct Rectangle(){
    let field = 0
    let a = 2
    let b = 3
}

impl Rectangle(){
    func calcField(){
        self.field = self.a + self.b
    }
}