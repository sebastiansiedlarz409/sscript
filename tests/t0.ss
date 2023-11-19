let d = returnA().field + 4
let e = self.a.c.b
let e = self.a.c.b.getA().array[0]
let f = c.b.a.getArray()
self.a.c.b.getA().array[0] = 10

func test(){
    let d = returnA().field + 4
    let e = self.a.c.b
    let e = self.a.c.b.getA().array[0]
    let f = c.b.a.getArray()
    self.a.c.b.getA().array[0] = 10
}

impl A(){
    func test(){
        let d = returnA().field + 4
        let e = self.a.c.b
        let e = self.a.c.b.getA().array[0]
        let f = c.b.a.getArray()
        self.a.c.b.getA().array[0] = 10
    }
}