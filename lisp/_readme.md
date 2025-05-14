Pasta destinada arquivos lisp temporários.

Como usar comandos lisp:

Exemplo de código lisp:

1    (defun c:custom_fillet ( / ent1 ent2)
2        (setq ent1 (handent "{handle1}"))
3        (setq ent2 (handent "{handle2}")) ;comentarios sao marcados com ponto e vírgula
4        (command "_.fillet" ent1 ent2)
5        (princ)
     )

0 - lisp é baseado em listas, por isso cada linha precisa de parenteses

1 - defun: deifne a função 
    c:custom_fillet: nome da funçao
    ( / ent1 ent2): antes da / são argumentos e depois são as variáveis locais usadas na função

2 - setq : sintaxe para definir variáveis
    ent1/ent : nome da variável
    (handent "{handle1}") : nome do handle que será usado na variável

4 - command : executa uma funçao
    "_.fillet" : _ força o uso do comando em ingles, . força o uso do comando original do autocad(ignora alterações do usuário), fillet é o comando desejado
    ent1 ent2 : são os objetos que seriam escolhidos pelo usuário mas são automatizados aqui, (pode ser coordenadas tambem)

5 - princ : encerra o comando no autocad sem exibir retorno nil/nulo na command line

