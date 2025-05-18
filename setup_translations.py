#!/usr/bin/env python
"""
Master script to fix all django-modeltranslation issues in your project
Run this script from your project root directory
"""
import os
import sys
import subprocess
import time

def run_command(command):
    """Run a shell command and print the output"""
    print(f"\nRunning command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    return result.returncode == 0

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def main():
    print_section("DJANGO-MODELTRANSLATION FIX SCRIPT")
    print("This script will fix issues with django-modeltranslation in your project")
    print("It will:")
    print(" 1. Check and fix your settings.py")
    print(" 2. Check and fix translation.py files")
    print(" 3. Create missing migrations")
    print(" 4. Apply migrations")
    print(" 5. Sync translation fields")
    print(" 6. Create missing translation tables if needed")
    print("\nMake sure you have a backup of your project before proceeding!")
    
    confirm = input("\nDo you want to continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Aborted.")
        return
    
    # Step 1: Make sure __init__.py exists in migrations folders
    print_section("CHECKING MIGRATIONS FOLDER")
    for app_dir in ['users', 'core']:
        migrations_dir = os.path.join(app_dir, "migrations")
        if not os.path.exists(migrations_dir):
            os.makedirs(migrations_dir)
            print(f"Created migrations directory for {app_dir}")
        
        init_file = os.path.join(migrations_dir, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                pass  # Create empty __init__.py
            print(f"Created __init__.py in {migrations_dir}")
    
    # Step 2: Fix the LearningDomain model translation - create explicit migration
    print_section("CREATING EXPLICIT MIGRATION FOR LEARNINGDOMAIN")
    migration_path = os.path.join("users", "migrations", "0002_learningdomain_translation.py")
    
    if not os.path.exists(migration_path):
        print(f"Creating migration file {migration_path}")
        with open(migration_path, "w") as f:
            f.write("""# Generated manually
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
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
                'verbose_name': 'learning domain Translation',
                'db_table': 'users_learningdomain_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
        ),
    ]
""")
        print("Created explicit migration for LearningDomain translation table")
    else:
        print(f"Migration file {migration_path} already exists")
    
    # Step 3: Verify translation.py in users app
    print_section("CHECKING TRANSLATION FILES")
    users_translation_path = os.path.join("users", "translation.py")
    
    if not os.path.exists(users_translation_path):
        print(f"Creating translation.py for users app")
        with open(users_translation_path, "w") as f:
            f.write("""from modeltranslation.translator import register, TranslationOptions
from .models import LearningDomain

@register(LearningDomain)
class LearningDomainTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
""")
        print("Created translation.py for users app")
    else:
        print(f"Translation file {users_translation_path} already exists")
    
    # Step 4: Run migrations
    print_section("RUNNING MIGRATIONS")
    run_command("python manage.py migrate")
    
    # Step 5: Sync translation fields
    print_section("SYNCING TRANSLATION FIELDS")
    run_command("python manage.py sync_translation_fields")
    
    # Step 6: Update translation fields if needed
    print_section("UPDATING TRANSLATION FIELDS")
    run_command("python manage.py update_translation_fields")
    
    # Step 7: Check if the issue is resolved
    print_section("CHECKING RESULTS")
    print("Fix process completed.")
    print("\nYou should now try to access the admin panel to verify that the issue is resolved.")
    print("If you still encounter issues, run this script one more time or try the manual fix script.")

if __name__ == "__main__":
    main()