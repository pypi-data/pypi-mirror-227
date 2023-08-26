def rahul():
    a=int(input('intered your first no\n'))
    operators=input('intered your mission +,-,*,/\n')
    b=int(input('intered your second no\n'))
    if operators == '+':
        print('good',a+b)
    elif operators == '-':
        print('good',a-b)
    elif operators == '*':
        print('good',a*b)
    elif operators == '/':
        print('good',a/b)
    elif operators == '//':
        print('good',a//b)
    elif operators == '**':
        print('good',a**b)
    elif operators == '%':
        print('good',a%b)
        print('Good Job')
    else:
        print('sorry bro you entered wrong no')
    
rahul()
