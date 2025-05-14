(defun c:custom_fillet ( / linha1 linha2)
    (setq linha1 (handent "E4B"))
    (setq linha2 (handent "E4D"))
    (command "_.fillet" linha1 linha2)
    (princ "
Comando")
    (princ)
)