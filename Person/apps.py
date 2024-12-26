from django.apps import AppConfig
from django.db.models.signals import post_migrate


class PersonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Person'

    def ready(self):
        post_migrate.connect(create_default_groups, sender=self)


def create_default_groups(sender, **kwargs):
    """
    Automates creation of default groups after migrations.
    """
    from django.contrib.auth.models import Group
    from django.contrib.auth.models import Permission

    default_groups_permissions = {
        "Admin": [
            "add_customuser", "change_customuser", "delete_customuser", "view_customuser",
            "add_customer", "change_customer", "delete_customer", "view_customer",
            "add_request", "change_request", "delete_request", "view_request",
            "add_requestorder", "change_requestorder", "delete_requestorder", "view_requestorder",
            "add_order", "change_order", "delete_order", "view_order",
            "add_service", "change_service", "delete_service", "view_service",
            "add_orderservice", "change_orderservice", "delete_orderservice", "view_orderservice",
            "add_orderimage", "change_orderimage", "delete_orderimage", "view_orderimage",
            "add_work", "change_work", "delete_work", "view_work",
        ],
        "Manager": [
            "add_customer", "change_customer", "delete_customer", "view_customer",
            "add_order", "change_order", "delete_order", "view_order",
            "add_orderimage", "change_orderimage", "delete_orderimage", "view_orderimage",
            "add_orderservice", "change_orderservice", "delete_orderservice", "view_orderservice",
            "add_request", "change_request", "delete_request", "view_request",
            "add_requestorder", "change_requestorder", "delete_requestorder", "view_requestorder",
            "add_service", "change_service", "delete_service", "view_service",
            "view_work",
        ],
        "Worker": [
            "view_order",
            "view_orderimage",
            "view_orderservice",
            "view_work",
        ],
    }
    for group_name, permissions in default_groups_permissions.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Group '{group_name}' created.")
        # Add permissions to group
        for perm_codename in permissions:
            try:
                perm = Permission.objects.get(codename=perm_codename)
                group.permissions.add(perm)
            except Permission.DoesNotExist:
                print(f"Permission '{perm_codename}' does not exist.")
