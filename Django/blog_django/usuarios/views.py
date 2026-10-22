from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegistroForm, PerfilForm
from .models import Perfil


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # El perfil se crea justo después de guardar el usuario
            Perfil.objects.create(user=usuario)
            login(request, usuario)
            return redirect('perfil')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def perfil(request):
    # get_or_create: cubre usuarios viejos (ej. el superusuario) que no tienen perfil
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    return render(request, 'usuarios/perfil.html', {'perfil': perfil})


@login_required
def editar_perfil(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # request.FILES lleva el avatar subido
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'usuarios/editar_perfil.html', {'form': form, 'perfil': perfil})
