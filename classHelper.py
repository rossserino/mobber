class ClassHelper:
  """
  Per-class leveling profiles for pre-renewal (Project Alfheim).

  Each profile describes which targets a class hunts efficiently:
  - elements: target defense elements the class exploits (None = any element)
  - races: target races the class exploits (None = any race)
  - sizes: preferred target sizes given the class' weapon penalties (None = any)
  - notes: short qualitative tips (signature skills, converters/endows)

  Profiles are keyed by second class; transcendent classes reuse the same
  profile with a higher default level band. These are starting points, not
  gospel - Alfheim has custom skill/monster adjustments, so verify in game.
  """

  ELEMENTS_ALL = ["Neutral", "Water", "Earth", "Fire", "Wind",
                  "Poison", "Holy", "Dark", "Ghost", "Undead"]

  PROFILES = {
    "knight": {
      "elements": None,  # Bowling Bash is neutral, works on everything but Ghost
      "races": None,
      "sizes": ["Medium", "Large"],
      "notes": [
        "Bowling Bash (neutral) clears dense packs of almost any element - avoid Ghost, which resists neutral.",
        "Spears + Pierce excel vs Large targets; swords are steadier vs Small/Medium.",
        "Ask a Sage for an Endow to exploit a specific map's element.",
      ],
    },
    "crusader": {
      "elements": ["Undead", "Dark"],
      "races": ["Undead", "Demon"],
      "sizes": None,
      "notes": [
        "Holy Cross and Grand Cross hit Undead and Demon targets hardest.",
        "Faith + Holy-element weapon (or Aspersio) stacks with the above.",
        "Shield builds can mob up with Shield Reflect where it is available.",
      ],
    },
    "wizard": {
      "elements": ["Fire", "Water", "Wind", "Earth", "Undead"],
      "races": None,
      "sizes": None,
      "notes": [
        "Match the spell to the target: Storm Gust -> Fire, Meteor Storm -> Earth/Undead, Lord of Vermilion -> Water, Heaven's Drive -> Wind.",
        "Quagmire, Ice Wall and Safety Wall let you farm above your weight.",
        "Holy/Dark/Ghost/Poison packs are usually someone else's job.",
      ],
    },
    "sage": {
      "elements": ["Fire", "Water", "Wind", "Earth"],
      "races": None,
      "sizes": None,
      "notes": [
        "Hindsight auto-bolts pair with your own Endows - pick the bolt the map is weak to.",
        "Dispell / Spellbreaker shut down caster mobs; wear status protection.",
        "Strong party support: Endows, Deluge/Volcano/Violent Gale floors, Magic Rod.",
      ],
    },
    "hunter": {
      "elements": None,  # arrows/converters cover every element
      "races": None,
      "sizes": ["Small", "Medium"],
      "notes": [
        "Carry converters (or Silver arrows for Undead/Dark) and match the arrow to the map.",
        "Bows lose damage vs Large - prefer Small/Medium unless your bow outgears it.",
        "Blitz Beat is neutral: solid filler, but avoid Ghost with it.",
      ],
    },
    "bard_dancer": {
      "elements": None,
      "races": None,
      "sizes": None,
      "notes": [
        "Arrow Vulcan is neutral ranged damage - good on dense packs, weak vs Ghost.",
        "Elemental arrows/converters cover whatever Arrow Vulcan cannot.",
        "Duet with a Bard/Dancer partner for Ensemble levels and faster kills.",
      ],
    },
    "blacksmith": {
      "elements": None,  # Mammonite is neutral
      "races": None,
      "sizes": ["Medium", "Large"],
      "notes": [
        "Mammonite is neutral - bring zeny, avoid Ghost, and let Adrenaline Rush do the work.",
        "Axes shine vs Large and suffer vs Small; maces are steadier vs Small/Medium.",
        "Hammer Fall stuns packs; Weapon Perfection ignores size penalties when needed.",
      ],
    },
    "alchemist": {
      "elements": None,  # Acid Terror is neutral ranged
      "races": None,
      "sizes": None,
      "notes": [
        "Acid Terror is ranged neutral damage - few matchups are bad.",
        "Your homunculus tanks and finishes: Lif/Vanil for support, Amistr/Filir for damage.",
        "Aid Potion and slim potions keep both of you upright on hard maps.",
      ],
    },
    "assassin": {
      "elements": None,  # converters cover every element
      "races": None,
      "sizes": ["Small", "Medium"],
      "notes": [
        "Katars lose damage vs Large - hunt Small/Medium or switch weapon.",
        "Converters pick the element; Enchant Poison is free damage over time.",
        "Sonic Blow / Grimtooth are neutral finishers - avoid Ghost with them.",
      ],
    },
    "rogue": {
      "elements": None,
      "races": None,
      "sizes": ["Small", "Medium"],
      "notes": [
        "Daggers want Small targets; bows + Double Strafe want range and the right arrow.",
        "Plagiarize enemy AoE or bolts to farm above your weight.",
        "Backstab and strip skills add party value on tougher maps.",
      ],
    },
    "priest": {
      "elements": ["Undead", "Dark"],
      "races": ["Undead", "Demon"],
      "sizes": None,
      "notes": [
        "Turn Undead only works on the Undead race (and is level-gated) - check the race column.",
        "Magnus Exorcismus shreds Demon/Undead packs; Aspersio makes any party physical.",
        "Holy Light finishes runners; bring Blue Gemstones and a Bless/Agi party.",
      ],
    },
    "monk": {
      "elements": None,
      "races": None,
      "sizes": None,
      "notes": [
        "Fists have no size penalty - hunt whatever has the best EXP/HP.",
        "Occult Impaction scales against high-DEF targets; Triple Attack combos build spheres.",
        "Guillotine Fist / Asura Strike finish high-HP targets - pack SP items.",
      ],
    },
  }

  TRANS_NOTE = (
    "Transcendent: same elemental logic at higher levels. Alfheim trans "
    "characters need more EXP per level, so favor high EXP/HP targets and parties."
  )

  # (display name, branch, tier, profile key, default level band)
  CLASSES = [
    ("Knight", "Swordsman", "2-1", "knight", (40, 85)),
    ("Crusader", "Swordsman", "2-2", "crusader", (40, 85)),
    ("Wizard", "Mage", "2-1", "wizard", (40, 85)),
    ("Sage", "Mage", "2-2", "sage", (40, 85)),
    ("Hunter", "Archer", "2-1", "hunter", (40, 85)),
    ("Bard", "Archer", "2-2", "bard_dancer", (40, 85)),
    ("Dancer", "Archer", "2-2", "bard_dancer", (40, 85)),
    ("Blacksmith", "Merchant", "2-1", "blacksmith", (40, 85)),
    ("Alchemist", "Merchant", "2-2", "alchemist", (40, 85)),
    ("Assassin", "Thief", "2-1", "assassin", (40, 85)),
    ("Rogue", "Thief", "2-2", "rogue", (40, 85)),
    ("Priest", "Acolyte", "2-1", "priest", (40, 85)),
    ("Monk", "Acolyte", "2-2", "monk", (40, 85)),
    ("Lord Knight", "Swordsman", "Trans", "knight", (60, 99)),
    ("Paladin", "Swordsman", "Trans", "crusader", (60, 99)),
    ("High Wizard", "Mage", "Trans", "wizard", (60, 99)),
    ("Professor", "Mage", "Trans", "sage", (60, 99)),
    ("Sniper", "Archer", "Trans", "hunter", (60, 99)),
    ("Clown", "Archer", "Trans", "bard_dancer", (60, 99)),
    ("Gypsy", "Archer", "Trans", "bard_dancer", (60, 99)),
    ("Whitesmith", "Merchant", "Trans", "blacksmith", (60, 99)),
    ("Creator", "Merchant", "Trans", "alchemist", (60, 99)),
    ("Assassin Cross", "Thief", "Trans", "assassin", (60, 99)),
    ("Stalker", "Thief", "Trans", "rogue", (60, 99)),
    ("High Priest", "Acolyte", "Trans", "priest", (60, 99)),
    ("Champion", "Acolyte", "Trans", "monk", (60, 99)),
  ]
