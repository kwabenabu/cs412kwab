from django.contrib import admin
from .models import Voter


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "street_number",
        "street_name",
        "zipcode",
        "dob",
        "party",
        "voter_score",
    )
    list_filter = ("party", "precinct", "v20state", "v21town", "v21primary", "v22general", "v23town")
    search_fields = ("last_name", "first_name", "street_name", "zipcode")
