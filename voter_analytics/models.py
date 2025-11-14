"""
File: voter_analytics/models.py
Author: kwabena <kwabena@bu.edu>
Description: Django models for voter analytics application. Contains the Voter model
and utility functions for importing voter data from CSV files.
"""

from typing import Optional
from django.db import models
from datetime import datetime, date
import csv
import os
from pathlib import Path


class Voter(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment = models.CharField(max_length=20, blank=True, null=True)
    zipcode = models.CharField(max_length=10)
    dob = models.DateField()
    registration_date = models.DateField()
    party = models.CharField(max_length=2)
    precinct = models.CharField(max_length=5)

    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    voter_score = models.IntegerField(default=0)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    @property
    def street_address(self) -> str:
        return f"{self.street_number} {self.street_name}".strip()

    @property
    def full_address(self) -> str:
        parts = [self.street_address]
        if self.apartment:
            parts.append(f"Apt {self.apartment}")
        # Default city/state since dataset is Newton, MA
        parts.append(f"Newton, MA {self.zipcode}")
        return ", ".join([p for p in parts if p])


def _parse_date(value: str) -> Optional[date]:
    """Parse a date string in various formats, handling edge cases like invalid days."""
    if not value:
        return None  # type: ignore
    value = str(value).strip()
    
    # Handle edge case of invalid dates like 1900-01-00
    if value.endswith("-00"):
        # Replace day 00 with day 01
        value = value[:-2] + "01"
    
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    # If nothing matched, raise to make the issue visible
    raise ValueError(f"Unrecognized date format: {value}")


def _parse_bool(value) -> bool:
    """Parse a boolean value from various string representations."""
    if value is None:
        return False
    s = str(value).strip().upper()
    return s in {"TRUE", "T", "1", "Y", "YES"}


def load_data(csv_path: Optional[str] = None):
    """
    Load Voter rows from the given CSV path. If not provided, looks for
    voter_analytics/data/newton_voters.csv next to this app.
    """
    if csv_path is None:
        app_dir = Path(__file__).resolve().parent
        csv_path = os.path.join(app_dir, "data", "newton_voters.csv")

    created = 0
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                party_val = (row.get("Party Affiliation") or "").strip()
                voter = Voter(
                    first_name=(row.get("First Name") or "").strip(),
                    last_name=(row.get("Last Name") or "").strip(),
                    street_number=(row.get("Residential Address - Street Number") or "").strip(),
                    street_name=(row.get("Residential Address - Street Name") or "").strip(),
                    apartment=(row.get("Residential Address - Apartment Number") or None),
                    zipcode=(row.get("Residential Address - Zip Code") or "").strip(),
                    dob=_parse_date(row.get("Date of Birth")),
                    registration_date=_parse_date(row.get("Date of Registration")),
                    party=party_val,
                    precinct=(row.get("Precinct Number") or "").strip(),
                    v20state=_parse_bool(row.get("v20state")),
                    v21town=_parse_bool(row.get("v21town")),
                    v21primary=_parse_bool(row.get("v21primary")),
                    v22general=_parse_bool(row.get("v22general")),
                    v23town=_parse_bool(row.get("v23town")),
                    voter_score=int((row.get("voter_score") or 0) or 0),
                )
                voter.save()
                created += 1
            except Exception as e:
                # For a real app we might log this with details
                raise
    return created
