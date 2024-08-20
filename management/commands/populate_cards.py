import requests
from django.core.management.base import BaseCommand
from cards.models import Card


class Command(BaseCommand):
    help = 'Populate the database with Scryfall bulk data'

    def handle(self, *args, **kwargs):
        # Step 1: Fetch the bulk data metadata from Scryfall
        response = requests.get('https://api.scryfall.com/bulk-data')
        bulk_data = response.json()  # 'bulk_data' is defined here as the JSON response

        # Step 2: Find the specific URL for the 'default_cards' bulk data
        all_cards_url = None
        for item in bulk_data['data']:
            if item['type'] == 'default_cards':  # Check if the item is for 'default_cards'
                # Set the download URL for card data
                all_cards_url = item['download_uri']
                break  # Stop searching once we've found the URL

        # Step 3: If we can't find the URL, print an error and exit
        if not all_cards_url:
            self.stdout.write(self.style.ERROR('Could not find bulk data URL'))
            return

        # Step 4: Fetch the actual card data from the URL we found
        response = requests.get(all_cards_url)
        # Convert the downloaded card data into a Python dictionary
        card_data = response.json()

        # Step 5: Populate the database with the card data
        for card in card_data:
            # Prepare the fields for the Card model
            defaults = {
                'name': card['name'],
                'mana_cost': card.get('mana_cost'),
                # 'cmc' from Scryfall is used for 'mana_value'
                'mana_value': card.get('cmc', 0),
                'type_line': card['type_line'],
                'oracle_text': card.get('oracle_text'),
                # Join keywords into a string
                'keywords': ', '.join(card.get('keywords', [])),
                # Convert power to an integer
                'power': int(card['power']) if card.get('power') else None,
                # Convert toughness to an integer
                'toughness': int(card['toughness']) if card.get('toughness') else None,
                # Convert color identity to a string
                'color_identity': ''.join(card.get('color_identity', ['C'])),
                'set_name': card['set_name'],
                'rarity': card['rarity'],
                # Use 0 if 'edhrec_rank' is not available
                'edhrec_rank': card.get('edhrec_rank', 0),
                # Handle missing images
                'img_url': card['image_uris']['normal'] if card.get('image_uris') else ''
            }

            # Create a new Card object or update an existing one with the same scryfall_id
            Card.objects.update_or_create(
                # Use 'scryfall_id' as the unique identifier
                scryfall_id=card['id'],
                defaults=defaults  # Update or set the fields as specified in 'defaults'
            )

        # Step 6: Print a success message after populating the database
        self.stdout.write(self.style.SUCCESS(
            'Successfully populated the database with Scryfall data'))
