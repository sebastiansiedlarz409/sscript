struct Figure(){
    let field = 0
}

impl Figure(){
    func getField(){
        return self.field
    }
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
        return "Field is equal to: " + self.getField()
    }
}

let rect = alloc Rectangle
rect.calcField(1)

return rect.toString()