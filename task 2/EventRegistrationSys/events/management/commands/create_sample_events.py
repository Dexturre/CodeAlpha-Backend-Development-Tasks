from django.core.management.base import BaseCommand
from events.models import Event
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Create sample events for testing'

    def handle(self, *args, **kwargs):
        Event.objects.all().delete()
        now = datetime.now()
        events = [
            Event(title='Django Workshop', description='Learn Django basics', date=now + timedelta(days=5), location='Online'),
            Event(title='Python Conference', description='Annual Python conference', date=now + timedelta(days=15), location='New York'),
            Event(title='Tech Meetup', description='Monthly tech meetup', date=now + timedelta(days=30), location='San Francisco'),
        ]
        Event.objects.bulk_create(events)
        self.stdout.write(self.style.SUCCESS('Sample events created successfully.'))
