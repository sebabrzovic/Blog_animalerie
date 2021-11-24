from django.shortcuts import render, get_object_or_404, redirect
from .models import Animal, Equipement
from .forms import MoveForm

# Create your views here.

def animal_list(request):
    animals = Animal.objects.filter()
    return render(request, 'animalerie/animal_list.html', {'animals': animals})
 
def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    form=MoveForm()
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)
    else:
        form = MoveForm()
    if form.is_valid():
        ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        ancien_lieu.disponibilite = "libre"
        ancien_lieu.save()
        form.save()
        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        nouveau_lieu.disponibilite = "occupé"
        nouveau_lieu.save()
        return redirect('animal_detail', id_animal=id_animal)
    else:
        form = MoveForm()
        form.save(commit=False) 
        return render(request,
                  'animalerie/animal_detail.html',
                  {'animal': animal, 'lieu': animal.lieu, 'form': form})