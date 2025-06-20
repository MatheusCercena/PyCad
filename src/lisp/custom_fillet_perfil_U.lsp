(defun c:custom_fillet ( / linha1 linha2)
    (setq linha1 (handent "10D5"))
    (setq linha2 (handent "10D5"))
    (command "_.fillet" linha1 linha2)
    (princ "
Comando")
    (princ)
)