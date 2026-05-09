import traceback

from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

User = get_user_model()

#region Caja

def Caja(request):
    if request.user.is_authenticated:
        try:
            if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero":
                return redirect("/")
            
            contexto = {"User": request.user}
            
            return render(request, "caja.html", contexto)
        except Exception as ex:
            print("\n\n############### E X C E P C I Ó N ###############")
            print(traceback.format_exc())
            print("#####################################################\n\n")
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

#endregion Caja

#region InicioArqueo

def InicioArqueo(request):
    if request.user.is_authenticated:
        try:
            if request.user.IdCargo.Nombre == "Armador" or request.user.IdCargo.Nombre == "Mesero":
                return redirect("/")
            
            contexto = {"User": request.user}
            
            return render(request, "caja.html", contexto)
        except Exception as ex:
            print("\n\n############### E X C E P C I Ó N ###############")
            print(traceback.format_exc())
            print("#####################################################\n\n")
    else:
        # Si no lo ha hecho entonces deberá iniciar sesión
        return render(request, "login.html")

#endregion InicioArqueo