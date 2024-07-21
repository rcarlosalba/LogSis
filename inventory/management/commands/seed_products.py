from django.core.management.base import BaseCommand
from django_seed import Seed
from inventory.models import Product
import random


class Command(BaseCommand):
    help = 'Seed the database with sabple products'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int,
                            help='The number of fake products to create')

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        number = options['number']

        seeder.add_entity(Product, number, {
            'name': lambda x: seeder.faker.name(),
            'description': lambda x: seeder.faker.text(),
            'price': lambda x: round(random.uniform(10.0, 1000.0), 2),
            'imagen_url': lambda x: f"https://picsum.photos/seed/{random.randint(1, 1000)}/300/200",
            'quantity': lambda x: random.randint(0, 100),
            'category': lambda x: random.choice(['Bicicletas', 'Repuestos', 'Accesorios', 'Mantenimiento']),
            'sku': lambda x: seeder.faker.uuid4()
        })

        seeder.execute()

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded {number} products'))
