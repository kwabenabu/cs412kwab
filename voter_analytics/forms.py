"""
File: voter_analytics/forms.py
Author: kwabena kwabena@bu.edu
Description: Django forms for voter analytics application. Provides filtering
form for voter data with dynamic choice fields.

Reference: Django Forms documentation - https://docs.djangoproject.com/en/stable/topics/forms/
"""

from django import forms


class VoterFilterForm(forms.Form):
    """
    Form for filtering voter data by various criteria.
    
    Provides dynamic choice fields for party affiliation, birth year range,
    voter score, and election participation checkboxes.
    
    Reference: Django Forms - https://docs.djangoproject.com/en/stable/topics/forms/
    """
    party = forms.ChoiceField(required=False)
    dob_min_year = forms.ChoiceField(required=False)
    dob_max_year = forms.ChoiceField(required=False)
    voter_score = forms.ChoiceField(required=False)

    v20state = forms.BooleanField(required=False)
    v21town = forms.BooleanField(required=False)
    v21primary = forms.BooleanField(required=False)
    v22general = forms.BooleanField(required=False)
    v23town = forms.BooleanField(required=False)

    def __init__(self, *args, party_choices=None, year_choices=None, score_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Add an empty choice at the top for optional filters
        if party_choices is None:
            party_choices = []
        if year_choices is None:
            year_choices = []
        if score_choices is None:
            score_choices = [(str(i), str(i)) for i in range(0, 6)]

        self.fields["party"].choices = [("", "All")] + [(p, p) for p in party_choices]
        self.fields["dob_min_year"].choices = [("", "Any")] + [(str(y), str(y)) for y in year_choices]
        self.fields["dob_max_year"].choices = [("", "Any")] + [(str(y), str(y)) for y in year_choices]
        self.fields["voter_score"].choices = [("", "All")] + list(score_choices)

