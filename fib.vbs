Function fibonacci(n COMO integer) COMO integer
    ' codigo do raphael costa
    DEFINIR flag COMO boolean
    
    flag = false
    SE n = 0 FAZER
        fibonacci = 1
        flag = true
    FIM SE

    SE n = 1 FAZER 
        fibonacci = 1
        flag = true
    FIM SE

    SE flag = false FAZER
        fibonacci = fibonacci(n-2) + fibonacci(n-1)
    FIM SE

FIM Function

Sub principal()
    DEFINIR num COMO integer
    num = ENTRADA
    print fibonacci(num)
FIM Sub