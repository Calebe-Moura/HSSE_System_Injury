from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ============================================================
# CHOICES
# ============================================================

UNIT_CHOICES = (
    ("ANY", "Anna Nery"),
    ("ATL", "Atlanta"),
    ("MQU", "Maria Quitéria"),
)

TYPE_CHOICES = (
    ("FAC", "First Aid Case"),
    ("MTC", "Medical Treatment Case"),
    ("RWC", "Restricted Work Case"),
    ("LTI", "Lost Time Injury"),
)

STATUS_CHOICES = (
    ("OPE", "Open"),
    ("CLO", "Closed"),
)

STATUS_ACTION_CHOICES = (
    ("ACT", "Active"),
    ("COM", "Completed"),
    ("EXP", "Expired"),
)

LOCATION_CHOICES = (
    ("ACC", "Accommodation"),
    ("AST", "Ashore / Travel"),
    ("CAT", "Cargo Tank"),
    ("ENR", "Engine Room"),
    ("HEL", "Helideck"),
    ("MEP", "Main deck except process"),
    ("MOZ", "MOB / Zodiac"),
    ("PCA", "Process incl. HP compressor area"),
    ("PUP", "Pump Room"),
    ("SIY", "Site / Yard"),
    ("OTH", "Other"),
)

BODYPART_CHOICES = (
    ("ARM", "Arm(s)"),
    ("BAC", "Back"),
    ("EYE", "Eye(s)"),
    ("FIN", "Finger(s)"),
    ("FOO", "Foot / Feet"),
    ("HAN", "Hand"),
    ("HEA", "Head"),
    ("INT", "Internal Injury"),
    ("LEG", "Leg(s)"),
    ("LOW", "Lower body"),
    ("OTH", "Other"),
    ("SHO", "Shoulder"),
    ("TOR", "Torso"),
)

RISK_CHOICES = (
    ("ONE", "1 <|> 1 -> 1"),
    ("TWO", "1 <|> 2 -> 2"),
    ("THR", "2 <|> 1 -> 2"),
    ("FOU", "1 <|> 3 -> 3"),
    ("FIV", "3 <|> 1 -> 3"),
    ("SIX", "1 <|> 4 -> 4"),
    ("SEV", "2 <|> 2 -> 4"),
    ("EIG", "4 <|> 1 -> 4"),
    ("NIN", "1 <|> 5 -> 5"),
    ("TEN", "5 <|> 1 -> 5"),
    ("ELE", "2 <|> 3 -> 6"),
    ("TWE", "3 <|> 2 -> 6"),
    ("THI", "2 <|> 4 -> 8"),
    ("FOT", "4 <|> 2 -> 8"),
    ("FIF", "3 <|> 3 -> 9"),
    ("SIE", "2 <|> 5 -> 10"),
    ("SET", "5 <|> 2 -> 10"),
    ("EIT", "3 <|> 4 -> 12"),
    ("NIT", "4 <|> 3 -> 12"),
    ("TWN", "3 <|> 5 -> 15"),
    ("TON", "5 <|> 3 -> 15"),
    ("TTW", "4 <|> 4 -> 16"),
    ("TTH", "4 <|> 5 -> 20"),
    ("TFO", "5 <|> 4 -> 20"),
    ("TFI", "5 <|> 5 -> 25"),
)

TYPE_ACCIDENT_CHOICES = (
    ("ASS", "Assault or Violent Act"),
    ("AVI", "Aviation accidents"),
    ("CAU", "Caught In, Under or Between (excl. dropped objects)"),
    ("CON", "Confined Space"),
    ("CUT", "Cut, Puncture, Scrape"),
    ("DRO", "Dropped Objects"),
    ("EXB", "Explosions or Burns"),
    ("EXE", "Exposure: Electrical"),
    ("EXP", "Exposure: Noise, Chemical, Biological, Vibration"),
    ("FAL", "Falls from height"),
    ("ILL", "Illness"),
    ("OTH", "Other"),
    ("OVE", "Overexertion / Strain"),
    ("PRE", "Pressure release"),
    ("SLI", "Slips and Trips (at the same height)"),
    ("STR", "Struck By (excl. dropped object)"),
    ("WAT", "Water related, drowning"),
)

TYPE_INJURY_CHOICES = (
    ("ABR", "Abrasion"),
    ("ALL", "Allergic Reaction"),
    ("AMP", "Amputation"),
    ("BRU", "Bruise"),
    ("BUR", "Burn Chemical"),
    ("BUE", "Burn Electrical"),
    ("BUT", "Burn Thermal"),
    ("CON", "Concussion"),
    ("COT", "Contusion"),
    ("CRU", "Crush"),
    ("DIS", "Dislocation"),
    ("DYS", "Dysbaric illness"),
    ("ELE", "Electrocution"),
    ("FOR", "Foreign Body"),
    ("FRA", "Fracture"),
    ("GAS", "Gassing"),
    ("HEA", "Hearing Loss"),
    ("INC", "Incision"),
    ("INF", "Infection"),
    ("ING", "Ingestion"),
    ("INS", "Insect / Animal Bite or Sting"),
    ("IRR", "Irritation"),
    ("LAC", "Laceration"),
    ("LOC", "Loss of Consciousness"),
    ("LOS", "Loss of Sight"),
    ("MEN", "Mental illness"),
    ("OTH", "Other"),
    ("PEN", "Penetration"),
    ("PUN", "Puncture"),
    ("RAD", "Radiation"),
    ("RES", "Respiratory"),
    ("SCA", "Scald"),
    ("SKI", "Skin Disease"),
    ("SPR", "Sprain"),
    ("STA", "Stain"),
    ("TRO", "Tropical Disease"),
)


# ============================================================
# INJURY
# ============================================================

class Injury(models.Model):

    unit = models.CharField(
        max_length=3,
        choices=UNIT_CHOICES,
    )

    date_report = models.DateTimeField(
        default=timezone.now,
    )

    reported_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reported_injuries",
    )

    type_incident = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
    )

    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default="OPE",
    )

    cod_sys = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True,
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    date_incident = models.DateTimeField()

    responsible = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="responsible_injuries",
    )

    underlying_causes = models.TextField(
        blank=True,
    )

    location_incident = models.CharField(
        max_length=3,
        choices=LOCATION_CHOICES,
    )

    work_days_lost = models.PositiveIntegerField(
        default=0,
    )

    bodypart_injured = models.CharField(
        max_length=3,
        choices=BODYPART_CHOICES,
    )

    employer = models.CharField(
        max_length=50,
    )

    injured_person_name = models.CharField(
        max_length=80,
        blank=True,
    )

    condition_injured = models.TextField(
        blank=True,
    )

    risk_potencial = models.CharField(
        max_length=3,
        choices=RISK_CHOICES,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-date_incident"]
        verbose_name = "Injury"
        verbose_name_plural = "Injuries"

    def __str__(self):
        return f"{self.cod_sys} - {self.title}"

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            year = self.date_incident.year

            self.cod_sys = (
                f"{self.unit}/{year}/{self.pk:05d}"
            )

            super().save(
                update_fields=["cod_sys"]
            )

    @property
    def is_open(self):
        return self.status == "OPE"


# ============================================================
# TYPE OF ACCIDENT
# ============================================================

class TypeAccident(models.Model):

    injury = models.ForeignKey(
        Injury,
        on_delete=models.CASCADE,
        related_name="accident_types",
    )

    name = models.CharField(
        max_length=3,
        choices=TYPE_ACCIDENT_CHOICES,
    )

    class Meta:
        verbose_name = "Type of Accident"
        verbose_name_plural = "Types of Accident"
        ordering = ["name"]

    def __str__(self):
        return self.get_name_display() # type: ignore


# ============================================================
# TYPE OF INJURY
# ============================================================

class TypeInjury(models.Model):

    injury = models.ForeignKey(
        Injury,
        on_delete=models.CASCADE,
        related_name="injury_types",
    )

    name = models.CharField(
        max_length=3,
        choices=TYPE_INJURY_CHOICES,
    )

    class Meta:
        verbose_name = "Type of Injury"
        verbose_name_plural = "Types of Injury"
        ordering = ["name"]

    def __str__(self):
        return self.get_name_display() # type: ignore


# ============================================================
# ACTION
# ============================================================

class ActionInjury(models.Model):

    injury = models.ForeignKey(
        Injury,
        on_delete=models.CASCADE,
        related_name="actions",
    )

    limit_date_action = models.DateTimeField()

    completed_date_action = models.DateTimeField(
        null=True,
        blank=True,
    )

    responsible = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="injury_actions",
    )

    task = models.TextField()

    description = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=3,
        choices=STATUS_ACTION_CHOICES,
        default="ACT",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["limit_date_action"]
        verbose_name = "Injury Action"
        verbose_name_plural = "Injury Actions"

    def __str__(self):
        return (
            f"{self.injury.cod_sys} - "
            f"{self.task[:50]}"
        )