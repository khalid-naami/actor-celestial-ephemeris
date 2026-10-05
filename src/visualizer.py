"""High-Impact Interactive Plotly Visualizations for 3D Solar System, Night Sky Polar Radar & Moon Phases."""

import math
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

PALETTE = {
    "bg": "#0e1117",
    "card_bg": "#1e222b",
    "text": "#e0e6ed",
    "primary": "#38bdf8",     # Sky Blue
    "secondary": "#f59e0b",   # Sun / Gold
    "accent": "#10b981",      # Emerald
    "danger": "#ef4444",      # Mars Red
    "purple": "#a855f7",
    "grid": "#2a303c"
}

def create_3d_solar_system_orrery(planets_list: List[Dict[str, Any]]) -> go.Figure:
    """Create interactive 3D Solar System Orrery with orbits, Sun, and planetary positions."""
    fig = go.Figure()

    # 1. The Sun at Origin
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode="markers+text",
        marker=dict(size=18, color="#f59e0b", line=dict(color="#ffffff", width=2)),
        text=["☀️ The Sun"],
        textposition="top center",
        name="The Sun ☀️",
        hoverinfo="text"
    ))

    # Semi-major axes in AU
    orbit_radii = [0.39, 0.72, 1.0, 1.52, 5.2, 9.58, 19.2, 30.1]
    orbit_names = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    orbit_colors = ["#94a3b8", "#fef08a", "#38bdf8", "#ef4444", "#f59e0b", "#eab308", "#38bdf8", "#6366f1"]

    theta = np.linspace(0, 2 * np.pi, 80)

    # 2. Draw Orbital Ellipses/Circles
    for r, name, col in zip(orbit_radii, orbit_names, orbit_colors):
        # Scale for 3D visualization: logarithmic/cubic root scaling so outer planets fit in scene
        r_scaled = math.pow(r, 0.6) * 4.0
        x_orb = r_scaled * np.cos(theta)
        y_orb = r_scaled * np.sin(theta)
        z_orb = np.zeros_like(theta)

        fig.add_trace(go.Scatter3d(
            x=x_orb, y=y_orb, z=z_orb,
            mode="lines",
            line=dict(color=col, width=1.5, dash="dot"),
            name=f"Orbit: {name}",
            hoverinfo="skip",
            showlegend=False
        ))

    # 3. Draw Planets at Current Positions
    for idx, (p, r, col) in enumerate(zip(planets_list, orbit_radii[0:2] + orbit_radii[3:], orbit_colors[0:2] + orbit_colors[3:])):
        r_scaled = math.pow(r, 0.6) * 4.0
        # Angle based on azimuth
        angle_rad = math.radians(p["azimuth_deg"])
        x_p = r_scaled * math.cos(angle_rad)
        y_p = r_scaled * math.sin(angle_rad)
        z_p = (p["altitude_deg"] / 90.0) * 1.5

        fig.add_trace(go.Scatter3d(
            x=[x_p], y=[y_p], z=[z_p],
            mode="markers+text",
            marker=dict(size=9, color=col, line=dict(color="#ffffff", width=1)),
            text=[f"{p['display_label']}"],
            textposition="top center",
            name=f"{p['planet_name']} ({p['distance_million_km']} M km)",
            hovertext=(
                f"🪐 <b>{p['display_label']}</b><br>"
                f"Constellation: {p['constellation']}<br>"
                f"Distance: <b>{p['distance_million_km']} M km</b> ({p['distance_au']} AU)<br>"
                f"Magnitude: <b>{p['apparent_magnitude']:+.1f}</b><br>"
                f"Status: {p['visibility_badge']}"
            ),
            hoverinfo="text"
        ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=PALETTE["bg"],
        scene=dict(
            xaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            zaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False),
            bgcolor=PALETTE["bg"]
        ),
        title="🌌 Interactive 3D Solar System Orrery & Planetary Orbits",
        height=620,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=10))
    )
    return fig

def create_night_sky_polar_chart(planets_list: List[Dict[str, Any]], moon_data: Dict[str, Any]) -> go.Figure:
    """2D Polar Radar Chart of the Night Sky (Zenith at center, Horizon at outer edge)."""
    fig = go.Figure()

    # Horizon boundary ring (Alt = 0°)
    theta_ring = list(range(0, 361, 10))
    fig.add_trace(go.Scatterpolar(
        r=[90] * len(theta_ring),
        theta=theta_ring,
        mode="lines",
        line=dict(color="#334155", width=2),
        name="Horizon (0° Alt)",
        hoverinfo="skip",
        showlegend=False
    ))

    # Add Moon Position (Simulated Altitude 45°, Azimuth 160°)
    moon_r = 90.0 - 45.0  # Distance from center = 90 - Altitude
    fig.add_trace(go.Scatterpolar(
        r=[moon_r],
        theta=[160.0],
        mode="markers+text",
        marker=dict(size=16, color="#fef08a", symbol="circle"),
        text=[f"🌕 Moon ({moon_data['illumination_pct']}%)"],
        textposition="top center",
        name="Moon 🌕",
        hovertext=f"🌕 <b>{moon_data['phase_name']}</b><br>Illumination: {moon_data['illumination_pct']}%<br>Distance: {moon_data['distance_km']:,} km",
        hoverinfo="text"
    ))

    # Add Planets
    for p in planets_list:
        if p["is_above_horizon"]:
            r_val = 90.0 - max(0.0, p["altitude_deg"])
            fig.add_trace(go.Scatterpolar(
                r=[r_val],
                theta=[p["azimuth_deg"]],
                mode="markers+text",
                marker=dict(size=12, color=p["color"], line=dict(color="#ffffff", width=1.5)),
                text=[f"{p['display_label']}"],
                textposition="top center",
                name=f"{p['planet_name']}",
                hovertext=f"🪐 <b>{p['display_label']}</b><br>Alt: {p['altitude_deg']}° | Az: {p['azimuth_deg']}°<br>Mag: {p['apparent_magnitude']:+.1f}<br>{p['visibility_badge']}",
                hoverinfo="text"
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 90], tickvals=[0, 30, 60, 90], ticktext=["Zenith (90°)", "60°", "30°", "Horizon (0°)"], gridcolor=PALETTE["grid"]),
            angularaxis=dict(direction="clockwise", rotation=90, gridcolor=PALETTE["grid"])
        ),
        template="plotly_dark",
        plot_bgcolor=PALETTE["bg"],
        paper_bgcolor=PALETTE["bg"],
        title="🔭 Local Stargazing Sky Chart (Zenith = 90° overhead, Horizon = 0°)",
        height=540,
        margin=dict(l=40, r=40, t=60, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5)
    )
    return fig

def create_moon_illumination_gauge(illumination_pct: float, phase_name: str) -> go.Figure:
    """Gauge Indicator showing real-time lunar disc illumination %."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=illumination_pct,
        number={'font': {'size': 38, 'color': PALETTE["text"]}, 'suffix': "%"},
        title={'text': f"<b>{phase_name}</b>", 'font': {'size': 16, 'color': PALETTE["primary"]}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': PALETTE["text"], 'ticksuffix': "%"},
            'bar': {'color': "#fef08a", 'thickness': 0.3},
            'steps': [
                {'range': [0, 25], 'color': "#1e293b"},
                {'range': [25, 50], 'color': "#334155"},
                {'range': [50, 75], 'color': "#475569"},
                {'range': [75, 100], 'color': "#64748b"}
            ]
        }
    ))
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor=PALETTE["bg"],
        paper_bgcolor=PALETTE["bg"],
        height=320,
        margin=dict(l=40, r=40, t=70, b=30)
    )
    return fig

def create_planetary_distance_bar(planets_list: List[Dict[str, Any]]) -> go.Figure:
    """Horizontal Bar chart comparing planetary distances from Earth in Million km."""
    fig = go.Figure()
    names = [p["display_label"] for p in planets_list]
    dists = [p["distance_million_km"] for p in planets_list]
    colors = [p["color"] for p in planets_list]

    fig.add_trace(go.Bar(
        y=names,
        x=dists,
        orientation="h",
        marker=dict(color=colors),
        text=[f"{d:,.1f} M km" for d in dists],
        textposition="outside"
    ))

    fig.update_layout(
        title="📏 Real-Time Distance from Earth to Solar System Planets (Million km)",
        template="plotly_dark",
        plot_bgcolor=PALETTE["bg"],
        paper_bgcolor=PALETTE["bg"],
        xaxis=dict(title="Distance (Million Kilometers)", gridcolor=PALETTE["grid"]),
        margin=dict(l=40, r=40, t=60, b=30),
        height=360
    )
    return fig

def create_iss_world_map(iss_data: Dict[str, Any], user_lat: float, user_lon: float, user_city: str) -> go.Figure:
    """Global Map displaying live ISS location, footprint radius, and observer city."""
    fig = go.Figure()

    iss_lat = iss_data["latitude"]
    iss_lon = iss_data["longitude"]

    # 1. ISS Marker
    fig.add_trace(go.Scattergeo(
        lon=[iss_lon],
        lat=[iss_lat],
        mode="markers+text",
        text=["🛰️ ISS (Zarya Module)"],
        textposition="top center",
        name="ISS Space Station 🛰️",
        marker=dict(size=18, color="#38bdf8", symbol="diamond", line=dict(color="#ffffff", width=2)),
        hovertext=(
            f"🛰️ <b>International Space Station</b><br>"
            f"Altitude: <b>{iss_data['altitude_km']} km</b><br>"
            f"Velocity: <b>{iss_data['velocity_kmh']:,} km/h</b> (7.66 km/s)<br>"
            f"Distance to {user_city}: <b>{iss_data['distance_to_user_km']:,} km</b>"
        ),
        hoverinfo="text"
    ))

    # 2. User City Pin
    fig.add_trace(go.Scattergeo(
        lon=[user_lon],
        lat=[user_lat],
        mode="markers+text",
        text=[f"📍 {user_city}"],
        textposition="top center",
        name=f"Observer: {user_city}",
        marker=dict(size=12, color="#10b981", symbol="circle", line=dict(color="#ffffff", width=1.5)),
        hoverinfo="text"
    ))

    fig.update_geos(
        projection_type="natural earth",
        showland=True,
        landcolor="#1a202c",
        showocean=True,
        oceancolor="#0c1017",
        showcountries=True,
        countrycolor="#334155",
        coastlinecolor="#475569",
        bgcolor=PALETTE["bg"]
    )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor=PALETTE["bg"],
        paper_bgcolor=PALETTE["bg"],
        title=f"🛰️ Real-Time ISS Ground Track & Distance ({iss_data['status']})",
        height=580,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )
    return fig
