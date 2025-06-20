(defun c:custom_fillet ( / linha1 linha2)
    (setq linha1 (handent "1189"))
    (setq linha2 (handent "118B"))
    (command "_.fillet" linha1 linha2)
    (princ "
Comando")
    (princ)
)