# importing group class from django
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# import User model
from  django.contrib.auth.models import User 


def add_group(group_name, permitt):
    try:
        group_name = group_name.strip()  # Remove leading/trailing spaces
        if Group.objects.filter(name=group_name).exists():
            return True, f"A group with the name '{group_name}' already exists"
        
        new_group, created = Group.objects.get_or_create(name=group_name)

        ct = ContentType.objects.get_for_model(User)

        permit_codename = permitt.replace(" ", "_")

        permission, created = Permission.objects.get_or_create(
            codename=permit_codename,
            content_type=ct,
            defaults={'name': permitt}
        )

        new_group.permissions.add(permission)

        return True, "Group and permission added successfully"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"


   




