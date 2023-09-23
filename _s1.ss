struct Figura(){
    public let field = 0
}

let a = alloc(Figura, 1)
a.field = 10
let b = 2 + a.field

func p(){
    a.field = 10
    let gg = a.field
}