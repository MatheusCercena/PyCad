#criar linha: acad.model.AddLine(APoint(0, 0), APoint(100, 0))
# copiar: variavel.Copy()
# mover: variavel.Move(APoint(0, 0), APoint(0, 0))
#criar blocos: acad.doc.Blocks.Add(APoint(0, 0), "MeuBloco")
#adicionar linha no bloco: line = block.AddLine(APoint(0, 0), APoint(50, 50))

#inserir bloco: acad.model.InsertBlock(APoint(0, 0), "MeuBloco", 1, 1, 1, 0) #Insere o bloco "MeuBloco" na posição (0,0), escala 1:1, rotação 0°.

#adicionar linha e puxar cota
# line = acad.model.AddLine(APoint(0, 0), APoint(3557, 0))
# dim = acad.model.AddDimAligned(APoint(0, 0), APoint(3557, 0), APoint(50, 200))
# dim.StyleName = "LINHA DE CENTRO"

# mtext = acad.model.AddMText(APoint(10, 10), 50, "Texto Exemplo")# posição (10,10), largura 50 e altura 5
#altura do mtext = mtext.Height = 5  
#enviar comando aleatorio acad.doc.SendCommand('FILLET\nR\n10\n\n')  # Define raio 10 e entra no comando FILLET

#mover: 
# obj = acad.model.AddLine(APoint(0, 0), APoint(50, 0))
# obj.Move(APoint(0, 0), APoint(10, 10))

#copiar: 
# obj = acad.model.AddCircle(APoint(50, 50), 20)
# copy_obj = obj.Copy()
# copy_obj.Move(APoint(50, 50), APoint(100, 100))

#definir layer
# linha.Layer = "MinhaLayer"  # Definir a layer da linha
#rotacionar: obj.Rotate(base_point, angle)#angle in radianos

#Se a linha estiver inclinada, calculamos o vetor perpendicular à linha para garantir que a cota fique sempre acima.
# import math

# # Criar linha inclinada
# p1 = APoint(0, 0)
# p2 = APoint(100, 50)
# linha = acad.model.AddLine(p1, p2)

# # Calcular vetor direção da linha
# dx = p2.x - p1.x
# dy = p2.y - p1.y
# length = math.sqrt(dx**2 + dy**2)

# # Vetor unitário perpendicular (90° sentido anti-horário)
# perp_x = -dy / length
# perp_y = dx / length

# # Calcular posição da cota deslocada na direção perpendicular
# offset = 10  # Distância da cota em relação à linha
# p3 = APoint((p1.x + p2.x) / 2 + perp_x * offset, (p1.y + p2.y) / 2 + perp_y * offset)

# # Criar a cota
# dim = acad.model.AddDimAligned(p1, p2, p3)

# for obj in acad.iter_objects("AcDbLine"):
#     p1 = APoint(obj.StartPoint)  # Ponto inicial
#     p2 = APoint(obj.EndPoint)    # Ponto final