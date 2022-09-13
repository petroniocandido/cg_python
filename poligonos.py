import cg-python.comum
from cg-python.comum import putpixel
from cg-python.retas import reta

class Poligono(object):

  # Construtor
  def __init__(self):
    self.pontos = []  # Lista de Pontos

    self.xmax = 0
    self.ymax = 0
    self.xmin = 0
    self.ymin = 0

  def add(self, x, y):
    
    self.pontos.append((x,y))

    self.xmax = np.max([self.xmax, x])
    self.ymax = np.max([self.ymax, y])
    self.xmin = np.min([self.xmin, x])
    self.ymin = np.min([self.ymin, y])
    
  def centro(self):
    mx = (self.xmax - self.xmin)/2 + self.xmin
    my = (self.ymax - self.ymin)/2 + self.ymin
    return (mx, my)
  
  def transformar(self, mat):
    p = Poligono()
    for x,y in self.pontos:
      xn, yn = mat.aplicar(x,y)
      p.add(xn, yn)
    return p

  # Bordas
  def boundary(self, tela, cor=(50,50,50,255)):

    # Desenha a reta entre o último e o primeiro ponto
    x1, y1 = self.pontos[0]
    x2, y2 = self.pontos[-1]
    
    reta(tela, x1, y1, x2, y2, cor=cor)

    # para cada par de pontos, do primeiro ao último
    for i in range(1, len(self.pontos)):
    
      x1, y1 = self.pontos[i-1]
      x2, y2 = self.pontos[i]
    
      # Desenha a reta
      reta(tela, x1, y1, x2, y2, cor=cor)

  # Preenchimento de Polígonos - Algoritmo de Varredura
  def fill_raster(self,tela, background, foreground):

    # Desenha as bordas
    self.boundary(tela, foreground)

    # Percorre o bounding box no eixo Y
    for y in range(self.ymin, self.ymax):

      pontosx = []  #Cria uma lista vazia de pontos

      # Percorre o bounding box no eixo X
      for x in range(self.xmin, self.xmax):
        
        # Se o pixel (x,y) está pintado
        # verifica se os pixels de cima tb estão pintados
        if tela.getpixel((x,y)) != background and \
          ( tela.getpixel((x,y-1)) != background or tela.getpixel((x-1,y-1)) != background \
           or tela.getpixel((x+1,y-1)) != background):

          # Se sim, adiciona na lista de pontos
          pontosx.append(x)

      # Para cada par de pontos
      for i in range(0, len(pontosx)-1, 2):
        x1 = pontosx[i]
        x2 = pontosx[i+1]

        # Traça uma reta entre os pontos
        reta(tela, x1, y, x2, y, foreground)
             
  # Preenchimento de Polígonos - Algoritmo de Varredura
  def fill_degrade(self,tela, background, cor1, cor2):

    R = 0
    G = 1
    B = 2

    amplitude = self.xmax - self.xmin

    ir = int((cor2[R] - cor1[R])/amplitude)
    ig = int((cor2[G] - cor1[G])/amplitude)
    ib = int((cor2[B] - cor1[B])/amplitude)

    cor = cor1
    linha_degrade = [cor1]
    for x in range(self.xmin, self.xmax):
      ncor = (cor[R] + ir, cor[G] + ig, cor[B] + ib, 255)
      linha_degrade.append(ncor)
      cor = ncor 

    # Desenha as bordas
    self.boundary(tela, foreground)

    # Percorre o bounding box no eixo Y
    for y in range(self.ymin, self.ymax):

      pontosx = []  #Cria uma lista vazia de pontos

      # Percorre o bounding box no eixo X
      for x in range(self.xmin, self.xmax):
        
        # Se o pixel (x,y) está pintado
        # verifica se os pixels de cima tb estão pintados
        if tela.getpixel((x,y)) != background and \
          ( tela.getpixel((x,y-1)) != background or tela.getpixel((x-1,y-1)) != background \
           or tela.getpixel((x+1,y-1)) != background):

          # Se sim, adiciona na lista de pontos
          pontosx.append(x)

      # Para cada par de pontos
      for i in range(0, len(pontosx)-1, 2):
        x1 = pontosx[i]
        x2 = pontosx[i+1]

        # Traça uma reta entre os pontos
        for x in range(x1, x2):
          putpixel(tela, x, y, linha_degrade[self.xmin - x])

  def __str__(self):
    return str(self.pontos)