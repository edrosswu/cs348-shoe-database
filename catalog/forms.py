from django import forms

class Report(forms.Form):
    shoe_name = forms.CharField(required = False, help_text = "Enter a shoe name or leave empty", max_length = 100, min_length = 0, strip = True)
    
    brand_name = forms.CharField(required = False, help_text = "Enter a brand name or leave empty", max_length = 30, min_length = 0, strip = True)
    
    lockdown_q = forms.IntegerField(help_text = "Enter a minimum number for lockdown", max_value = 10, min_value = 0)
    
    traction_q = forms.IntegerField(help_text = "Enter a minimum number for traction", max_value = 10, min_value = 0)

    comfort_q = forms.IntegerField(help_text = "Enter a minimun number for comfort", max_value = 10, min_value = 0)

    looks_q = forms.IntegerField(help_text = "Enter a minimum number for looks", max_value = 10, min_value = 0)

