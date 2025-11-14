"""
File: voter_analytics/views.py
Author: kwabena kwabena@bu.edu
Description: Django views for voter analytics application. Provides list, detail, and
analytics views for voter data with filtering and visualization capabilities.

References:
- Django ListView documentation: https://docs.djangoproject.com/en/stable/ref/class-based-views/generic-display/#listview
- Django DetailView documentation: https://docs.djangoproject.com/en/stable/ref/class-based-views/generic-display/#detailview
- Django QuerySet filtering: https://docs.djangoproject.com/en/stable/topics/db/queries/#retrieving-specific-objects-with-filters
- Plotly Python documentation: https://plotly.com/python/
- Python Counter class: https://docs.python.org/3/library/collections.html#collections.Counter
"""

from collections import Counter
from datetime import date
from urllib.parse import urlencode
from typing import Tuple, Dict

from django.db.models import QuerySet
from django.views.generic import ListView, DetailView, TemplateView
from django.http import HttpRequest

from .models import Voter
from .forms import VoterFilterForm


def _filtered_queryset(request: HttpRequest) -> Tuple[QuerySet, VoterFilterForm, Dict]:
    """
    Create a filtered queryset of voters based on request parameters.
    
    Args:
        request: HTTP request containing filter parameters
        
    Returns:
        tuple: (filtered_queryset, form_instance, metadata_dict)
        
    Reference: Django QuerySet filtering - https://docs.djangoproject.com/en/stable/topics/db/queries/
    """
    qs = Voter.objects.all()

    # Dynamic choices
    parties = list(
        Voter.objects.exclude(party="").values_list("party", flat=True).distinct().order_by("party")
    )
    years = list(
        Voter.objects.values_list("dob", flat=True).order_by("dob")
    )
    year_choices = sorted({d.year for d in years if d})

    form = VoterFilterForm(
        data=request.GET or None,
        party_choices=parties,
        year_choices=year_choices,
    )

    if form.is_valid():
        data = form.cleaned_data
        # party
        party = data.get("party")
        if party:
            qs = qs.filter(party=party)

        # dob range
        min_year = data.get("dob_min_year")
        max_year = data.get("dob_max_year")
        if min_year:
            qs = qs.filter(dob__gte=date(int(min_year), 1, 1))
        if max_year:
            qs = qs.filter(dob__lte=date(int(max_year), 12, 31))

        # voter score
        score = data.get("voter_score")
        if score not in (None, ""):
            qs = qs.filter(voter_score=int(score))

        # elections (checkboxes)
        for flag in ["v20state", "v21town", "v21primary", "v22general", "v23town"]:
            if data.get(flag):
                qs = qs.filter(**{flag: True})

    return qs, form, {"party_choices": parties, "year_choices": year_choices}


class VoterListView(ListView):
    """
    Display a paginated list of voters with filtering capabilities.
    
    Supports filtering by party affiliation, birth year range, voter score,
    and participation in specific elections.
    
    Reference: Django ListView - https://docs.djangoproject.com/en/stable/ref/class-based-views/generic-display/#listview
    """
    model = Voter
    template_name = "voter_analytics/voter_list.html"
    paginate_by = 100
    context_object_name = "voters"
    ordering = ["last_name", "first_name"]

    def get_queryset(self):
        qs, form, _ = _filtered_queryset(self.request)
        return qs.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs, form, meta = _filtered_queryset(self.request)
        context.update({
            "filter_form": form,
            "total_count": Voter.objects.count(),
            "filtered_count": qs.count(),
        })
        return context


class VoterDetailView(DetailView):
    """
    Display detailed information for a single voter.
    
    Shows personal information, address, voting history, and participation statistics.
    
    Reference: Django DetailView - https://docs.djangoproject.com/en/stable/ref/class-based-views/generic-display/#detailview
    """
    model = Voter
    template_name = "voter_analytics/voter_detail.html"
    context_object_name = "voter"


class GraphsView(ListView):
    """
    Display interactive data visualizations and analytics for voter data.
    
    Generates charts using Plotly for:
    - Birth year distribution (bar chart)
    - Party affiliation distribution (pie chart) 
    - Election participation rates (bar chart)
    
    Falls back to summary statistics if Plotly is not available.
    
    References:
    - Plotly Python documentation: https://plotly.com/python/
    - Python Counter class: https://docs.python.org/3/library/collections.html#collections.Counter
    """
    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"

    def get_queryset(self):
        qs, form, _ = _filtered_queryset(self.request)
        return qs

    def get_context_data(self, **kwargs):
        """
        Generate context data including interactive charts using Plotly.
        
        Creates visualizations for birth year distribution, party affiliation,
        and election participation rates. Handles graceful fallback if Plotly
        is not available.
        
        Returns:
            dict: Context dictionary with chart HTML and form data
        """
        context = super().get_context_data(**kwargs)
        qs, form, _ = _filtered_queryset(self.request)

        # Attempt to build Plotly graphs; if plotly not available, show placeholders
        birth_year_html = party_html = elections_html = None
        try:
            import plotly.express as px

            # Birth year distribution
            years = [v.dob.year for v in qs if v.dob]
            if years:
                year_counts = Counter(years)
                fig1 = px.bar(x=sorted(year_counts.keys()), y=[year_counts[y] for y in sorted(year_counts.keys())],
                              labels={"x": "Birth Year", "y": "Voters"}, title="Voters by Birth Year")
                birth_year_html = fig1.to_html(full_html=False, include_plotlyjs="cdn")

            # Party affiliation distribution
            parties = [v.party or "" for v in qs]
            if parties:
                party_counts = Counter(parties)
                labels = list(party_counts.keys())
                values = [party_counts[p] for p in labels]
                fig2 = px.pie(names=labels, values=values, title="Voters by Party Affiliation")
                party_html = fig2.to_html(full_html=False, include_plotlyjs=False)

            # Participation counts per election
            elections = [
                ("2020 State", sum(1 for v in qs if v.v20state)),
                ("2021 Town", sum(1 for v in qs if v.v21town)),
                ("2021 Primary", sum(1 for v in qs if v.v21primary)),
                ("2022 General", sum(1 for v in qs if v.v22general)),
                ("2023 Town", sum(1 for v in qs if v.v23town)),
            ]
            labels = [e[0] for e in elections]
            values = [e[1] for e in elections]
            fig3 = px.bar(x=labels, y=values, labels={"x": "Election", "y": "Voted"}, title="Participation by Election")
            elections_html = fig3.to_html(full_html=False, include_plotlyjs=False)

        except Exception:
            # Leave HTML as None; template will show a helpful message
            pass

        # Calculate average voter score
        average_score = 0.0
        if qs.exists():
            total_score = sum(v.voter_score for v in qs)
            average_score = total_score / qs.count()

        context.update({
            "filter_form": form,
            "average_score": average_score,
            "graph_birth_year_html": birth_year_html,
            "graph_party_html": party_html,
            "graph_elections_html": elections_html,
        })
        return context
