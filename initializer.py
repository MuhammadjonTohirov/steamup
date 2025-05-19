#!/usr/bin/env python
import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'steamup_platform.settings')
django.setup()

from users.models.LearningDomain import LearningDomain
from users.models.LearningMotivation import LearningMotivation
from users.models.LearningPeriodTarget import LearningPeriodTarget
from django.utils.translation import activate, get_language


def initialize_learning_domains():
    """
    Initialize learning domains with translations for en, uz, and ru
    """
    print("Initializing Learning Domains...")
    
    domains = [
        {
            'title': 'Science',
            'translations': {
                'en': 'Science',
                'uz': 'Ilm-fan',
                'ru': 'Наука'
            }
        },
        {
            'title': 'Technology',
            'translations': {
                'en': 'Technology',
                'uz': 'Texnologiya',
                'ru': 'Технология'
            }
        },
        {
            'title': 'Engineering',
            'translations': {
                'en': 'Engineering',
                'uz': 'Muhandislik',
                'ru': 'Инженерия'
            }
        },
        {
            'title': 'Math',
            'translations': {
                'en': 'Mathematics',
                'uz': 'Matematika',
                'ru': 'Математика'
            }
        },
        {
            'title': 'Computer Science',
            'translations': {
                'en': 'Computer Science',
                'uz': 'Kompyuter fanlari',
                'ru': 'Информатика'
            }
        },
        {
            'title': 'Robotics',
            'translations': {
                'en': 'Robotics',
                'uz': 'Robototexnika',
                'ru': 'Робототехника'
            }
        },
        {
            'title': 'Astronomy',
            'translations': {
                'en': 'Astronomy',
                'uz': 'Astronomiya',
                'ru': 'Астрономия'
            }
        },
        {
            'title': 'Environmental Science',
            'translations': {
                'en': 'Environmental Science',
                'uz': 'Ekologiya',
                'ru': 'Экология'
            }
        },
        {
            'title': 'Physics',
            'translations': {
                'en': 'Physics',
                'uz': 'Fizika',
                'ru': 'Физика'
            }
        },
        {
            'title': 'Chemistry',
            'translations': {
                'en': 'Chemistry',
                'uz': 'Kimyo',
                'ru': 'Химия'
            }
        },
        {
            'title': 'Biology',
            'translations': {
                'en': 'Biology',
                'uz': 'Biologiya',
                'ru': 'Биология'
            }
        }
    ]
    
    for domain_data in domains:
        # Check if domain already exists
        existing_domain = LearningDomain.objects.filter(title=domain_data['title']).first()
        
        if not existing_domain:
            # Create new domain
            domain = LearningDomain.objects.create(title=domain_data['title'])
            
            # Add translations
            for lang_code, translation in domain_data['translations'].items():
                domain.set_current_language(lang_code)
                domain.name_translated = translation
                domain.save()
            
            print(f"Created domain: {domain_data['title']}")
        else:
            print(f"Domain already exists: {domain_data['title']}")


def initialize_learning_motivations():
    """
    Initialize learning motivations with translations for en, uz, and ru
    """
    print("Initializing Learning Motivations...")
    
    motivations = [
        {
            'title': 'Just for fun',
            'translations': {
                'en': 'Just for fun',
                'uz': 'Shunchaki qiziq',
                'ru': 'Просто для удовольствия'
            }
        },
        {
            'title': 'Improve my career',
            'translations': {
                'en': 'Improve my career',
                'uz': 'Karyeramni rivojlantirish',
                'ru': 'Улучшить карьеру'
            }
        },
        {
            'title': 'Support my education',
            'translations': {
                'en': 'Support my education',
                'uz': "Ta'limni qo'llab-quvvatlash",
                'ru': 'Поддержать образование'
            }
        },
        {
            'title': 'Personal growth',
            'translations': {
                'en': 'Personal growth',
                'uz': 'Shaxsiy rivojlanish',
                'ru': 'Личностный рост'
            }
        },
        {
            'title': 'Contribution to society',
            'translations': {
                'en': 'Contribution to society',
                'uz': 'Jamiyatga hissa qo\'shish',
                'ru': 'Вклад в общество'
            }
        }
    ]
    
    for motivation_data in motivations:
        # Check if motivation already exists
        existing_motivation = LearningMotivation.objects.filter(title=motivation_data['title']).first()
        
        if not existing_motivation:
            # Create new motivation
            motivation = LearningMotivation.objects.create(title=motivation_data['title'])
            
            # Add translations
            for lang_code, translation in motivation_data['translations'].items():
                motivation.set_current_language(lang_code)
                motivation.tr_title = translation
                motivation.save()
            
            print(f"Created motivation: {motivation_data['title']}")
        else:
            print(f"Motivation already exists: {motivation_data['title']}")


def initialize_learning_period_targets():
    """
    Initialize learning period targets (daily goals) with translations for en, uz, and ru
    """
    print("Initializing Learning Period Targets...")
    
    targets = [
        {
            'period_unit': 'daily',
            'repeat_count': 1,
            'complement': 'Just getting started',
            'translations': {
                'en': 'Take it easy',
                'uz': 'Bosqichma-bosqich',
                'ru': 'Не торопясь'
            }
        },
        {
            'period_unit': 'daily',
            'repeat_count': 2,
            'complement': 'Building a habit',
            'translations': {
                'en': 'Building a habit',
                'uz': 'Odatni shakllantirish',
                'ru': 'Формирование привычки'
            }
        },
        {
            'period_unit': 'daily',
            'repeat_count': 5,
            'complement': 'Consistent learner',
            'translations': {
                'en': 'Consistent learner',
                'uz': 'Doimiy o\'rganuvchi',
                'ru': 'Постоянный ученик'
            }
        },
        {
            'period_unit': 'daily',
            'repeat_count': 10,
            'complement': 'Ambitious achiever',
            'translations': {
                'en': 'Ambitious achiever',
                'uz': 'Shuhratparast yutuqqa erishuvchi',
                'ru': 'Амбициозный ученик'
            }
        },
        {
            'period_unit': 'weekly',
            'repeat_count': 3,
            'complement': 'Weekend warrior',
            'translations': {
                'en': 'Weekend warrior',
                'uz': 'Dam olish kunlari o\'rganuvchi',
                'ru': 'Выходной воин'
            }
        },
        {
            'period_unit': 'weekly',
            'repeat_count': 5,
            'complement': 'Steady progress',
            'translations': {
                'en': 'Steady progress',
                'uz': 'Barqaror progress',
                'ru': 'Стабильный прогресс'
            }
        },
        {
            'period_unit': 'monthly',
            'repeat_count': 15,
            'complement': 'Monthly milestone',
            'translations': {
                'en': 'Monthly milestone',
                'uz': 'Oylik maqsad',
                'ru': 'Ежемесячная цель'
            }
        }
    ]
    
    for target_data in targets:
        # Check if target with same period_unit and repeat_count exists
        existing_target = LearningPeriodTarget.objects.filter(
            period_unit=target_data['period_unit'],
            repeat_count=target_data['repeat_count']
        ).first()
        
        if not existing_target:
            # Create new target
            target = LearningPeriodTarget.objects.create(
                period_unit=target_data['period_unit'],
                repeat_count=target_data['repeat_count'],
                complement=target_data['complement']
            )
            
            # Add translations
            for lang_code, translation in target_data['translations'].items():
                target.set_current_language(lang_code)
                target.tr_complement = translation
                target.save()
            
            print(f"Created target: {target_data['period_unit']} x {target_data['repeat_count']}")
        else:
            print(f"Target already exists: {target_data['period_unit']} x {target_data['repeat_count']}")


def main():
    """
    Initialize all data
    """
    # Store current language
    current_language = get_language()
    
    try:
        # Initialize data
        initialize_learning_domains()
        initialize_learning_motivations()
        initialize_learning_period_targets()
        
        print("Initialization completed successfully!")
    except Exception as e:
        print(f"Error during initialization: {e}")
    finally:
        # Restore language
        if current_language:
            activate(current_language)


if __name__ == "__main__":
    main()