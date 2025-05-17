from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    """
    Create initial data for the application after migrations are applied.
    This includes learning domains and app configuration.
    """
    
    # Create initial learning domains
    LearningDomain = apps.get_model('users', 'LearningDomain')
    AppConfig = apps.get_model('core', 'AppConfig')
    
    # Create learning domains if they don't exist
    domains = [
        "Physics", "Chemistry", "Biology", "Mathematics", 
        "Computer Science", "Engineering", "Robotics", 
        "Astronomy", "Environmental Science"
    ]
    
    for domain in domains:
        LearningDomain.objects.get_or_create(name=domain)
    
    # Create app configuration if it doesn't exist
    AppConfig.objects.get_or_create(
        key="primary_color",
        defaults={"value": "#12D18E"}
    )
    
    AppConfig.objects.get_or_create(
        key="platform_name",
        defaults={"value": "SteamUp"}
    )