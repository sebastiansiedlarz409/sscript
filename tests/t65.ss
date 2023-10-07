struct B(){
    let a = [1,2,3]
}

let b = alloc B
b.a[0] = 2
return b.a[0]