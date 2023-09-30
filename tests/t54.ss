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
        return self.field
    }

    func toString(){
        return "Field is equal to: " + self.calcField(3)
    }
}

let rect = alloc Rectangle

return rect.toString()