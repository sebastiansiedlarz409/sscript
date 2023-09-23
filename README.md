<h2 align="left">SScript - programming language written for fun</h2>

<h3>Supported stuff:</h3>
* variables (let) and constant (const)
* basic arithmetic operations (+-/*%) and some binary operations (|&^<<>>)
* logic operations (eq, neq, gr, ge, ls, le)
* operators like ++ --
* functions and returning
* loops: for, while, do..while
* loops flow instructions: break, continue
* conditionals: if, else if, else
* arrays declaration, array element read and override

<h1></h1>
<h4>Basic types</h4>

```
let a = "A"
let b = "B"
let c = "E"
let d = true
let e = 99

return c + b + a + d + e
```

<h1></h1>
<h4>Loops</h4>

```
let i = 0

do{
    i = i + 2
}
while(i ls 9)

while(i gr 0){
    i = i - 1
}

for(let j = 0;j le 10;j++){
    logln(j)
}
```

<h1></h1>
<h4>Conditional instructions</h4>

```
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
```

<h1></h1>
<h4>Functions</h4>

```
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
```

<h1></h1>
<h4>Arrays</h4>


```
let a = []
let b = [1,2,3, "ASD"]
a = [1]

let c = b[1*10]
logln(c)
```