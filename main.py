import numpy as np

import warnings
warnings.filterwarnings("ignore")


def _replace_nan(a, val):
    a = np.array(a, subok=True, copy=True)
    if a.dtype == np.object_:
        mask = a != a
    elif issubclass(a.dtype.type, np.inexact):
        mask = np.isnan(a)
    else:
        mask = None
    if mask is not None:
        np.copyto(a, val, where=mask)
    return a, mask

def concatena_registro(tab, registro):
  tab[0, :] = registro
  return tab

def forma_canonica(tab, base): #dada uma base que sabemos ser viavel, transfomar tab na fpi
  for idx, bs in enumerate(base):
    tab, _ = pivoteamento(tab, idx+1, bs, tab[0,:].copy()) #colocar registro aleatorio, fodasse ele

  return tab

def get_viabilidade(c, a, b, n, m):


  #add variaveis de folga
  c = np.pad(c, (0, n+1), 'constant')
  id = np.eye(n)
  a = np.concatenate((a, id), axis=1)
  registro = c*(-1) #registrar linha c original

  neg = np.where(b < 0)[0]
  for i in neg:
    a[:][i] = a[:][i]*(-1)
    b[i] = b[i]*(-1)

  tab = np.zeros((n + 1, m + n + n+ 1))

  c = np.zeros(m + n + n +1)
  c[m+n:-1] = np.ones(n)
  id = np.eye(n)
  a = np.concatenate((a, id), axis=1)
  registro = np.pad(registro, (0, n))

  #concatenar tudo formando o tableau
  a = np.column_stack((a,b))
  tab[0] = c
  tab[1:, :] = a


  #formar matriz id para achar certificados
  cert = np.zeros((n + 1, n))
  cert[1:, :] = np.eye(n)

  for i in neg:
    cert[:][i+1] = cert[:][i+1]*(-1)

  tab = np.column_stack((cert, tab))
  registro = np.pad(registro, (n, 0), 'constant')


  #deixar na forma canonica
  for i in range (1, n+1):
    tab[0,:] = tab[i, :]*(-1) + tab[0, :]
    registro[:] = tab[i, :]*(-1) + registro[:]

  base = [i for i in range(2*n, 2*n + n)]

  tab, base, registro = simplex(tab, base, n, m, registro)

  return tab, base, registro


def find_colunm(tab, n):
 
  aux = tab[0, n:-1]
  primeiro = np.where(aux < 0)[0]

  return n + primeiro[0]


def find_line(tab, n):
  col = find_colunm(tab, n)

  aux2 = [tab[i,col] if tab[i,col]>=0 else 0 for i in range(1,n+1)]
  aux = tab[1:,-1]/aux2

  aux = np.array(aux)
  aux, mask = _replace_nan(aux, np.inf)

  line = np.where(aux >= 0, aux, np.inf).argmin()

  return line + 1


def atualiza_base(base, row, col): #subtrair 1 para atualizar indice da linha pulando o c 
  base[row-1] = col
  return base


def pivoteamento(tab, row, col, registro):
  element = float(tab[row, col])


  if element < 0 and not np.isclose(element, 0):
  	tab[row, :] = tab[row, :]*(-1)

  tab[row,:] = tab[row,:]/element #transformar elemento em 1

  for i in range (len(tab)):
    if i == row:
      continue
    else:
      aux = tab[i, col]
      tab[i, :] = tab[row, :]*(-1)*(aux) + tab[i, :]

      if i == 0:
        registro[:] = tab[row, :]*(-1)*(aux) + registro[:]
  
  return tab, registro


def simplex(tab, base, n, m, registro):

  for i in range (len(tab[0,:])):
    if np.isclose(tab[0,i], 0):
      tab[0,i] = 0

  if all(i >= 0 for i in tab[0,n:-2]):
    return tab, base, registro
  
  else:
    col = find_colunm(tab, n)
    aux = tab[:, col]
    if all(i <= 0 for i in aux):
        print("ilimitada")
        tab = np.around(tab, decimals=7)

        base = [i - n for i in base]

        ultima_coluna = tab[:,-1]

        cert1 = np.zeros(m+ m + n)

        for idx, bs in enumerate(base):
          cert1[bs] = ultima_coluna[idx+1]
        cert1 = cert1[0:m]

        coluna_negativa = tab[:, col]
        cert2 = np.zeros(m+ m + n)
        cert2[col-n] = 1

        for idx, bs in enumerate(base):
          cert2[bs] = coluna_negativa[idx+1]*(-1)
        cert2 = cert2[0:m]


        for i in cert1:
            print(f"{round(i, 7):.7f}", end=' ')
        print()

        for i in cert2:
            print(f"{round(i, 7):.7f}", end=' ')
        print()


        exit()
        return tab, base, registro
    row = find_line(tab, n)
    tab, registro = pivoteamento(tab, row, col, registro)
    base = atualiza_base(base, row, col)
    return simplex(tab, base, n, m, registro)


def sol_otima(tab, base, n, m):
  base = [i - n for i in base]
  aux = tab[1:, -1]
  sol = np.zeros(len(tab[0]-n)) #numero de colunas - aux de certificados
  for idx, i in enumerate(base):
    sol[i] = aux[idx]

  cert = tab[0, 0:n]
  otimo = tab[0, -1]
  return sol[0:m], cert, otimo

n, m = input().split()
c = input().split()
ab = []
for i in range(int(n)):
  ab.append(input().split())

n = int(n)
m = int(m)
ab = np.array(ab)
ab = np.float32(ab)
c = np.array(c)
c = np.float32(c)
a = ab[:, 0:m]
b = ab[:, -1]


tab, base, registro = get_viabilidade(c, a, b, n, m)
#tab = np.around(tab, decimals=7)

if (round(tab[0, -1], 1) == 0):
  tab = concatena_registro(tab, registro)
  tab = forma_canonica(tab, base)
  tab, base, registro = simplex(tab, base, n, m, registro.copy())
  #tab = np.around(tab, decimals=7)
  sol, cert, otm = sol_otima(tab, base, n, m)
  print('otima')
  print(otm)
  for i in sol:
    print(f"{round(i, 7):.7f}", end=' ')
  print()
  for i in cert:
    print(f"{round(i, 7):.7f}", end=' ')
  print()

else:
  #tab = np.around(tab, decimals=7)
  print("inviavel")
  inv = tab[0, 0:n]
  for i in inv:
    print(f"{round(i, 7):.7f}", end=' ')
  print()
