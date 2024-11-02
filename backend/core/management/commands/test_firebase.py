# core/management/commands/test_firebase.py
from firebase_admin import firestore
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Test Firebase connection by writing and reading a document.'

    def handle(self, *args, **kwargs):
        try:
            # Initialize Firestore
            db = firestore.client()

            # Reference a test document
            doc_ref = db.collection('test').document('firebase_test')

            # Write data to the document
            test_data = {'message': 'Hello Firebase!'}
            doc_ref.set(test_data)
            self.stdout.write(self.style.SUCCESS('Successfully wrote test data to Firebase.'))

            # Read data from the document
            result = doc_ref.get()
            if result.exists:
                self.stdout.write(self.style.SUCCESS(f'Read data from Firebase: {result.to_dict()}'))
            else:
                self.stdout.write(self.style.ERROR('No data found in Firebase test document.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error connecting to Firebase: {e}'))
