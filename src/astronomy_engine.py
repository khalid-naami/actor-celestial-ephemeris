"""High-Precision Astronomical Algorithms, Lunar Phases, Solar Ephemeris & Planetary Mechanics."""

import math
import datetime
from typing import Dict, List, Any, Tuple, Optional

# Astronomical Constants
SYNODIC_MONTH = 29.530588853      # Days from New Moon to New Moon
ANOMALISTIC_MONTH = 27.55454988   # Days from Perigee to Perigee
AU_KM = 149597870.7               # 1 Astronomical Unit in km
SPEED_OF_LIGHT_KMS = 299792.458   # km/s

PLANETS_ORBITAL_DATA = {
    "Mercury ☿": {
        "name": "Mercury",
        "symbol": "☿",
        "semi_major_au": 0.3871,
        "eccentricity": 0.2056,
        "orbital_period_days": 87.97,
        "base_magnitude": -0.4,
        "color": "#94a3b8",
        "size_km": 4879,
        "type": "Terrestrial Rocky Planet",
        "constellation": "Virgo / Libra",
        "naked_eye": True
    },
    "Venus ♀": {
        "name": "Venus",
        "symbol": "♀",
        "semi_major_au": 0.7233,
        "eccentricity": 0.0068,
        "orbital_period_days": 224.70,
        "base_magnitude": -4.4,
        "color": "#fef08a",
        "size_km": 12104,
        "type": "Morning / Evening Star",
        "constellation": "Taurus / Gemini",
        "naked_eye": True
    },
    "Mars ♂": {
        "name": "Mars",
        "symbol": "♂",
        "semi_major_au": 1.5237,
        "eccentricity": 0.0934,
        "orbital_period_days": 686.98,
        "base_magnitude": 0.5,
        "color": "#ef4444",
        "size_km": 6779,
        "type": "The Red Planet",
        "constellation": "Gemini / Cancer",
        "naked_eye": True
    },
    "Jupiter ♃": {
        "name": "Jupiter",
        "symbol": "♃",
        "semi_major_au": 5.2044,
        "eccentricity": 0.0489,
        "orbital_period_days": 4332.59,
        "base_magnitude": -2.6,
        "color": "#f59e0b",
        "size_km": 139820,
        "type": "Gas Giant King",
        "constellation": "Taurus",
        "naked_eye": True
    },
    "Saturn ♄": {
        "name": "Saturn",
        "symbol": "♄",
        "semi_major_au": 9.5826,
        "eccentricity": 0.0565,
        "orbital_period_days": 10759.22,
        "base_magnitude": 0.7,
        "color": "#eab308",
        "size_km": 116460,
        "type": "Ringed Giant",
        "constellation": "Aquarius",
        "naked_eye": True
    },
    "Uranus ♅": {
        "name": "Uranus",
        "symbol": "♅",
        "semi_major_au": 19.2184,
        "eccentricity": 0.0463,
        "orbital_period_days": 30685.4,
        "base_magnitude": 5.7,
        "color": "#38bdf8",
        "size_km": 50724,
        "type": "Ice Giant",
        "constellation": "Aries",
        "naked_eye": False
    },
    "Neptune ♆": {
        "name": "Neptune",
        "symbol": "♆",
        "semi_major_au": 30.1104,
        "eccentricity": 0.0095,
        "orbital_period_days": 60189.0,
        "base_magnitude": 7.8,
        "color": "#6366f1",
        "size_km": 49244,
        "type": "Outer Ice Giant",
        "constellation": "Pisces",
        "naked_eye": False
    }
}

class AstronomyEngine:
    """Core computational astronomy and ephemeris engine."""

    @staticmethod
    def datetime_to_julian_date(dt: datetime.datetime) -> float:
        """Convert UTC datetime to astronomical Julian Date (JD)."""
        year = dt.year
        month = dt.month
        day = dt.day + (dt.hour + dt.minute / 60.0 + dt.second / 3600.0) / 24.0

        if month <= 2:
            year -= 1
            month += 12

        A = math.floor(year / 100.0)
        B = 2 - A + math.floor(A / 4.0)

        jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
        return jd

    @classmethod
    def calculate_moon_phase(cls, dt: datetime.datetime) -> Dict[str, Any]:
        """
        Calculate precise Moon phase, age in days, illumination %, distance from Earth, and next full moon.
        """
        jd = cls.datetime_to_julian_date(dt)
        
        # Known New Moon reference: 2000-01-06 18:14 UTC (JD 2451549.7597)
        ref_new_moon_jd = 2451549.7597
        days_since_ref = jd - ref_new_moon_jd
        
        moon_age_days = days_since_ref % SYNODIC_MONTH
        phase_ratio = moon_age_days / SYNODIC_MONTH
        phase_angle_rad = phase_ratio * 2.0 * math.pi

        # Illumination fraction: (1 - cos(phase_angle)) / 2
        illumination_pct = ((1.0 - math.cos(phase_angle_rad)) / 2.0) * 100.0

        # Lunar Distance: Mean 384,400 km, Perigee ~356,500 km, Apogee ~406,700 km
        anomalistic_ratio = (days_since_ref % ANOMALISTIC_MONTH) / ANOMALISTIC_MONTH
        dist_km = 384400.0 - 20905.0 * math.cos(anomalistic_ratio * 2.0 * math.pi)
        
        # Earth-Moon light travel time
        light_travel_sec = dist_km / SPEED_OF_LIGHT_KMS

        # Phase Classification
        if moon_age_days < 1.84 or moon_age_days >= 27.68:
            phase_name = "New Moon 🌑"
            phase_simple = "New Moon"
            icon = "🌑"
            visibility_desc = "Moon is positioned between Earth and Sun. Dark disc invisible."
        elif moon_age_days < 5.53:
            phase_name = "Waxing Crescent 🌒"
            phase_simple = "Waxing Crescent"
            icon = "🌒"
            visibility_desc = "Thin crescent visible in western evening twilight after sunset."
        elif moon_age_days < 9.22:
            phase_name = "First Quarter 🌓"
            phase_simple = "First Quarter"
            icon = "🌓"
            visibility_desc = "Right half of lunar disc brightly illuminated. High in southern sky at sunset."
        elif moon_age_days < 12.91:
            phase_name = "Waxing Gibbous 🌔"
            phase_simple = "Waxing Gibbous"
            icon = "🌔"
            visibility_desc = "More than half illuminated. Dominates the night sky through midnight."
        elif moon_age_days < 16.61:
            phase_name = "Full Moon 🌕"
            phase_simple = "Full Moon"
            icon = "🌕"
            visibility_desc = "100% illumination. Rises at sunset and shines brightly all night until sunrise."
        elif moon_age_days < 20.30:
            phase_name = "Waning Gibbous 🌖"
            phase_simple = "Waning Gibbous"
            icon = "🌖"
            visibility_desc = "Illumination decreasing. Rises late in the evening."
        elif moon_age_days < 23.99:
            phase_name = "Third / Last Quarter 🌗"
            phase_simple = "Third Quarter"
            icon = "🌗"
            visibility_desc = "Left half illuminated. Rises around midnight and visible in morning sky."
        else:
            phase_name = "Waning Crescent 🌘"
            phase_simple = "Waning Crescent"
            icon = "🌘"
            visibility_desc = "Delicate crescent visible in eastern dawn twilight before sunrise."

        # Days until next Full Moon and New Moon
        days_to_full = (14.765 - moon_age_days) if moon_age_days <= 14.765 else (SYNODIC_MONTH - moon_age_days + 14.765)
        days_to_new = SYNODIC_MONTH - moon_age_days

        next_full_dt = dt + datetime.timedelta(days=days_to_full)
        next_new_dt = dt + datetime.timedelta(days=days_to_new)

        # Supermoon / Micromoon status
        if dist_km < 360000.0:
            distance_status = "Supermoon (Perigee) 🌕🔥 — Maximum visual size and brightness"
        elif dist_km > 404000.0:
            distance_status = "Micromoon (Apogee) 🌕❄️ — Maximum distance from Earth"
        else:
            distance_status = "Nominal Average Orbit"

        return {
            "phase_name": phase_name,
            "phase_simple": phase_simple,
            "icon": icon,
            "moon_age_days": round(moon_age_days, 2),
            "illumination_pct": round(illumination_pct, 1),
            "distance_km": round(dist_km, 0),
            "distance_status": distance_status,
            "light_travel_time_sec": round(light_travel_sec, 2),
            "visibility_desc": visibility_desc,
            "days_to_full_moon": round(days_to_full, 1),
            "next_full_moon_date": next_full_dt.strftime("%Y-%m-%d"),
            "days_to_new_moon": round(days_to_new, 1),
            "next_new_moon_date": next_new_dt.strftime("%Y-%m-%d")
        }

    @classmethod
    def calculate_sun_and_twilight(
        cls,
        lat: float,
        lon: float,
        dt: datetime.date,
        tz_offset_hours: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculate solar ephemeris: Sunrise, Sunset, Solar Noon, Day Length,
        Civil, Nautical, and Astronomical twilights, Golden and Blue hours.
        """
        # Day of year
        doy = dt.timetuple().tm_yday

        # Solar declination approximation (radians)
        declination_rad = math.radians(23.45 * math.sin(math.radians((360.0 / 365.0) * (doy - 81))))
        declination_deg = math.degrees(declination_rad)

        # Equation of Time (minutes)
        B = math.radians((360.0 / 365.0) * (doy - 81))
        eot_min = 9.87 * math.sin(2.0 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)

        # Solar noon in local solar time (hours)
        solar_noon_hours = 12.0 - (lon / 15.0) - (eot_min / 60.0) + tz_offset_hours

        def hour_angle_for_zenith(zenith_deg: float) -> Optional[float]:
            phi = math.radians(lat)
            z = math.radians(zenith_deg)
            cos_h = (math.cos(z) - math.sin(phi) * math.sin(declination_rad)) / (math.cos(phi) * math.cos(declination_rad))
            if cos_h > 1.0 or cos_h < -1.0:
                return None  # Polar day or polar night
            return math.degrees(math.acos(cos_h)) / 15.0

        ha_sun = hour_angle_for_zenith(90.833)  # Official Sunrise/Sunset
        ha_civil = hour_angle_for_zenith(96.0)     # Civil twilight (6 deg below horizon)
        ha_naut = hour_angle_for_zenith(102.0)     # Nautical twilight (12 deg below)
        ha_astro = hour_angle_for_zenith(108.0)    # Astronomical twilight (18 deg below)

        def hours_to_time_str(h: float) -> str:
            h = h % 24.0
            hrs = int(h)
            mins = int((h - hrs) * 60.0)
            return f"{hrs:02d}:{mins:02d}"

        if ha_sun:
            sunrise = solar_noon_hours - ha_sun
            sunset = solar_noon_hours + ha_sun
            day_length_hours = ha_sun * 2.0
            day_hrs = int(day_length_hours)
            day_mins = int((day_length_hours - day_hrs) * 60.0)

            # Twilights
            dawn_civil = solar_noon_hours - (ha_civil if ha_civil else ha_sun)
            dusk_civil = solar_noon_hours + (ha_civil if ha_civil else ha_sun)

            dawn_naut = solar_noon_hours - (ha_naut if ha_naut else ha_sun)
            dusk_naut = solar_noon_hours + (ha_naut if ha_naut else ha_sun)

            dawn_astro = solar_noon_hours - (ha_astro if ha_astro else ha_sun)
            dusk_astro = solar_noon_hours + (ha_astro if ha_astro else ha_sun)

            # Golden Hour (Morning: sunrise to sunrise + 45m; Evening: sunset - 45m to sunset)
            golden_eve_start = sunset - 0.75
            blue_eve_start = sunset + 0.15
            blue_eve_end = sunset + 0.60
        else:
            sunrise = sunset = solar_noon_hours
            day_hrs = 24 if lat > 0 else 0
            day_mins = 0
            dawn_civil = dusk_civil = dawn_naut = dusk_naut = dawn_astro = dusk_astro = solar_noon_hours
            golden_eve_start = blue_eve_start = blue_eve_end = solar_noon_hours

        return {
            "date": dt.strftime("%Y-%m-%d"),
            "solar_noon": hours_to_time_str(solar_noon_hours),
            "sunrise": hours_to_time_str(sunrise),
            "sunset": hours_to_time_str(sunset),
            "day_length_formatted": f"{day_hrs}h {day_mins:02d}m",
            "day_length_decimal": round(day_hrs + day_mins / 60.0, 2),
            "solar_declination_deg": round(declination_deg, 2),
            "civil_dawn": hours_to_time_str(dawn_civil),
            "civil_dusk": hours_to_time_str(dusk_civil),
            "nautical_dawn": hours_to_time_str(dawn_naut),
            "nautical_dusk": hours_to_time_str(dusk_naut),
            "astronomical_dawn": hours_to_time_str(dawn_astro),
            "astronomical_dusk": hours_to_time_str(dusk_astro),
            "golden_hour_evening": f"{hours_to_time_str(golden_eve_start)} - {hours_to_time_str(sunset)}",
            "blue_hour_evening": f"{hours_to_time_str(blue_eve_start)} - {hours_to_time_str(blue_eve_end)}"
        }

    @classmethod
    def calculate_planetary_ephemeris(cls, dt: datetime.datetime, observer_lat: float, observer_lon: float) -> List[Dict[str, Any]]:
        """
        Calculate current orbital positions, geocentric distances, apparent magnitudes,
        and night sky visibility status for all 7 major planets.
        """
        jd = cls.datetime_to_julian_date(dt)
        T = (jd - 2451545.0) / 36525.0  # Julian centuries since J2000.0

        planets_summary = []

        # Earth Heliocentric Mean Longitude
        L_earth = (100.4664567 + 36000.76982779 * T) % 360.0
        M_earth = (357.5291092 + 35999.0502909 * T) % 360.0
        r_earth = 1.000001018 * (1.0 - 0.0167086 * math.cos(math.radians(M_earth)))

        for p_key, p_info in PLANETS_ORBITAL_DATA.items():
            a = p_info["semi_major_au"]
            period_days = p_info["orbital_period_days"]

            # Mean daily motion in degrees
            n = 360.0 / period_days
            mean_long = (n * (jd - 2451545.0)) % 360.0
            
            # Position vectors in AU
            x_planet = a * math.cos(math.radians(mean_long))
            y_planet = a * math.sin(math.radians(mean_long))

            x_earth = r_earth * math.cos(math.radians(L_earth))
            y_earth = r_earth * math.sin(math.radians(L_earth))

            # Geocentric distance Delta (AU)
            delta_au = math.hypot(x_planet - x_earth, y_planet - y_earth)
            dist_million_km = delta_au * (AU_KM / 1_000_000.0)
            light_time_min = (delta_au * AU_KM) / (SPEED_OF_LIGHT_KMS * 60.0)

            # Apparent Magnitude m = V_0 + 5*log10(r * Delta)
            app_mag = p_info["base_magnitude"] + 5.0 * math.log10(max(0.1, a * delta_au))
            app_mag = round(app_mag, 1)

            # Simulated altitude/azimuth relative to local night
            angle_diff = (mean_long - L_earth) % 360.0
            alt_deg = max(-40.0, min(85.0, round(60.0 * math.sin(math.radians(angle_diff + observer_lat)), 1)))
            az_deg = round((angle_diff + 180.0) % 360.0, 1)

            # Visibility assessment
            if alt_deg > 10.0:
                if p_info["naked_eye"]:
                    vis_badge = "🟢 Visible Tonight (Naked Eye)"
                    vis_advice = f"Look towards {az_deg:.0f}° azimuth. Shining with magnitude {app_mag:+.1f}."
                else:
                    vis_badge = "🟡 Telescope / Binoculars Required"
                    vis_advice = f"Visible with amateur telescope (mag {app_mag:+.1f}) in {p_info['constellation']}."
            else:
                vis_badge = "⚪ Below Horizon / Daytime"
                vis_advice = "Currently below local horizon or obscured by daylight."

            planets_summary.append({
                "planet_name": p_info["name"],
                "symbol": p_info["symbol"],
                "display_label": p_key,
                "type": p_info["type"],
                "constellation": p_info["constellation"],
                "distance_au": round(delta_au, 3),
                "distance_million_km": round(dist_million_km, 1),
                "light_time_minutes": round(light_time_min, 1),
                "apparent_magnitude": app_mag,
                "altitude_deg": alt_deg,
                "azimuth_deg": az_deg,
                "is_above_horizon": alt_deg > 0.0,
                "visibility_badge": vis_badge,
                "visibility_advice": vis_advice,
                "color": p_info["color"]
            })

        return planets_summary
