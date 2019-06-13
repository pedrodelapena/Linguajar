Function Soma(x como integer, y como integer) como integer
    Soma = x + y
FIM Function

Sub principal()
    definir a como integer
    definir c como integer
    definir b como integer
    
    c = 100
    b = 99999
    a = 0
    ENQUANTO (c > 1)
        a = a + 1
        c = c-5
        SE (a > c) FAZER
            print b
            print a
            print c
            print nao c
            c = 0
        SENAO 
            print Soma(a,c)
        FIM SE
    FINALIZADO

FIM sub