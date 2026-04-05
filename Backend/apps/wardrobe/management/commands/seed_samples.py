"""Seed 30 sample WardrobeItems (is_sample=True) into the database.

These are used for:
  1. Visual admin inspection
  2. Gap-filling when a user's wardrobe is missing a category slot
  3. Module 2 (Style Me) demonstration when the engine queries DB sample items

Running this command is idempotent — existing sample items are skipped.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from apps.wardrobe.models import WardrobeItem
from apps.engine.sample_dataset import SAMPLE_ITEMS


class Command(BaseCommand):
    help = "Seed 30 curated sample WardrobeItems (is_sample=True) into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--user-email",
            default="sample@dripfit.local",
            help="Email of the owner user for sample items (created if missing).",
        )

    def handle(self, *args, **options):
        email = options["user_email"]
        user, user_created = User.objects.get_or_create(
            email=email,
            defaults={"username": "sample_user", "is_active": False},
        )
        if user_created:
            self.stdout.write(f"Created placeholder user: {email}")

        created_count = 0
        skipped_count = 0

        for item_data in SAMPLE_ITEMS:
            # Use the item id string as a fingerprint to avoid duplicates
            sample_id_str = str(item_data.get("id", ""))
            if WardrobeItem.objects.filter(
                user=user,
                is_sample=True,
                caption__startswith=f"[{sample_id_str}]",
            ).exists():
                skipped_count += 1
                continue

            WardrobeItem.objects.create(
                user=user,
                image="",                          # no physical file for sample
                colour_hex=item_data.get("colour_hex", "#808080"),
                colour_name=item_data.get("colour_name", ""),
                item_type=item_data.get("item_type", "top"),
                item_subtype=item_data.get("item_subtype", ""),
                pattern=item_data.get("pattern", "solid"),
                formality=item_data.get("formality", 3),
                occasions=item_data.get("occasions", []),
                is_sample=True,
                caption=f"[{sample_id_str}] {item_data.get('colour_name','')} {item_data.get('item_subtype','')}",
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done — {created_count} sample items created, {skipped_count} already existed."
        ))
