from django.db import models

class CustomPermissionsMixin(models.Model):
    """
    
    This is a custom PermissionMixis model, this is made to fix conflicting name issue 
    for the predefined 'auth.User' since 'CustomUser' also includes the name 'User'. 
    This class would then created tables that have ManyToMany relationship. This would
    then add the required permissions for the CustomUser model. It would also add 
    it on a auth group and as well having the user within the group to have permissions
    for the user.    

    """

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_users',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_users',
        related_query_name='custom_user',
    )

    class Meta:
        abstract = True