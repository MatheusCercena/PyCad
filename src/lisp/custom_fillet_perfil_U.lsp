(defun c:custom_fillet ( h1 h2 / linha1 linha2)
    (setq linha1 (handent h1))
    (setq linha2 (handent h2))
    (command "_.fillet" linha1 linha2)
    (princ "
Comando")
    (princ)
)