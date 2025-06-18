(defun c:custom_fillet ( / linha1 linha2)
    (setq linha1 (handent "EAE"))
    (setq linha2 (handent "EB0"))
    (command "_.fillet" linha1 linha2)
    (princ "
Comando")
    (princ)
)