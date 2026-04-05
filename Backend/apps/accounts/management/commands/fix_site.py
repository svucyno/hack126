"""Management command: fix_site.
Sets the django.contrib.sites Site record to localhost:8000,
which allauth requires to build OAuth callback URLs correctly.
"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = "Set the Sites framework domain to localhost:8000 (required for allauth OAuth)."

    def handle(self, *args, **options):
        site, created = Site.objects.get_or_create(id=1)
        old_domain = site.domain
        site.domain = "localhost:8000"
        site.name = "DripFit (local)"
        site.save()
        if created:
            self.stdout.write(self.style.SUCCESS(
                "Created Site(id=1) with domain=localhost:8000"
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Updated Site(id=1): {old_domain!r} → 'localhost:8000'"
            ))
