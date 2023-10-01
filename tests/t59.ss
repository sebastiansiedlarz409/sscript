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

struct Box(Rectangle){
    let height = 4
}

impl Box(Rectangle){
    func calcCapacity(){
        self.calcField(1)
        return self.height * self.getField()
    }
}

let b = alloc Box
b.calcCapacity()
return b.field