from django.contrib.auth.models import User
from django.core.management.commands import migrate

from conf.models import Conf, Site, SitePermission


class Command(migrate.Command):
    help = 'Creates an initial Site and User (admin/admin) for Timestrap.'

    def handle(self, *args, **kwargs):
        super().handle(*args, **kwargs)

        default_site = Site.objects.get(id=1)
        Conf.objects.get_or_create(site=default_site)
        if default_site.domain == 'example.com':
            default_site.name = 'Timestrap'
            default_site.save()

        superusers = User.objects.filter(is_superuser=True)
        if len(superusers) == 0:
            default_superuser = User.objects.create_superuser(
                username='admin',
                password='admin',
                email='admin@example.com'
            )
            site_permission = SitePermission.objects.create(
                user=default_superuser
            )
            site_permission.sites.set(Site.objects.filter(id=1))
            site_permission.save()
