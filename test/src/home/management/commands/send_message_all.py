import logging

from django.core.management.base import BaseCommand
from scripts.send_to_all_users import FirebaseMessenger

logger = logging.getLogger(__name__)

class Command(BaseCommand):

    help = 'Send message to everyone'

    def add_arguments(self, parser):
        parser.add_argument(
            '-message',
            type=str,
            help='Message to send.'
        )
        parser.add_argument(
            '-title',
            type=str,
            help='title of message.'
        )

    def handle(self, *args, **options):
        FirebaseMessenger(message=options['message'],title=options['title'])