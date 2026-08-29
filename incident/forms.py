from django import forms
from django.contrib.auth.models import User

from .models import (
    Injury,
    ActionInjury,
    TYPE_ACCIDENT_CHOICES,
    TYPE_INJURY_CHOICES,
)


# ============================================================
# HELPERS
# ============================================================

def bulma_class(field, css_class="input"):

    widget = field.widget

    if isinstance(widget, forms.Select):
        widget.attrs["class"] = "select"

    elif isinstance(widget, forms.SelectMultiple):
        widget.attrs["class"] = "select"

    elif isinstance(widget, forms.CheckboxSelectMultiple):
        widget.attrs["class"] = "checkbox"

    else:
        widget.attrs["class"] = css_class

    return field


# ============================================================
# INJURY FORM
# ============================================================

class InjuryForm(forms.ModelForm):

    # ========================================================
    # TYPE ACCIDENT
    # ========================================================

    type_accident = forms.MultipleChoiceField(
        required=False,
        choices=TYPE_ACCIDENT_CHOICES,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "checkbox",
            }
        ),
        label="Type of Accident",
    )

    # ========================================================
    # TYPE INJURY
    # ========================================================

    type_injury = forms.MultipleChoiceField(
        required=False,
        choices=TYPE_INJURY_CHOICES,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "checkbox",
            }
        ),
        label="Type of Injury",
    )

    # ========================================================
    # REPORTED BY
    # ========================================================

    reported_by = forms.ModelChoiceField(
        queryset=User.objects.filter(
            is_active=True
        ).order_by(
            "first_name",
            "last_name",
            "username",
        ),
        required=False,
        empty_label="Select user",
    )

    # ========================================================
    # RESPONSIBLE
    # ========================================================

    responsible = forms.ModelChoiceField(
        queryset=User.objects.filter(
            is_active=True
        ).order_by(
            "first_name",
            "last_name",
            "username",
        ),
        required=False,
        empty_label="Select responsible",
    )

    class Meta:

        model = Injury

        fields = [
            "unit",
            "date_report",
            "reported_by",
            "type_incident",
            "status",
            "title",
            "description",
            "date_incident",
            "responsible",
            "underlying_causes",
            "location_incident",
            "work_days_lost",
            "bodypart_injured",
            "employer",
            "injured_person_name",
            "condition_injured",
            "risk_potencial",
        ]

        widgets = {

            "unit": forms.Select(
                attrs={
                    "class": "select",
                }
            ),

            "date_report": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "type": "datetime-local",
                    "class": "input",
                },
            ),

            "type_incident": forms.Select(
                attrs={
                    "class": "select",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "select",
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "Incident title",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "textarea",
                    "rows": 4,
                }
            ),

            "date_incident": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "type": "datetime-local",
                    "class": "input",
                },
            ),

            "underlying_causes": forms.Textarea(
                attrs={
                    "class": "textarea",
                    "rows": 4,
                }
            ),

            "location_incident": forms.Select(
                attrs={
                    "class": "select",
                }
            ),

            "work_days_lost": forms.NumberInput(
                attrs={
                    "class": "input",
                    "min": 0,
                }
            ),

            "bodypart_injured": forms.Select(
                attrs={
                    "class": "select",
                }
            ),

            "employer": forms.TextInput(
                attrs={
                    "class": "input",
                }
            ),

            "injured_person_name": forms.TextInput(
                attrs={
                    "class": "input",
                }
            ),

            "condition_injured": forms.Textarea(
                attrs={
                    "class": "textarea",
                    "rows": 4,
                }
            ),

            "risk_potencial": forms.Select(
                attrs={
                    "class": "select",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # ====================================================
        # DATE FORMAT
        # ====================================================

        if self.instance and self.instance.pk:

            if self.instance.date_report:
                self.initial["date_report"] = (
                    self.instance.date_report.strftime(
                        "%Y-%m-%dT%H:%M"
                    )
                )

            if self.instance.date_incident:
                self.initial["date_incident"] = (
                    self.instance.date_incident.strftime(
                        "%Y-%m-%dT%H:%M"
                    )
                )

            # ================================================
            # EXISTING ACCIDENT TYPES
            # ================================================

            self.initial["type_accident"] = list(
                self.instance.accident_types.values_list(
                    "name",
                    flat=True,
                )
            )

            # ================================================
            # EXISTING INJURY TYPES
            # ================================================

            self.initial["type_injury"] = list(
                self.instance.injury_types.values_list(
                    "name",
                    flat=True,
                )
            )


# ============================================================
# ACTION FORM
# ============================================================

class ActionInjuryForm(forms.ModelForm):

    responsible = forms.ModelChoiceField(
        queryset=User.objects.filter(
            is_active=True
        ).order_by(
            "first_name",
            "last_name",
            "username",
        ),
        required=False,
        empty_label="Select responsible",
    )

    class Meta:

        model = ActionInjury

        fields = [
            "limit_date_action",
            "completed_date_action",
            "responsible",
            "task",
            "description",
            "status",
        ]

        widgets = {

            "limit_date_action": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "type": "datetime-local",
                    "class": "input",
                },
            ),

            "completed_date_action": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "type": "datetime-local",
                    "class": "input",
                },
            ),

            "task": forms.Textarea(
                attrs={
                    "class": "textarea",
                    "rows": 3,
                    "placeholder": "Action task",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "textarea",
                    "rows": 4,
                    "placeholder": "Action description",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "select",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:

            if self.instance.limit_date_action:
                self.initial["limit_date_action"] = (
                    self.instance.limit_date_action.strftime(
                        "%Y-%m-%dT%H:%M"
                    )
                )

            if self.instance.completed_date_action:
                self.initial["completed_date_action"] = (
                    self.instance.completed_date_action.strftime(
                        "%Y-%m-%dT%H:%M"
                    )
                )