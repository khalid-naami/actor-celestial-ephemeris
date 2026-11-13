"""Apify Actor Entrypoint: Celestial Ephemeris, Lunar Cycles & Orbital Mechanics."""

import asyncio
import datetime
import math
import os
from typing import Any, Dict
from apify import Actor
from src.astronomy_engine import AstronomyEngine
from src.iss_tracker_client import ISSTrackerClient
from src.celestial_events_data import METEOR_SHOWERS, ECLIPSES_CALENDAR


def sanitize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively strips None, NaN, and Infinity values for clean JSON schema validation."""
    cleaned: Dict[str, Any] = {}
    for k, v in record.items():
        if v is None:
            continue
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            continue
        if isinstance(v, dict):
            cleaned[k] = sanitize_record(v)
        elif isinstance(v, list):
            cleaned_list = []
            for item in v:
                if isinstance(item, dict):
                    cleaned_list.append(sanitize_record(item))
                elif item is not None and not (isinstance(item, float) and (math.isnan(item) or math.isinf(item))):
                    cleaned_list.append(item)
            cleaned[k] = cleaned_list
        else:
            cleaned[k] = v
    return cleaned


def utc_now_naive() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        lat = float(actor_input.get("latitude", 33.5731))
        lon = float(actor_input.get("longitude", -7.5898))
        tz_offset = float(actor_input.get("timezoneOffsetHours", 1.0))
        target_date_str = str(actor_input.get("targetDate", "")).strip()
        api_key = actor_input.get("apiKey") or os.getenv("APIFY_TOKEN") or os.getenv("API_KEY", "")

        include_moon = bool(actor_input.get("includeMoonPhase", True))
        include_sun = bool(actor_input.get("includeSolarTwilights", True))
        include_planets = bool(actor_input.get("includePlanets", True))
        include_iss = bool(actor_input.get("includeIssTracker", True))
        include_events = bool(actor_input.get("includeEclipsesAndMeteors", True))

        if api_key:
            Actor.log.info("API Key / Token authentication provided.")

        if target_date_str:
            try:
                calc_date = datetime.datetime.strptime(target_date_str, "%Y-%m-%d").date()
                calc_dt = datetime.datetime.combine(calc_date, datetime.time(20, 0, 0))
            except Exception:
                calc_dt = utc_now_naive()
                calc_date = calc_dt.date()
        else:
            calc_dt = utc_now_naive()
            calc_date = calc_dt.date()

        Actor.log.info(
            f"Computing Ephemeris for Lat: {lat}, Lon: {lon}, Date: {calc_date.isoformat()}, TZ: UTC{tz_offset:+0.1f}"
        )

        dataset_records = []
        moon_data: Dict[str, Any] = {}
        solar_data: Dict[str, Any] = {}
        planets_data = []
        iss_telemetry: Dict[str, Any] = {}
        observer_coords = {"latitude": lat, "longitude": lon}

        # 1. Lunar Phase & Illumination
        if include_moon:
            moon_data = AstronomyEngine.calculate_moon_phase(calc_dt)
            dataset_records.append(sanitize_record({
                "record_type": "lunar_phase",
                "calculation_date": calc_date.isoformat(),
                "observer_coordinates": observer_coords,
                "data": moon_data,
            }))
            Actor.log.info(f"Calculated Moon Phase: {moon_data.get('phase_name')} ({moon_data.get('illumination_pct')}%)")

        # 2. Solar Ephemeris & Twilights
        if include_sun:
            solar_data = AstronomyEngine.calculate_sun_and_twilight(lat, lon, calc_date, tz_offset)
            dataset_records.append(sanitize_record({
                "record_type": "solar_ephemeris",
                "calculation_date": calc_date.isoformat(),
                "observer_coordinates": observer_coords,
                "data": solar_data,
            }))
            Actor.log.info(f"Calculated Solar Timings: Sunrise {solar_data.get('sunrise')} | Sunset {solar_data.get('sunset')}")

        # 3. 7 Planets Ephemeris
        if include_planets:
            planets_data = AstronomyEngine.calculate_planetary_ephemeris(calc_dt, lat, lon)
            dataset_records.append(sanitize_record({
                "record_type": "planetary_ephemeris",
                "calculation_date": calc_date.isoformat(),
                "observer_coordinates": observer_coords,
                "planets_count": len(planets_data),
                "planets": planets_data,
            }))
            Actor.log.info(f"Calculated orbital mechanics for {len(planets_data)} planets.")

        # 4. Live ISS Tracker
        if include_iss:
            iss_client = ISSTrackerClient()
            iss_telemetry = iss_client.fetch_live_iss_position(lat, lon)
            dataset_records.append(sanitize_record({
                "record_type": "iss_orbital_telemetry",
                "calculation_date": calc_date.isoformat(),
                "timestamp_utc": utc_now_naive().isoformat(),
                "observer_coordinates": observer_coords,
                "data": iss_telemetry,
            }))
            Actor.log.info(
                f"Fetched ISS telemetry: Lat {iss_telemetry.get('latitude')}, Lon {iss_telemetry.get('longitude')}, Overhead: {iss_telemetry.get('is_overhead')}"
            )

        # 5. Eclipses & Meteor Showers
        if include_events:
            dataset_records.append(sanitize_record({
                "record_type": "celestial_events_calendar",
                "calculation_date": calc_date.isoformat(),
                "observer_coordinates": observer_coords,
                "meteor_showers": METEOR_SHOWERS,
                "eclipses_calendar": ECLIPSES_CALENDAR,
            }))
            Actor.log.info(f"Attached {len(METEOR_SHOWERS)} meteor showers & {len(ECLIPSES_CALENDAR)} eclipses.")

        if dataset_records:
            await Actor.push_data(dataset_records)
            Actor.log.info(f"Successfully pushed {len(dataset_records)} ephemeris records to Apify dataset.")

        # Save executive summary in Key-Value store for Apify MCP & instant API tools
        summary_payload = sanitize_record({
            "date": calc_date.isoformat(),
            "observer": observer_coords,
            "moon": {
                "phase": moon_data.get("phase_name"),
                "illuminationPct": moon_data.get("illumination_pct"),
                "distanceKm": moon_data.get("distance_km"),
            },
            "sun": {
                "sunrise": solar_data.get("sunrise"),
                "sunset": solar_data.get("sunset"),
                "dayLength": solar_data.get("day_length_formatted"),
            },
            "visiblePlanetsCount": len([p for p in planets_data if p.get("is_above_horizon")]),
            "issStatus": {
                "overhead": iss_telemetry.get("is_overhead", False),
                "distanceToObserverKm": iss_telemetry.get("distance_to_user_km"),
            },
        })
        await Actor.set_value("OUTPUT", summary_payload)
        if not dataset_records:
            await Actor.fail(status_message="No celestial ephemeris records were produced.")
            return
        Actor.log.info("Stored summary OUTPUT in Key-Value store.")


if __name__ == "__main__":
    asyncio.run(main())
