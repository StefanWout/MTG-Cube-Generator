import requests
import os
import django
from cube_generator.models import Card

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'mtg_commander_cube_generator.settings')
django.setup()


def populate_cards():
    # Step 1: Fetch the bulk data metadata from Scryfall
    response = requests.get('https://api.scryfall.com/bulk-data')
    bulk_data = response.json()

    # Step 2: Find the specific URL for the 'default_cards' bulk data
    all_cards_url = None
    for item in bulk_data['data']:
        if item['type'] == 'default_cards':
            all_cards_url = item['download_uri']
            break

    # Step 3: If we can't find the URL, print an error and exit
    if not all_cards_url:
        print('Could not find bulk data URL')
        return

    # Step 4: Fetch the actual card data from the URL we found
    response = requests.get(all_cards_url)
    card_data = response.json()

    # Step 5: Populate the database with the card data
    for card in card_data:
        defaults = {
            'name': card['name'],
            'mana_cost': card.get('mana_cost'),
            'mana_value': card.get('cmc', 0),
            'type_line': card['type_line'],
            'oracle_text': card.get('oracle_text'),
            'keywords': ', '.join(card.get('keywords', [])),
            'power': int(card['power']) if card.get('power') else None,
            'toughness': int(card['toughness']) if card.get('toughness') else None,
            'color_identity': ''.join(card.get('color_identity', ['C'])),
            'set_name': card['set_name'],
            'rarity': card['rarity'],
            'edhrec_rank': card.get('edhrec_rank', 0),
            'img_url': card['image_uris']['normal'] if card.get('image_uris') else ''
        }

        Card.objects.update_or_create(
            scryfall_id=card['id'],
            defaults=defaults
        )

    # Step 6: Print a success message after populating the database
    print('Successfully populated the database with Scryfall data')


if __name__ == '__main__':
    populate_cards()
