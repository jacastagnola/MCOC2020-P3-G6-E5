from matplotlib.pylab import *

# Defino mi geometria
a = 1.
b = 1.
Nx = 30 
Ny = 30  

dx = b / Nx
dy = a / Ny


if dx != dy:
    print("ERRROR!!!!! dx != dy")
    exit(-1)
    
h = dx
    
#funcion de conveniencia para calcular las cordenadas del punto(i,j)
def coords(i,j): return(dx * i, dy * j)

x,y = coords(4, 2)

print("x: ", x)
print("y: ", y)

def imshowbien(u):
    imshow(u.T[Nx::-1, :], cmap=cm.coolwarm, interpolation = "bilinear")
    cbar = colorbar(extend="both", cmap=cm.coolwarm)
    ticks = arange(0, 35, 5)
    ticks_Text = ["{}".format(deg) for deg in ticks]
    cbar.set_ticks(ticks)
    cbar.set_ticklabels(ticks_Text)
    clim(0, 30)
    
    xlabel("b")
    ylabel("a")
    xTicks_N = arange(0, Nx + 1, 3)
    yTicks_N = arange(0, Ny + 1, 3)
    xTicks = [coords(i, 0)[0] for i in xTicks_N]
    yTicks = [coords(0, i)[1] for i in yTicks_N]
    xTicks_Text = ["{0:.2f}".format(tick) for tick in xTicks]
    yTicks_Text = ["{0:.2f}".format(tick) for tick in yTicks]
    xticks(xTicks_N, xTicks_Text, rotation="vertical")
    yticks(yTicks_N, yTicks_Text)
    margins(0.2)
    subplots_adjust(bottom = 0.15)
    

u_k = zeros((Nx + 1, Ny + 1), dtype = double)
u_km1 = zeros((Nx + 1, Ny + 1), dtype = double)

#condicion de borde inicial
u_k[:,:] = 20.

#parametros del problema (iguales a los usados en ayudantia)
dt = 0.01      # segundos
K = 79.5       # m^2/s
c = 450.       # J/Kg*C
p = 7800.      # Kg/m^3
α = K * dt / (c * p * dx ** 2)

# informar cosas interesantes
print(f"dt = {dt}")
print(f"dx = {dx}")
print(f"K = {K}")
print(f"c = {c}")
print(f"rho = {p}")
print(f"alpha = {α}")

# Loop en el tiempo
minuto = 60.
hora = 3600.
dia = 24 * 3600.

dt = 1 * minuto
dnext_t = 0.5 * hora

next_t = 0
framenum = 0

T = 1 * dia
Days = T * 1 # cuantos dias quiero simular

u_0 = zeros(int32(Days / dt))
u_N4 = zeros(int32(Days / dt))
u_2N4 = zeros(int32(Days / dt))
u_3N4 = zeros(int32(Days / dt))

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

# Loop en el tiempo
for k in range(int32(Days / dt)):
    t= dt * (k + 1)
    dias = truncate(t/dia,0)
    horas = truncate((t - dias * dia) / hora, 0)
    minutos = truncate((t - dias * dia - horas * horas) / minuto, 0)
    titulo = "k = {0:05.0f}".format(
        k) + " t = {0:02.0f}d {1:02.0f}h {2:02.0f}m ".format(dias, horas, minutos)
    print(titulo)
    
    # condiciones de borde esenciales
    u_k[0, :] = 20.    # IZQUIERDO
    u_k[:, 0] = 20.    # INFERIOR
    u_k[:, -1] = 0.    # SUPERIOR
    u_k[-1, :] =  u_k[-2,:] - 0 * dx   # DERECHO

    # Loop en el espacio
    for i in range(1,Nx):
        for j in range(1,Ny):
            
            nabla_u_k = (u_k[i - 1, j] + u_k[i + 1, j] + u_k[i, j-1] + u_k[i, j+1] - 4 * u_k[i, j]) / h ** 2
            
            u_km1[i, j] = u_k[i, j] + α * nabla_u_k
    
    #avanzar la solucion a k+1        
    u_k = u_km1
    
    # CB denuevo para asegurar el cumplimiento
    u_k[0, :] = 20.
    u_k[:, 0] = 20.
    u_k[:, -1] = 0.
    u_k[-1, :] = u_k[-2, :] - 0 * dx
    
    #encuentro temperatura en puntos interesantes
    u_0[k] = u_k[int(Nx / 2), -1]
    u_N4[k] = u_k[int(Nx / 2), int( Ny / 4)]
    u_2N4[k] = u_k[int(Nx / 2), int(2 * Ny / 4)]
    u_3N4[k] = u_k[int(Nx / 2), int(3 * Ny / 4)]
    
    
    if t > next_t:
        figure(1)
        imshowbien(u_k)
       
        savefig("Ejemplo/frame_{0:04.0f}.png".format(framenum))
        framenum += 1
        next_t += dnext_t
        
        close(1)
        
show()

# ploteo historia de temperaturas en puntos interesantes
figure(2)
plot(range(int32(Days / dt )), u_0, label="superficie")
plot(range(int32(Days / dt )), u_N4, label="N/4")
plot(range(int32(Days / dt )), u_2N4, label="2N4")
plot(range(int32(Days / dt )), u_3N4, label="3N4")
title("Evolución de temperatura en puntos")
#VERIFICAR EL NOMBRE DEL CASO PARA GUARDAR IMAGEN
savefig("Evolucion_Temperaturas_caso2.png")
legend()

show()


#codigo para el gif--------------------------------------  
import glob
from PIL import Image
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r"(\d+)", text)]

#frame
fp_in = "Ejemplo/frame_*.png"
#VERIFICAR EL NOMBRE DEL CASO PARA GUARDAR GIF
fp_out = "Ejemplo_caso2.gif"

listaImagenes = sorted(glob.glob(fp_in))
print("sorted(glob.glob(fp_in)): ", listaImagenes)
listaImagenes.sort(key=natural_keys)
print("listaImagenes: ", listaImagenes)
img, *imgs = [Image.open(f) for f in listaImagenes]
img.save(fp=fp_out, format="GIF", append_images=imgs, 
         save_all=True, duration=150, loop=0)
#--------------------------------------------------------


















