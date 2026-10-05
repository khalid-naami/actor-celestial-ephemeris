# Apify Actor: Celestial Ephemeris, Lunar Cycles & ISS Radar 🪐🔭

A high-precision computational astronomy Actor delivering real-time Moon phase cycles, 7-planet orbital ephemeris, solar dawn/dusk twilight timings, eclipses, meteor shower peak schedules, and live International Space Station (ISS) orbital passes.

---

## 🌟 Key Features

1. **Precision Lunar Mechanics**: Julian Date based algorithms calculating Moon phase name, synodic age (0-29.53 days), illumination %, Earth-Moon distance (km), light travel time, and Supermoon/Micromoon perigee detection.
2. **Solar Ephemeris & Twilights**: Exact sunrise, solar noon, sunset, day length, Civil, Nautical, and Astronomical twilight thresholds, plus Golden Hour and Blue Hour windows.
3. **7-Planet Ephemeris**: Real-time celestial mechanics for Mercury, Venus, Mars, Jupiter, Saturn, Uranus, and Neptune. Computes geocentric distance (AU & million km), light travel time (mins), apparent magnitude ($V_0$), altitude, azimuth, and naked-eye vs. telescope visibility status.
4. **Live ISS Orbital Tracker**: Live latitude, longitude, altitude (~420 km), velocity (~27,600 km/h), and instant observer overhead pass detection (<2200 km horizon footprint).
5. **Eclipses & Meteor Showers Calendar**: Verified schedules for upcoming Total Solar & Lunar Eclipses (including the Great 2027 North African Eclipse) and major meteor showers (Perseids, Geminids, Quadrantids, Orionids).

---

## 📥 Input Schema

| Field | Type | Default | Description |
|---|---|---|---|
| `latitude` | Float | `33.5731` | Observer latitude (-90 to +90). |
| `longitude` | Float | `-7.5898` | Observer longitude (-180 to +180). |
| `timezoneOffsetHours` | Float | `1.0` | Local timezone offset from UTC. |
| `targetDate` | String | `""` | Optional target date (`YYYY-MM-DD`). Defaults to current date. |
| `includeMoonPhase` | Boolean | `true` | Compute Moon phase, illumination, and next full moon. |
| `includeSolarTwilights` | Boolean | `true` | Compute solar ephemeris and dawn/dusk twilights. |
| `includePlanets` | Boolean | `true` | Calculate orbital mechanics for all 7 major planets. |
| `includeIssTracker` | Boolean | `true` | Query live ISS orbital coordinates and overhead check. |
| `includeEclipsesAndMeteors` | Boolean | `true` | Include upcoming eclipse paths and meteor shower peaks. |

---

## 📤 Output Dataset Format

Outputs structured objects for each enabled astronomical module:
```json
{
  "record_type": "lunar_phase",
  "calculation_date": "2026-10-03",
  "data": {
    "phase_name": "Waxing Gibbous 🌔",
    "illumination_pct": 82.4,
    "distance_km": 379200,
    "light_travel_time_sec": 1.26,
    "days_to_full_moon": 2.8,
    "next_full_moon_date": "2026-10-06"
  }
}
```

---

## 🚀 How to Run Locally

```bash
cd actor-celestial-ephemeris
pip install -r requirements.txt
python -m src.main
```
