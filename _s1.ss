for(let i = 0;i ls 10;i=i+1){
    if(i eq 2){
        break
    }
    logln(i)
}

logln("---")

let j = 0
while(j ls 10){
    if(j eq 2){
        break
    }
    logln(j)
    j = j + 1
}

logln("---")

j = 0
do{
    if(j eq 2){
        break
    }
    logln(j)
    j = j + 1
}while(j ls 10)

logln("---")

for(let i = 0;i ls 10;i=i+1){
    if(i eq 2){
        continue
    }
    logln(i)
}

logln("---")

j = 0
while(j ls 10){
    if(j eq 2){
        j = j + 1
        continue
    }
    logln(j)
    j = j + 1
}

logln("---")

j = 0
do{
    if(j eq 2){
        j = j + 1
        continue
    }
    logln(j)
    j = j + 1
}while(j ls 10)