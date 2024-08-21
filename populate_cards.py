import requests
import os
import django
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mtg_commander_cube_generator.settings')
django.setup()

from cube_generator.models import Card

logging.basicConfig(level=logging.DEBUG)

def safe_int(value):
    """Convert value to an integer, or return None if not valid."""
    try:
        if value == '*':
            return None  # or some special value if you want to treat '*' as a placeholder
        return int(value)
    except (ValueError, TypeError):
        return None

def extract_card_faces(card_data):
    """Extract card faces, or handle as a single card if no faces."""
    card_faces_data = []
    
    # If 'card_faces' is present, handle the faces
    if 'card_faces' in card_data:
        faces = card_data['card_faces']
        
        # If the two faces are identical, use only one
        if len(faces) == 2 and faces[0] == faces[1]:
            card_faces_data.append(faces[0])
        else:
            # Process each face separately if they differ
            card_faces_data.extend(faces)
    else:
        # If no 'card_faces', treat as a single card
        card_faces_data.append(card_data)
    
    return card_faces_data

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
        card_faces = extract_card_faces(card)

        # Step 5.1: Check if any face is missing the 'type_line'. If so, skip the card entirely.
        if any('type_line' not in face for face in card_faces):
            logging.error(f"Skipping card due to missing 'type_line': {card['name']} (ID: {card['id']})")
            continue  # Skip to the next card

        for face in card_faces:
            defaults = {
                'name': face['name'],
                'mana_cost': face.get('mana_cost'),
                'mana_value': face.get('cmc', 0),
                'type_line': face['type_line'],
                'oracle_text': face.get('oracle_text'),
                'keywords': ', '.join(face.get('keywords', [])),
                'power': safe_int(face['power']) if face.get('power') else None,
                'toughness': safe_int(face['toughness']) if face.get('toughness') else None,
                'color_identity': ''.join(card.get('color_identity', ['C'])),
                'set_name': card['set_name'],
                'rarity': card['rarity'],
                'edhrec_rank': card.get('edhrec_rank', 0),
                'img_url': face['image_uris']['normal'] if face.get('image_uris') else ''
            }

            Card.objects.update_or_create(
                scryfall_id=card['id'],  # Use the same scryfall_id for both faces or single-faced cards
                defaults=defaults
            )

    # Step 6: Print a success message after populating the database
    print('Successfully populated the database with Scryfall data')

if __name__ == '__main__':
    populate_cards()
