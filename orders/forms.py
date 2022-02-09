from django import forms 


class MyModelForm(ModelForm):
    class Meta:
        model = Pizza
        fields = ["toppings"]