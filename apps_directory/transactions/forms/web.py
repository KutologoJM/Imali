"""
Django forms for template-rendered views.

Docs: https://docs.djangoproject.com/en/stable/topics/forms/

Rules:
    - Forms handle two responsibilities: HTML input rendering and request data validation.
    - Once is_valid() passes, extract cleaned_data and pass it to a service — never save from a form directly.
    - Use ModelForm when the form maps closely to a model; use plain Form otherwise.
    - Keep validation in clean() and clean_<field>() — no business logic here.
    - Never use forms in API views — that is the job of input serializers.

Example:
    class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = ["title", "body"]

        def clean_title(self):
            value = self.cleaned_data["title"]
            if len(value) < 5:
                raise forms.ValidationError("Title must be at least 5 characters.")
            return value
"""
