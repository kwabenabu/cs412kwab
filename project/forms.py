from django import forms
from django.contrib.auth.models import User
from .models import UserCard, Card, Player, CardSet, Profile

# User registration form
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Profile edit form
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class AddCardToCollectionForm(forms.ModelForm):
    """
    Form for adding a card to user's collection.
    """
    class Meta:
        model = UserCard
        fields = ['card', 'purchase_price', 'purchase_date', 'grade', 'grade_score', 'condition_note']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'card': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'grade_score': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'condition_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Exclude cards already in user's collection
        if user:
            owned_cards = UserCard.objects.filter(user=user).values_list('card', flat=True)
            self.fields['card'].queryset = Card.objects.exclude(id__in=owned_cards)


class EditUserCardForm(forms.ModelForm):
    """
    Form for editing a card in user's collection.
    """
    class Meta:
        model = UserCard
        fields = ['purchase_price', 'purchase_date', 'grade', 'grade_score', 'condition_note', 'for_sale', 'sale_price']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'grade_score': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'condition_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'for_sale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        for_sale = cleaned_data.get('for_sale')
        sale_price = cleaned_data.get('sale_price')

        if for_sale and not sale_price:
            raise forms.ValidationError("Sale price is required when marking card for sale.")
        
        return cleaned_data


class CardSearchForm(forms.Form):
    """
    Form for searching cards with multiple filters.
    """
    player_name = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter player name...'
        })
    )
    
    rarity = forms.ChoiceField(
        required=False,
        choices=[('', 'Any Rarity')] + Card.RARITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    card_set = forms.ModelChoiceField(
        required=False,
        queryset=CardSet.objects.all(),
        empty_label="Any Set",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    min_value = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Value ($)',
            'step': '0.01'
        })
    )
    
    max_value = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Value ($)',
            'step': '0.01'
        })
    )
    
    position = forms.ChoiceField(
        required=False,
        choices=[('', 'Any Position')] + Player._meta.get_field('position').choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        min_value = cleaned_data.get('min_value')
        max_value = cleaned_data.get('max_value')

        if min_value and max_value and min_value > max_value:
            raise forms.ValidationError("Minimum value cannot be greater than maximum value.")
        
        return cleaned_data


class PlayerFilterForm(forms.Form):
    """
    Form for filtering players list.
    """
    position = forms.ChoiceField(
        required=False,
        choices=[('', 'All Positions')] + Player._meta.get_field('position').choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    country = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by country...'
        })
    )
    
    club_team = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by team...'
        })
    )


class CardSetFilterForm(forms.Form):
    """
    Form for filtering card sets list.
    """
    brand = forms.ChoiceField(
        required=False,
        choices=[('', 'All Brands')] + CardSet._meta.get_field('brand').choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    year_from = forms.IntegerField(
        required=False,
        min_value=1990,
        max_value=2025,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'From Year'
        })
    )
    
    year_to = forms.IntegerField(
        required=False,
        min_value=1990,
        max_value=2025,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'To Year'
        })
    )
