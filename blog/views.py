# from django.shortcuts import render
# from django.utils import timezone
# from .models import Equipement
# from .models import Animal
# from django.shortcuts import render, get_object_or_404, redirect

# from .forms import MoveForm


# def animal_list(request):
#     animals = Animal.objects.filter()
#     equipements = Equipement.objects.filter()
#     return render(request, 'animalerie/animal_list.html', {'animals': animals, 'equipements': equipements})

# def equipement_list(request):
#     equipements = Equipement.objects.filter()
#     return render(request, 'animalerie/animal_list.html', {'equipements': equipements})
    
# def animal_detail(request, id_animal):
#     animal = get_object_or_404(Animal, id_animal=id_animal)
#     form=MoveForm()
#     if request.method == "POST":
#         form = MoveForm(request.POST, instance=animal)
#     else:
#         form = MoveForm()
#     if form.is_valid():
#         lugar_antiguo = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
#         lugar_antiguo.disponibilite = "libre"
#         lugar_antiguo.save()
#         form.save()
#         nuevo_lugar = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
#         nuevo_lugar.disponibilite = "occupé"
#         nuevo_lugar.save()
#         return redirect('animal_detail', id_animal=id_animal)
#     else:
#         form = MoveForm()
#         form.save(commit=False) 
#         return render(request,
#                   'animalerie/animal_detail.html',
#                   {'animal': animal, 'lieu': animal.lieu, 'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement
 
# Create your views here.
def animal_list(request):
    animals = Animal.objects.filter()
    equipements = Equipement.objects.filter()
    return render(request, 'animalerie/animal_list.html', {'animals': animals, 'equipements': equipements})
                  
def equipement_list(request):
    equipements = Equipement.objects.filter()
    return render(request, 'animalerie/animal_list.html', {'equipements': equipements})
  
def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    lieu = animal.lieu
    form=MoveForm()
    if request.method == "POST":
        lugar_antiguo = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        form = MoveForm(request.POST, instance=animal)
        if form.is_valid():
            form.save(commit=False)
            nuevo_lugar = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
            if nuevo_lugar.disponibilite=='libre' and nuevo_lugar.id_equip=='mangeoire' and animal.etat == 'affamé':
                animal.etat='repus'
                nuevo_lugar.disponibilite='occupé'
                lugar_antiguo.disponibilite='libre'
                animal.save()
                lugar_antiguo.save()
                nuevo_lugar.save()
                return redirect('animal_detail', id_animal=id_animal)
            elif nuevo_lugar.disponibilite=='libre' and nuevo_lugar.id_equip=='roue' and animal.etat == 'repus':
                animal.etat='fatigue'
                nuevo_lugar.disponibilite='occupé'
                lugar_antiguo.disponibilite='libre'
                animal.save()
                lugar_antiguo.save()
                nuevo_lugar.save()
                return redirect('animal_detail', id_animal=id_animal)
            elif nuevo_lugar.disponibilite=='libre' and nuevo_lugar.id_equip=='nid' and animal.etat == 'fatigue':
                animal.etat='endormi'
                nuevo_lugar.disponibilite='occupé'
                lugar_antiguo.disponibilite='libre'
                animal.save()
                lugar_antiguo.save()
                nuevo_lugar.save()
                return redirect('animal_detail', id_animal=id_animal)
            elif nuevo_lugar.disponibilite=='libre' and nuevo_lugar.id_equip=='litière' and animal.etat == 'endormi':
                animal.etat='affamé'
                lugar_antiguo.disponibilite='libre'
                animal.save()                
                lugar_antiguo.save()
                return redirect('animal_detail', id_animal=id_animal)
            else:
                message="L'animal ne peut pas être déplacé"
                return render(request, 'blog/animal_detail.html', {'animal': animal, 'lieu': lieu, 'form': form, 'message': message})
    else:
        message='Ok !'
        form = MoveForm()
        return render(request,
                  'blog/animal_detail.html',
                  {'animal': animal, 'lieu': lieu, 'form': form, 'message': message})