(defun c:custom_fillet ( / linha1 linha2)
    (setq linha1 (handent "1227"))
    (setq linha2 (handent "1229"))
    (command "_.fillet" linha1 linha2)
    (princ "
Comando")
    (princ)
)