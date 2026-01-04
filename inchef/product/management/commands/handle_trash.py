from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from product.models import Product


class Command(BaseCommand):
    help = 'Move expired products to trash and delete old trashed products'

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # 1. В TRASH (3 часа)
        to_trash = Product.objects.filter(
            is_active=True,
            created_at__lte=now - timedelta(hours=3)
        )

        for product in to_trash:
            product.move_to_trash()

        # 2. УДАЛЕНИЕ (2 часа в trash)
        to_delete = Product.objects.filter(
            is_active=False,
            trashed_at__lte=now - timedelta(hours=2)
        )

        deleted_count = to_delete.count()
        to_delete.delete()

        self.stdout.write(
            f'Trashed: {to_trash.count()}, Deleted: {deleted_count}'
        )
