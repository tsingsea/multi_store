from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField(label="上传Excel文件")
