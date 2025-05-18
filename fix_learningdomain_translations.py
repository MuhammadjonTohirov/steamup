#!/usr/bin/env python
"""
Manual fix script for the "users_learningdomain_translation" missing table issue
This script creates a properly formatted migration file and applies it
"""
import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and print the output"""
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    return result.returncode == 0

def main():
    print("=" * 80)
    print(" FIXING MISSING LEARNINGDOMAIN TRANSLATION TABLE ".center(80, "="))
    print("=" * 80)
    
    # Step 1: Create a manual migration file for the translation table
    migrations_dir = os.path.join("users", "migrations")
    
    if not os.path.exists(migrations_dir):
        os.makedirs(migrations_dir)
        print(f"Created migrations directory: {migrations_dir}")
    
    init_file = os.path.join(migrations_dir, "__init__.py")
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            pass
        print(f"Created __init__.py in {migrations_dir}")
    
    # Create a migration file with a timestamp to ensure it runs after any existing migrations
    migration_path = os.path.join(migrations_dir, "9999_fix_learningdomain_translation.py")
    
    print(f"Creating migration file at {migration_path}")
    with open(migration_path, "w") as f:
        f.write("""# Manual migration to fix missing LearningDomain translation table
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),  # Update this to match your latest migration
    ]

    operations = [
        migrations.CreateModel(
            name='LearningDomainTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='users.LearningDomain')),
            ],
            options={
                'verbose_name': 'Learning Domain Translation',
                'db_table': 'users_learningdomain_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
        ),
    ]
""")
    
    print("Migration file created successfully")
    
    # Step 2: Create or check the users/translation.py file
    translation_path = os.path.join("users", "translation.py")
    
    if not os.path.exists(translation_path):
        print(f"Creating translation.py at {translation_path}")
        with open(translation_path, "w") as f:
            f.write("""from modeltranslation.translator import register, TranslationOptions
from .models import LearningDomain

@register(LearningDomain)
class LearningDomainTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
""")
        print("Translation file created successfully")
    else:
        print(f"Translation file already exists at {translation_path}")
    
    # Step 3: Apply the migration
    print("\nApplying migrations...")
    run_command("python manage.py migrate users")
    
    print("\nFix completed. The LearningDomain translation table should now be created.")
    print("Try accessing the admin interface again to see if the issue is resolved.")

if __name__ == "__main__":
    main()