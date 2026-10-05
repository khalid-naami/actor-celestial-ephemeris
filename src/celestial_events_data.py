"""Major Meteor Showers, Solar & Lunar Eclipses Calendar, and Celestial Conjunctions."""

from typing import Dict, List, Any
import pandas as pd

METEOR_SHOWERS = [
    {
        "name": "Perseids ☄️",
        "peak_date": "August 12 - 13",
        "activity_period": "July 17 - August 24",
        "zhr_hourly_rate": 100,
        "radiant_constellation": "Perseus",
        "parent_body": "Comet 109P/Swift-Tuttle",
        "viewing_conditions": "Excellent summer night skies. High speed meteors leaving persistent glowing ionization trains."
    },
    {
        "name": "Geminids ☄️",
        "peak_date": "December 13 - 14",
        "activity_period": "December 4 - 17",
        "zhr_hourly_rate": 150,
        "radiant_constellation": "Gemini",
        "parent_body": "Asteroid 3200 Phaethon",
        "viewing_conditions": "The king of annual meteor showers. Bright, multi-colored (yellow/green) slow-moving fireballs."
    },
    {
        "name": "Quadrantids ☄️",
        "peak_date": "January 3 - 4",
        "activity_period": "December 28 - January 12",
        "zhr_hourly_rate": 120,
        "radiant_constellation": "Boötes",
        "parent_body": "Asteroid 2003 EH1",
        "viewing_conditions": "Intense short peak of ~6 hours. Best viewed from northern latitudes after midnight."
    },
    {
        "name": "Eta Aquariids ☄️",
        "peak_date": "May 5 - 6",
        "activity_period": "April 19 - May 28",
        "zhr_hourly_rate": 50,
        "radiant_constellation": "Aquarius",
        "parent_body": "Halley's Comet (1P/Halley)",
        "viewing_conditions": "Fast meteors produced by debris shed from famous Halley's Comet. Favors low latitudes."
    },
    {
        "name": "Orionids ☄️",
        "peak_date": "October 21 - 22",
        "activity_period": "October 2 - November 7",
        "zhr_hourly_rate": 25,
        "radiant_constellation": "Orion",
        "parent_body": "Halley's Comet (1P/Halley)",
        "viewing_conditions": "Fast meteors with long ionization trails radiating from the celestial hunter constellation Orion."
    },
    {
        "name": "Lyrids ☄️",
        "peak_date": "April 22 - 23",
        "activity_period": "April 16 - 25",
        "zhr_hourly_rate": 18,
        "radiant_constellation": "Lyra",
        "parent_body": "Comet C/1861 G1 Thatcher",
        "viewing_conditions": "One of the oldest recorded meteor showers (tracked for 2,700 years). Occasionally produces bright fireballs."
    }
]

ECLIPSES_CALENDAR = [
    {
        "date": "2026-08-12",
        "type": "Total Solar Eclipse 🌑☀️",
        "duration_totality": "2m 18s",
        "path_regions": "Greenland, Iceland, Spain (Majorca, Madrid), Western Mediterranean, Morocco / North Africa (Deep Partial)",
        "significance": "First total solar eclipse in mainland Europe since 1999. Spectacular totality sunset across Spain."
    },
    {
        "date": "2027-08-02",
        "type": "Total Solar Eclipse (Great North African Eclipse) 🌑☀️",
        "duration_totality": "6m 23s",
        "path_regions": "Morocco (Tangier), Spain, Algeria, Tunisia, Libya, Egypt (Luxor 6m23s), Saudi Arabia (Jeddah/Makkah), Yemen, Somalia",
        "significance": "The 'Eclipse of the Century' with extraordinary 6+ minutes of totality under cloudless desert skies."
    },
    {
        "date": "2028-07-22",
        "type": "Total Solar Eclipse 🌑☀️",
        "duration_totality": "5m 10s",
        "path_regions": "Australia (Sydney Harbour direct crossing), New Zealand",
        "significance": "Iconic total eclipse crossing directly over the Sydney Opera House and Harbour Bridge."
    },
    {
        "date": "2026-03-03",
        "type": "Total Lunar Eclipse (Blood Moon) 🌕🔴",
        "duration_totality": "58 mins",
        "path_regions": "Pacific, Asia, Australia, Americas, Atlantic",
        "significance": "Blood Moon where Earth's atmosphere filters red sunlight onto the lunar surface."
    },
    {
        "date": "2028-12-31",
        "type": "Total Lunar Eclipse (New Year's Blood Moon) 🌕🔴",
        "duration_totality": "1h 11m",
        "path_regions": "Europe, Africa, Asia, Australia",
        "significance": "Rare New Year's Eve Total Blood Moon."
    }
]

class CelestialEventsManager:
    """Manages astronomical event calendars, meteor shower peaks, and eclipses."""

    @staticmethod
    def get_meteor_showers_df() -> pd.DataFrame:
        return pd.DataFrame(METEOR_SHOWERS)

    @staticmethod
    def get_eclipses_df() -> pd.DataFrame:
        return pd.DataFrame(ECLIPSES_CALENDAR)
