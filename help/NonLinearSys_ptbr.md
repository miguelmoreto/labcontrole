## Sistema Não-linear

Ajuda para o sistema com processo não-linear

### Definindo um sistema de primeira ordem

Na string que descreve a equação diferencial do sistema não-linear, devem ser observadas se seguintes definições:

* A variável de saída deve ser inserida como `Y` (letra ípsilon maiúsculo)
* A derivada da varíavel de saída em relação ao tempo deve ser inserida como `DY`
* A variável de entrada deve ser inserida como `U` (letra u maiúsculo).

As seguintes expressões são aceitas na string de definição da equação diferencial do sistema:

* `^`: representa a operação potência, por exemplo `Y^2`,`Y^3`, etc.
* `e^`: representa a operação exponencial, por exemplo `e^(Y-1)` ou `e^(Y)`
* `sqrt`: representa a operação raiz quadrada, por exemplo `sqrt(Y)`
* `sin`: representa a operação seno, por exemplo `sin(Y)`
* `cos`: representa a operação cosseno, por exemplo `cos(Y)`

Além dessas definições, podem ser empregadas funções da biblioteca math do python (https://docs.python.org/3/library/math.html) desde que tenham como argumento principal um valor scalar. Por exemplo, podem ser usada a string `math.log10(Y)` para a operação logarítmo de base 10 da variável de saída. 

O separador decimal pode ser `.` ou `,`.

### Definindo um sistema de segunda ordem

Funcionalidade ainda não implementada.