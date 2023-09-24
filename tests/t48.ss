struct Figure(){
    let field = 0
}

struct Circle(Figure){
    let r = -1
}

let a = alloc Circle
a.field = 10
return a.field