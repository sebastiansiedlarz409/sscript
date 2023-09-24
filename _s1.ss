struct Figura(){
    let field = 0
}

struct Kolo(Figura){
    let promien = -1
}

let a = alloc Kolo
logln(a)