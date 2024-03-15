from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from bballcompapp.models import Game


class Command(BaseCommand):
    help = 'Checks for any upcoming games within the next hour starting from 8 AM'

    def handle(self, *args, **kwargs):
        # Calculate the start and end time for the next hour starting from 8 AM
        now = datetime.now()
        start_time = datetime(now.year, now.month, now.day, 8, 0, 0)
        end_time = start_time + timedelta(hours=1)

        # Query for upcoming games within the next hour
        upcoming_games = Game.objects.filter(start_time__gte=start_time, start_time__lt=end_time)

        # Trigger SMS notifications for each upcoming game
        for game in upcoming_games:
            print(f"Upcoming game: {game.home_team} vs {game.away_team} at {game.start_time}")
            # self.send_sms_notification(game)

    def send_sms_notification(self, game):
        from twilio.rest import Client
        account_sid = 'AC8f3ca5b6dbbc450456470c549a91ac7f'
        auth_token = 'b9e6e822413a838a3c9d1b3709f46a44'
      

        # Phone number to send the SMS notification to
        to_phone_number = '+18579916807'

        # Compose the SMS message
        message = f"Upcoming game: {game.home_team} vs {game.away_team} at {game.start_time}"

        # Send the SMS message
        message = client.messages.create(
            body=message,
            from_='+13307521464',  # Your Twilio phone number
            to='+18579916807'
        )

        print(f"SMS notification sent. SID: {message.sid}")
