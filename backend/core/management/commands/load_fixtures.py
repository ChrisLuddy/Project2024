from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import os
import firebase_admin
from firebase_admin import firestore
import json
from core.firebase_models import Client, Fund, Portfolio, Asset, Order, TradeRating, AIForecast, SupportRequest
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Clears the SQLite and Firebase databases and loads fixtures"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database reset process...")

        self.stdout.write("Clearing SQLite database...")
        self.clear_sqlite_database()

        self.stdout.write("Clearing Firebase database...")
        self.clear_firebase_database()

        self.stdout.write("Loading fixtures into SQLite...")
        self.load_sqlite_fixtures()

        self.stdout.write("Loading fixtures into Firebase...")
        self.load_firebase_fixtures()

        self.stdout.write("Creating SuperUser if not exists...")
        self.create_superuser()

        self.stdout.write("Database reset and fixture loading completed successfully.")

    def clear_sqlite_database(self):
        """
        Clears all data from the SQLite database.
        """
        call_command("flush", interactive=False, verbosity=0)

    def clear_firebase_database(self):
        """
        Clears all collections from the Firebase database.
        """
        if not firebase_admin._apps:
            cred = firebase_admin.credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)

        db = firestore.client()

        collections = [
            'users',
            'clients',
            'funds',
            'portfolios',
            'assets',
            'orders',
            'trade_ratings',
            'ai_forecasts',
            'support_requests',
        ]

        for collection in collections:
            self.stdout.write(f"Deleting collection: {collection}")
            self.delete_collection(db.collection(collection), batch_size=100)

    def delete_collection(self, collection_ref, batch_size):
        """
        Deletes all documents in a Firebase collection in batches.
        """
        docs = collection_ref.limit(batch_size).stream()
        deleted = 0

        for doc in docs:
            doc.reference.delete()
            deleted += 1

        if deleted >= batch_size:
            return self.delete_collection(collection_ref, batch_size)

    def load_sqlite_fixtures(self):
        """
        Loads JSON fixtures into the SQLite database.
        """
        fixtures_dir = os.path.join(settings.BASE_DIR, 'core', 'fixtures')
        fixtures = [
            'users_fixture.json',  # SQLite-specific fixtures
        ]

        for fixture in fixtures:
            fixture_path = os.path.join(fixtures_dir, fixture)
            if os.path.exists(fixture_path):
                self.stdout.write(f"Loading fixture: {fixture}")
                call_command("loaddata", fixture)
            else:
                self.stderr.write(f"Fixture not found: {fixture}")

    def load_firebase_fixtures(self):
        """
        Loads JSON fixtures into Firebase collections.
        """
        fixtures_dir = os.path.join(settings.BASE_DIR, 'core', 'fixtures')
        fixtures = {
            'clients': Client,
            'funds': Fund,
            'portfolios': Portfolio,
            'assets': Asset,
            'orders': Order,
            'trade_ratings': TradeRating,
            'ai_forecasts': AIForecast,
            'support_requests': SupportRequest,
        }

        for collection_name, model_class in fixtures.items():
            fixture_path = os.path.join(fixtures_dir, f"{collection_name}_fixture.json")
            if os.path.exists(fixture_path):
                self.stdout.write(f"Loading fixture into Firebase: {collection_name}")
                with open(fixture_path, 'r') as f:
                    data = json.load(f)
                    for obj in data:
                        model_instance = model_class(**obj['fields'])
                        model_instance.save()
            else:
                self.stderr.write(f"Firebase fixture not found: {fixture_path}")

    def create_superuser(self):
        """
        Creates a superuser if not already exists.
        """
        superuser_email = "vladyslav.rastvorov@mycit.ie"
        superuser_password = "password_123"

        if not User.objects.filter(email=superuser_email).exists():
            self.stdout.write("Creating superuser...")
            User.objects.create_superuser(
                username="SuperAdmin",
                email=superuser_email,
                password=superuser_password,
                is_active=True,
            )
            self.stdout.write(f"Superuser created: {superuser_email}")
        else:
            self.stdout.write(f"Superuser already exists: {superuser_email}")
