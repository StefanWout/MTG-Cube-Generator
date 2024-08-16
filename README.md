# MTG-Cube-Generator

**Learning SQL and creating a draftable set of cards for a variety of Magic the Gathering experiences**

## MTG Cube Generator Problem Statement:

I want to generate a commander cube based on a chosen set of deck archetypes.

## Target Audience:

- Entrenched Magic Players
- Players new to limited formats that don’t want to spend money

## MVP Features:

- Fully searchable card database by all the data fields provided in the original model as well as searching by archetype.
- Users can set limits on several factors when generating a cube:
  - Size of cube
  - Size of packs
  - Commander distribution
  - Color distribution
  - Card type distribution
  - Choice of sets
  - Power level
  - Choice of archetypes
- Ability for users to save and edit cubes
- User Authentication and Profile Management

## Additional Features:

- Users can upload their own collection and discover which archetypes are well supported
- Generate cubes out of the user’s collection

## System Architecture:

| Component  | Technology                                                                 |
|------------|-----------------------------------------------------------------------------|
| Frontend   | HTML, CSS, and Javascript (React.js)                                        |
| Backend    | Django                                                                      |
| Database   | PostgreSQL, CockroachDB, or Render                                          |
| API        | Scryfall integrated API ([https://scryfall.com/docs/api](https://scryfall.com/docs/api)) |
| Hosting    | Render                                                                      |

## Database Design - Models:

### Django User Model

This is the default model provided by Django for user authentication and profile management.

### Card Model

| Field Name       | Data Type                                     |
|------------------|-----------------------------------------------|
| `id`             | Auto                                          |
| `name`           | CharField                                     |
| `mana_cost`      | CharField (blank=True, null=True)             |
| `mana_value`     | NumField                                      |
| `type_line`      | CharField                                     |
| `oracle_text`    | CharField (blank=True, null=True)             |
| `keywords`       | CharField (blank=True, null=True)             |
| `power`          | NumField (blank=True, null=True)              |
| `toughness`      | NumField (blank=True, null=True)              |
| `color_identity` | CharField (choices: 'W', 'U', 'B', 'R', 'G', and their combinations) |
| `set_name`       | CharField                                     |
| `rarity`         | CharField                                     |
| `edhrec_rank`    | NumField                                      |
| `archetype_id`   | ForeignKey, ManyToManyField(Archetype)        |
| `img_url`        | URLField                                      |

### Archetype Model

| Field Name       | Data Type                         |
|------------------|-----------------------------------|
| `id`             | Auto                              |
| `name`           | CharField (unique=True)           |
| `description`    | CharField                         |
| `color_identities` | ForeignKey, ManyToManyField(Card) |

### Cube Model

| Field Name       | Data Type                               |
|------------------|-----------------------------------------|
| `id`             | Auto                                    |
| `name`           | CharField                               |
| `description`    | CharField                               |
| `cards`          | ManyToManyField(Card)                   |
| `archetypes`     | ManyToManyField(Archetype)              |
| `user`           | ForeignKey                              |