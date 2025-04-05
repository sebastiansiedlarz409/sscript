## SScript - programming language written for fun

### Things that I think work :P:
* variables (let) and constant (const)
* basic arithmetic operations (+-/*%) and some binary operations (|&^<<>>)
* logic operations (eq, neq, gr, ge, ls, le)
* operators like ++ --
* support for () and proper order of operations
* functions and returning
* loops: for, while, do..while
* loops flow instructions: break, continue
* conditionals: if, else if, else
* arrays declaration, array element read and override
* object oriented programming (struct and implementation syntax)

### Basic types

```
//source.ss
let a = "A"
let b = "B"
let c = "E"
let d = true
let e = 99
return c + b + a + d + e

//output
(empty)
EBAtrue99 //as exit code

```

### Loops

```
//source.ss
let i = 0

do{
    i = i + 2
}
while(i ls 9)

while(i gr 0){
    i = i - 1
}

for(let j = 0;j le 4;j++){
    logln(j)
}

//output
0
1
2
3
```

### Conditional instructions

```
//source.ss
let a = 2
let c = null

if (a eq 2){
    c = 20
}
elif (a eq 3){
    c = 30
}
elif (a eq 4){
    c = 40
}
else{
    c = 50
}
logln(c)

//output
20
```

### Functions

```
//source.ss
func pow(a, b){
    let i = 0
    let c = a
    while(i ls (b-1)){
        c = c * a
        i = i + 1
    }
    return c
}

logln(pow(2, 9))

//output
512
```

### Arrays

```
//source.ss
let a = []
let b = [1,2,3, "ASD"]
a = [1]

let c = b[1*2]
logln(c)

//output
3
```

### Object Oriented Programming

```
//source.ss
struct Figure(){ //base class
    let field = 0
}

struct Rectangle(Figure){ //child class
    let a = 2
    let b = 3
}

impl Rectangle(Figure){ //child class implementation
    func calcField(count){
        self.field = self.a*self.b*count //use 'self' to call struct member
    }
}

let rect = alloc Rectangle //alloc object

logln("Calculate field...")
rect.calcField(2) //object method call
logln(rect.field)

//output
Calculate field...
12
```
