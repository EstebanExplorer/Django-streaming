from django import forms


from .models import StreamingSetting



class EditCameraForm(forms.ModelForm):

    class Meta:
        model = StreamingSetting
        fields = ['cam1','cam2','cam3','cam4']
       