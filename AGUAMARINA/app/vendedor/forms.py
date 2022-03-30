from django.forms import *
from vendedor.models import Vendedor

class AdminForm(ModelForm):
    class Meta:
        model = Vendedor
        fields = "__all__"
        widgets = {
            'name' : TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : 'Ingrese un nombre',
                    'autocomplete' : 'off'
                }
            ),    
            'desc' : Textarea(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : 'Ingrese una descripcion',
                    'autocomplete' : 'off',
                    'rows' : 3,
                    'cols' : 3
                }
            )
        }
    def save(self, commit=True):
        data = {}
        form = super()
        try:
                if form.is_valid():
                    form.save()
                else:
                    data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data