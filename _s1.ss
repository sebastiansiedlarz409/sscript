struct B(){

}

struct A(){
    const a = 10
    let b = 11
    let c = [1,2]
    let d = alloc B
}

let obj = alloc A
logln(obj.d)