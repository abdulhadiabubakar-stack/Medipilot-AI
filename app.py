"""MediPilot AI - Gombe healthcare-agent simulator (simulation only)."""

from datetime import date, datetime, timedelta
from math import asin, cos, radians, sin, sqrt

import streamlit as st

st.set_page_config(page_title="MediPilot AI | Gombe Simulator", page_icon="🩺", layout="wide")
gi ad
LOCATIONS = {
    "Gombe metropolis": (10.2897, 11.1671),
    "Kaltungo": (9.8183, 11.3089),
    "Billiri": (9.8592, 11.2247),
    "Dukku": (10.8238, 11.0174),
}

FACILITIES = [
    {"name": "Federal Teaching Hospital Gombe", "type": "Tertiary hospital", "owner": "Federal", "lga": "Gombe", "address": "Ashaka Road, Gombe", "lat": 10.3020, "lon": 11.1710, "services": ["Emergency", "General medicine", "Surgery", "Paediatrics", "Laboratory"], "emergency": True},
    {"name": "Gombe State Specialist Hospital", "type": "Specialist hospital", "owner": "State", "lga": "Gombe", "address": "Pantami Road, Gombe", "lat": 10.2766, "lon": 11.1667, "services": ["Emergency", "General medicine", "Maternity", "Surgery", "Radiology"], "emergency": True},
    {"name": "Gombe State University Teaching Hospital", "type": "Teaching hospital", "owner": "State", "lga": "Gombe", "address": "Gombe, Gombe State", "lat": 10.2924, "lon": 11.1804, "services": ["General medicine", "Specialist consultation", "Laboratory", "Pharmacy"], "emergency": True},
    {"name": "Kaltungo General Hospital", "type": "General hospital", "owner": "State", "lga": "Kaltungo", "address": "Kaltungo, Gombe State", "lat": 9.8188, "lon": 11.3110, "services": ["Emergency", "General medicine", "Maternity", "Paediatrics"], "emergency": True},
    {"name": "Billiri General Hospital", "type": "General hospital", "owner": "State", "lga": "Billiri", "address": "Billiri, Gombe State", "lat": 9.8598, "lon": 11.2260, "services": ["Emergency", "General medicine", "Maternity", "Laboratory"], "emergency": True},
    {"name": "Dukku General Hospital", "type": "General hospital", "owner": "State", "lga": "Dukku", "address": "Dukku, Gombe State", "lat": 10.8242, "lon": 11.0190, "services": ["Emergency", "General medicine", "Maternity"], "emergency": True},
]

PROVIDERS = [
    {"name": "Dr. Amina Yusuf", "specialty": "General consultation", "facility": "Federal Teaching Hospital Gombe"},
    {"name": "Dr. Ibrahim Musa", "specialty": "Paediatrics", "facility": "Gombe State Specialist Hospital"},
    {"name": "Dr. Maryam Bello", "specialty": "Women’s health", "facility": "Kaltungo General Hospital"},
    {"name": "Dr. Yusuf Abdullahi", "specialty": "General consultation", "facility": "Gombe State University Teaching Hospital"},
]

def distance_km(a, b):
    lat1, lon1 = map(radians, a)
    lat2, lon2 = map(radians, b)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    x = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371 * 2 * asin(sqrt(x))

def log_event(message):
    st.session_state.activity.insert(0, datetime.now().strftime("%d %b %Y, %H:%M") + " — " + message)

def nearby(location_name, emergency_only=False):
    origin = LOCATIONS[location_name]
    output = []
    for facility in FACILITIES:
        if emergency_only and not facility["emergency"]:
            continue
        item = dict(facility)
        item["distance"] = distance_km(origin, (facility["lat"], facility["lon"]))
        item["minutes"] = max(4, round(item["distance"] * 2.3))
        output.append(item)
    return sorted(output, key=lambda item: item["distance"])

if "activity" not in st.session_state:
    st.session_state.activity = ["Simulator ready — no real calls, messages, bookings, or payments will be made."]
if "appointments" not in st.session_state:
    st.session_state.appointments = []
if "reminders" not in st.session_state:
    st.session_state.reminders = []
if "emergency_started" not in st.session_state:
    st.session_state.emergency_started = False

st.title("🩺 MediPilot AI")
st.caption("Gombe healthcare-agent simulator · safe demo mode")

with st.sidebar:
    st.header("Patient simulator")
    patient = st.text_input("Patient name", "Aisha Mohammed")
    location_name = st.selectbox("Simulated current location", list(LOCATIONS))
    location_allowed = st.toggle("Allow location access")
    contact_allowed = st.toggle("Allow emergency-contact alerts")
    st.divider()
    st.info("Simulation only: no real calls, messages, bookings, GPS, or calendar writes.")

if st.session_state.emergency_started:
    st.error("EMERGENCY MODE ACTIVE — call 112 in a real emergency. This simulator cannot place calls.")

tabs = st.tabs(["🚨 Emergency", "🏥 Find care", "📅 Book consultation", "🔔 Calendar", "🧾 Activity"])

with tabs[0]:
    st.subheader("Emergency response simulator")
    symptoms = st.text_area("What is happening?", placeholder="Example: severe chest pain and difficulty breathing")
    flags = ("chest pain", "difficulty breathing", "cannot breathe", "severe bleeding", "unconscious", "seizure", "stroke", "poisoning", "suicide")
    emergency = any(flag in symptoms.lower() for flag in flags)
    if symptoms and emergency:
        st.warning("Possible emergency detected. Do not wait for an AI diagnosis.")
    elif symptoms:
        st.success("No simulator red flag detected. A clinician should still assess serious or worsening symptoms.")
    if st.button("Start emergency response", type="primary", disabled=not symptoms):
        st.session_state.emergency_started = True
        log_event("Emergency response prepared for " + patient)
        st.rerun()
    if st.session_state.emergency_started:
        if not location_allowed:
            st.warning("Enable location access in the sidebar to find the nearest Gombe facility.")
        else:
            nearest = nearby(location_name, True)[0]
            st.metric("Nearest emergency facility", nearest["name"], f"{nearest['distance']:.1f} km · about {nearest['minutes']} min")
            st.write("Address:", nearest["address"])
            st.write("Simulated patient coordinates:", LOCATIONS[location_name])
            c1, c2, c3 = st.columns(3)
            if c1.button("📞 Simulate call to 112"):
                log_event("Simulated call to Nigeria emergency number 112")
                st.success("Simulation complete. No real call was placed.")
            if c2.button("🗺️ Simulate directions"):
                log_event("Simulated directions to " + nearest["name"])
                st.success("Simulation complete. Directions were prepared.")
            if c3.button("📍 Simulate location sharing", disabled=not contact_allowed):
                log_event("Simulated location alert to approved emergency contact")
                st.success("Simulation complete. Location alert was prepared.")

with tabs[1]:
    st.subheader("Find healthcare near the patient")
    service = st.selectbox("Filter by service", ["Any service", "Emergency", "Maternity", "Paediatrics", "Laboratory", "Surgery"])
    if not location_allowed:
        st.info("Enable location access in the sidebar to simulate GPS-based results.")
    else:
        results = nearby(location_name)
        if service != "Any service":
            results = [item for item in results if service in item["services"]]
        for item in results:
            with st.container(border=True):
                left, right = st.columns([3, 1])
                left.markdown("**" + item["name"] + "**  \n" + item["type"] + " · " + item["owner"] + " · " + item["lga"] + "  \n" + item["address"])
                left.caption("Services: " + ", ".join(item["services"]) + " · Gombe simulator directory")
                right.metric("Distance", f"{item['distance']:.1f} km", f"about {item['minutes']} min")
                a, b = right.columns(2)
                if a.button("Call", key="call_" + item["name"]):
                    log_event("Simulated call to " + item["name"])
                    st.toast("Simulated call prepared")
                if b.button("Directions", key="dir_" + item["name"]):
                    log_event("Simulated directions to " + item["name"])
                    st.toast("Simulated directions prepared")

with tabs[2]:
    st.subheader("Book a doctor consultation")
    specialty = st.selectbox("Consultation type", sorted({p["specialty"] for p in PROVIDERS}))
    providers = [p for p in PROVIDERS if p["specialty"] == specialty]
    provider_labels = [p["name"] + " — " + p["facility"] for p in providers]
    selected_label = st.selectbox("Provider", provider_labels)
    provider = providers[provider_labels.index(selected_label)]
    appointment_date = st.date_input("Preferred date", date.today() + timedelta(days=1), min_value=date.today())
    slot = st.selectbox("Available simulator slot", ["09:00", "11:30", "14:00", "16:30"])
    st.info("Simulator availability: " + provider["name"] + " · " + provider["facility"])
    if st.button("Prepare appointment for approval", type="primary"):
        st.session_state.pending = {"patient": patient, "provider": provider["name"], "facility": provider["facility"], "date": appointment_date, "time": slot}
        log_event("Appointment draft prepared; approval required")
    pending = st.session_state.get("pending")
    if pending:
        st.warning("Confirm simulated booking for " + pending["provider"] + " on " + pending["date"].strftime("%d %b %Y") + " at " + pending["time"] + "?")
        c1, c2 = st.columns(2)
        if c1.button("Approve simulated booking", type="primary"):
            st.session_state.appointments.append(pending)
            st.session_state.pending = None
            log_event("Simulated appointment booked with " + pending["provider"])
            st.success("Appointment booked in the simulator.")
        if c2.button("Cancel draft"):
            st.session_state.pending = None
            log_event("Appointment draft cancelled")
            st.rerun()

with tabs[3]:
    st.subheader("Calendar and reminders")
    if not st.session_state.appointments:
        st.info("No appointments yet. Book one in the consultation tab.")
    for i, appointment in enumerate(st.session_state.appointments):
        with st.container(border=True):
            st.markdown("**" + appointment["provider"] + "** · " + appointment["facility"] + "  \n" + appointment["date"].strftime("%d %b %Y") + " at " + appointment["time"])
            c1, c2 = st.columns(2)
            if c1.button("Add to simulated calendar", key="calendar_" + str(i)):
                log_event("Simulated calendar event created for " + appointment["provider"])
                st.success("Calendar event created in the simulator.")
            if c2.button("Set reminder", key="reminder_" + str(i)):
                st.session_state.reminders.append("Reminder: " + appointment["provider"] + " on " + appointment["date"].strftime("%d %b %Y") + " at " + appointment["time"])
                log_event("Simulated appointment reminder scheduled")
                st.success("Reminder scheduled in the simulator.")
    for reminder in st.session_state.reminders:
        st.write("•", reminder)

with tabs[4]:
    st.subheader("Agent activity and audit log")
    st.caption("The production agent can use this event trail for auditability and recovery.")
    for entry in st.session_state.activity:
        st.write("•", entry)
    if st.button("Reset simulator"):
        for key in ["activity", "appointments", "reminders", "emergency_started", "pending"]:
            st.session_state.pop(key, None)
        st.rerun()

st.divider()
st.caption("Prototype only. This simulator does not diagnose, prescribe, call emergency services, contact hospitals, send messages, access real GPS, or book real appointments.")
