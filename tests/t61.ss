impl Base(){
    func toString(){
        return "Im base"
    }
}

impl Child(){
    func toString(){
        return "Im child"
    }
}

let obj = alloc Child
return obj.toString()