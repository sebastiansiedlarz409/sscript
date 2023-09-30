struct Figure(){
    let field = 0
}

struct Rectangle(Figure){
    let a = 2
    let b = 3
}

impl Rectangle(Figure){
    func calcField(count){
        self.field = self.a*self.b*count
    }
}

let rect = alloc Rectangle

rect.calcField(2)
return rect.field