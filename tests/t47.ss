struct Figure(){
    let field = 2
}

struct Rectangle(Figure){
    let a = 0
    let b = 0
}

let obj = alloc Rectangle
return obj.field + 1