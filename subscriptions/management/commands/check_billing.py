from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from subscriptions.models import Subscription


class Command(BaseCommand):
    help = "Отправляет email-напоминания по подпискам, до списания которых осталось 3 дня или меньше"

    def handle(self, *args, **options):
        subs = Subscription.objects.filter(is_active=True).select_related('user')
        sent = 0

        for sub in subs:
            if sub.days_left <= 3 and sub.user.email:
                send_mail(
                    subject=f"SubTracker: скоро списание - {sub.title}",
                    message=(
                        f"Здравствуйте, {sub.user.username}!\n\n"
                        f"Через {sub.days_left} дн. ({sub.billing_date}) спишется "
                        f"{sub.price} грн за подписку «{sub.title}».\n\n"
                        f"- SubTracker"
                    ),
                    from_email=None,
                    recipient_list=[sub.user.email],
                    fail_silently=False,
                )
                sent += 1

        self.stdout.write(self.style.SUCCESS(f"Отправлено писем: {sent}"))
