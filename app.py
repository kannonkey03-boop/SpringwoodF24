

import streamlit as st
import pandas as pd
import math
from pathlib import Path
from supabase import create_client

st.set_page_config(
    page_title="Springwood F24 Race Engineer",
    page_icon="🏁",
    layout="wide",
)


# Secure team login
if "supabase_client" not in st.session_state:
    st.session_state["supabase_client"] = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )

if "authenticated_email" not in st.session_state:
    st.title("🔐 Springwood F24 Team Login")
    st.write("Sign in with your team account to access the race engineering tools.")

    with st.form("team_login_form"):
        email = st.text_input("Team email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", use_container_width=True)

    if submitted:
        try:
            response = st.session_state["supabase_client"].auth.sign_in_with_password(
                {"email": email.strip(), "password": password}
            )
            st.session_state["authenticated_email"] = response.user.email
            st.rerun()
        except Exception:
            st.error("Sign-in failed. Check your email and password, then try again.")

    st.stop()

with st.sidebar:
    st.caption(f"Signed in as {st.session_state['authenticated_email']}")
    if st.button("Log out", use_container_width=True):
        st.session_state["supabase_client"].auth.sign_out()
        del st.session_state["authenticated_email"]
        st.rerun()

st.title("🏁 Springwood F24 Race Engineer")
st.caption("Springwood School | Car #468 | Version 0.2")

st.warning(
    "Race analysis prototype. Lap counts and pace estimates are based "
    "on supplied timing data, not a validated battery model."
)

# Times are in seconds. Dictionary keys are the actual lap numbers.
# None represents a missing timing entry.

heat1 = {
    1:69.964, 2:67.236, 3:70.341, 4:67.116, 5:67.282,
    6:67.297, 7:67.094, 8:67.018, 9:67.695, 10:67.694,
    11:66.975, 12:67.716, 13:67.040, 14:67.206, 15:67.088,
    16:67.701, 17:67.188, 18:67.741, 19:67.711, 20:68.631,
    21:67.007, 22:67.370, 23:67.743, 24:67.153, 25:67.138,
    26:67.636, 27:215.062, 28:68.928, 29:68.706, 30:69.019,
    31:68.863, 32:68.841, 33:68.444, 34:68.431, 35:73.949,
    36:69.286, 37:69.090, 38:71.910, 39:71.851, 40:72.557,
    41:73.533, 42:75.545, 43:78.880, 44:87.298,
    45:101.260, 46:280.400,
}

heat2 = {
    1:70.540, 2:67.150, 3:67.306, 4:67.769, 5:66.344,
    6:66.938, 7:68.227, 8:66.571, 9:66.122, 10:66.571,
    11:66.633, 12:67.128, 13:66.565, 14:66.851, 15:67.206,
    16:71.209, 17:67.377, 18:66.896, 19:66.576, 20:66.496,
    21:67.263, 22:66.773, 23:69.525, 24:67.442, 25:208.612,
    26:67.837, 27:67.507, 28:67.683, 29:68.462, 30:70.144,
    31:68.604, 32:69.452, 33:67.314, 34:68.268, 35:69.072,
    36:69.139, 37:68.698, 38:69.041, 39:70.020, 40:69.565,
    41:69.941, 42:69.202, 43:69.664, 44:70.203, 45:69.882,
    46:69.324, 47:70.374, 48:69.679, 49:202.812, 50:70.675,
    51:72.894, 52:71.073, 53:71.066, 54:71.586, 55:71.978,
    56:72.428, 57:72.633, 58:76.676, 59:76.131, 60:79.455,
    61:85.362,
    # Lap 62 had no recorded time.
    63:113.650,
}

# Supplied competitor data.
southwest = {
    1:71.694, 2:69.881, 4:70.535, 5:69.354,
    6:67.672, 7:67.637, 8:67.466, 9:67.672, 10:67.861,
    11:67.359, 12:67.742, 13:66.999, 14:67.178, 15:67.145,
    17:67.121, 18:67.555, 19:67.661, 20:66.569, 21:67.060,
    22:67.381, 23:67.806, 24:66.869, 25:66.810, 26:67.319,
    27:69.314, 28:67.904, 29:67.005, 30:67.903, 31:68.556,
    32:68.697, 33:68.270, 34:67.994, 35:68.310, 36:67.990,
    37:68.249, 38:198.729, 39:67.863, 40:68.966, 41:67.248,
    43:68.999, 44:68.378, 45:68.670, 46:68.508, 47:68.655,
    48:69.368, 49:69.708, 50:69.022, 51:68.907, 52:70.066,
    53:69.437, 54:69.789, 55:69.776, 56:70.856, 57:70.716,
    58:71.181, 59:72.945, 60:71.188, 61:70.009, 62:70.811,
    63:70.302, 64:218.666, 65:70.640, 66:70.952, 67:71.924,
    68:71.754, 69:71.730, 70:72.086, 71:72.656, 72:72.777,
    73:72.953, 74:73.648,
}

long_cane = {
    1:70.523, 2:67.678, 3:71.445, 4:68.000, 5:69.258,
    6:67.953, 7:68.569, 8:68.166, 9:68.125, 10:67.897,
    11:68.149, 12:68.069, 13:69.690, 14:68.096, 15:69.130,
    16:67.758, 17:68.717, 18:69.388, 19:219.923, 20:68.488,
    21:67.565, 22:69.104, 23:68.701, 24:69.122, 25:68.144,
    26:68.746, 27:68.358, 28:68.441, 29:71.419, 30:68.876,
    31:68.252, 32:68.244, 33:69.746, 34:73.842, 35:75.306,
    36:69.640, 37:69.327, 38:299.427, 39:69.704, 40:70.853,
    41:69.667, 42:69.379, 43:69.164, 44:72.197, 45:69.798,
    46:69.956, 47:72.791, 48:73.006, 49:70.766, 50:70.955,
    51:73.882, 53:71.360, 54:71.059, 55:70.939, 56:72.156,
    57:71.744, 58:72.097, 59:72.729, 60:72.221, 61:72.536,
    62:75.013, 63:73.729, 64:73.184, 65:73.856, 66:74.863,
    67:73.974, 68:74.880, 69:78.500, 70:80.099, 71:83.989,
    72:137.467,
}

races = {
    "Springwood — Heat 1": heat1,
    "Springwood — Heat 2": heat2,
    "Southwest Georgia STEM — Heat 1": southwest,
    "Long Cane Middle — Heat 2": long_cane,
}

def race_frame(data):
    return pd.DataFrame([
        {"Lap": lap, "Seconds": seconds}
        for lap, seconds in data.items()
    ]).sort_values("Lap")

def clean_laps(data):
    return [t for t in data.values() if t is not None and t <= 100]

def fmt(seconds):
    return f"{int(seconds // 60)}:{seconds % 60:05.2f}"

page = st.sidebar.radio(
    "Engineering tools",
    [
        "Race dashboard",
        "Historical Races",
        "Pace by segment",
        "Competitor Analysis",
	"Late-Race Analysis",
	"Race Strategy Simulator",
	"Live Lap Logger",
        "Race pace calculator",
        "Export data",
    ],
)


if page == "Race dashboard":
    import time
    import math

    st.title("🏁 Springwood Race Mode")
    st.caption("Car #468")

    columns = ["Race", "Lap", "Seconds", "Pit Stop"]

    try:
        response = (
            st.session_state["supabase_client"]
            .table("race_laps")
            .select("*")
            .execute()
        )
        lap_log = pd.DataFrame(
            [
                {
                    "Race": row["race"],
                    "Lap": row["lap"],
                    "Seconds": row["seconds"],
                    "Pit Stop": row["pit_stop"],
                }
                for row in response.data
            ],
            columns=columns,
        )
    except Exception as exc:
        st.error(f"Could not load shared lap data from Supabase: {exc}")
        st.stop()

    for col in columns:
        if col not in lap_log.columns:
            lap_log[col] = False if col == "Pit Stop" else None

    if "rc_reset_requested" not in st.session_state:
        st.session_state.rc_reset_requested = False

    if "rc_active" not in st.session_state:
        st.session_state.rc_active = False
    if "rc_start_time" not in st.session_state:
        st.session_state.rc_start_time = None
    if "rc_stint_start_time" not in st.session_state:
        st.session_state.rc_stint_start_time = None
    if "rc_stint_elapsed_seconds" not in st.session_state:
        st.session_state.rc_stint_elapsed_seconds = 0
    if "rc_in_pit" not in st.session_state:
        st.session_state.rc_in_pit = False
    if "rc_pit_start_time" not in st.session_state:
        st.session_state.rc_pit_start_time = None
    if "rc_saved_race" not in st.session_state:
        st.session_state.rc_saved_race = "Springwood — Heat 1"
    if "rc_saved_duration" not in st.session_state:
        st.session_state.rc_saved_duration = 90
    if "rc_saved_target" not in st.session_state:
        st.session_state.rc_saved_target = 74
    if "rc_saved_stops" not in st.session_state:
        st.session_state.rc_saved_stops = 2

    with st.expander("Race setup", expanded=not st.session_state.rc_active):
        race_name = st.text_input(
            "Race name",
            value=st.session_state.rc_saved_race,
            key="rc_mode_name",
            disabled=st.session_state.rc_active,
        )
        setup1, setup2, setup3 = st.columns(3)

        with setup1:
            duration = st.number_input(
                "Race minutes", 10, 180,
                value=st.session_state.rc_saved_duration,
                step=5, disabled=st.session_state.rc_active,
                key="rc_mode_duration",
            )
        with setup2:
            target = st.number_input(
                "Lap target", 1, 200,
                value=st.session_state.rc_saved_target,
                disabled=st.session_state.rc_active,
                key="rc_mode_target",
            )
        with setup3:
            planned_stops = st.number_input(
                "Driver-change stops", 0, 6,
                value=st.session_state.rc_saved_stops,
                disabled=st.session_state.rc_active,
                key="rc_mode_stops",
            )

        if not st.session_state.rc_active:
            if st.button("▶ START RACE", type="primary", use_container_width=True):
                st.session_state.rc_saved_race = race_name.strip() or "Springwood Race"
                st.session_state.rc_saved_duration = int(duration)
                st.session_state.rc_saved_target = int(target)
                st.session_state.rc_saved_stops = int(planned_stops)
                st.session_state.rc_start_time = time.time()
                st.session_state.rc_stint_start_time = time.time()
                st.session_state.rc_stint_elapsed_seconds = 0
                st.session_state.rc_in_pit = False
                st.session_state.rc_pit_start_time = None
                st.session_state.rc_active = True
                st.rerun()
        else:
            if st.button("■ END RACE", type="secondary", use_container_width=True):
                from datetime import datetime

                race_to_save = str(st.session_state.rc_saved_race)

                try:
                    client = st.session_state["supabase_client"]
                    existing_response = (
                        client.table("race_history")
                        .select("race,status")
                        .eq("race", race_to_save)
                        .execute()
                    )

                    already_saved = any(
                        row.get("status") == "Completed"
                        for row in existing_response.data
                    )

                    if already_saved:
                        st.warning(
                            "This race name is already in history. "
                            "Use a unique race name for each heat to avoid mixing results."
                        )
                    else:
                        client.table("race_history").insert({
                            "race": race_to_save,
                            "status": "Completed",
                            "duration_minutes": float(
                                st.session_state.rc_saved_duration
                            ),
                            "target_lap_seconds": float(
                                st.session_state.rc_saved_target
                            ),
                            "planned_stops": int(
                                st.session_state.rc_saved_stops
                            ),
                            "finish_time": datetime.now().astimezone().isoformat(),
                        }).execute()
                        st.success("Race saved to shared Historical Races.")

                except Exception as exc:
                    st.error(f"Could not save race history to Supabase: {exc}")

                st.session_state.rc_active = False
                st.session_state.rc_stint_start_time = None
                st.session_state.rc_stint_elapsed_seconds = 0
                st.session_state.rc_in_pit = False
                st.session_state.rc_pit_start_time = None
                st.rerun()

    race_name = st.session_state.rc_saved_race
    duration = st.session_state.rc_saved_duration
    target = st.session_state.rc_saved_target
    planned_stops = st.session_state.rc_saved_stops

    reset_col1, reset_col2 = st.columns([3, 1])
    with reset_col2:
        if st.button("RESET RACE", type="secondary", key="rc_reset_button"):
            st.session_state.rc_active = False
            st.session_state.rc_start_time = None
            st.session_state.rc_stint_start_time = None
            st.session_state.rc_stint_elapsed_seconds = 0
            st.session_state.rc_in_pit = False
            st.session_state.rc_pit_start_time = None
            st.session_state.rc_reset_requested = True
            st.rerun()

    if st.session_state.rc_reset_requested:
        st.warning("Race Mode has been reset. Historical lap-log data has been preserved.")
        st.session_state.rc_reset_requested = False

    if st.session_state.rc_active and st.session_state.rc_start_time:
        @st.fragment(run_every="1s")
        def race_clock():
            now = time.time()
            elapsed = max(0, now - st.session_state.rc_start_time)
            remaining = max(0, duration * 60 - elapsed)
            mins, secs = divmod(int(remaining), 60)
            st.metric("⏱ RACE TIME REMAINING", f"{mins:02d}:{secs:02d}")

            if st.session_state.rc_in_pit:
                pit_elapsed = max(
                    0, now - st.session_state.rc_pit_start_time
                )
                pit_mins, pit_secs = divmod(int(pit_elapsed), 60)
                st.warning(
                    f"IN PIT — {pit_mins:02d}:{pit_secs:02d} "
                    f"elapsed (2:00 target)"
                )
                if pit_elapsed >= 120:
                    st.error("PIT STOP OVER 2 MINUTES")
                if st.button(
                    "▶ DRIVER BACK ON TRACK",
                    type="primary",
                    use_container_width=True,
                    key="rc_driver_back_on_track",
                ):
                    st.session_state.rc_in_pit = False
                    st.session_state.rc_pit_start_time = None
                    st.session_state.rc_stint_elapsed_seconds = 0
                    st.session_state.rc_stint_start_time = time.time()
                    st.rerun()
            else:
                stint_elapsed = st.session_state.rc_stint_elapsed_seconds
                if st.session_state.rc_stint_start_time is not None:
                    stint_elapsed += max(
                        0, now - st.session_state.rc_stint_start_time
                    )

                stint_mins, stint_secs = divmod(int(stint_elapsed), 60)
                st.metric(
                    "🏎️ DRIVER TIME ON TRACK",
                    f"{stint_mins:02d}:{stint_secs:02d}",
                    help="Pauses during pit stops and resets for the next driver.",
                )

                if stint_elapsed >= 45 * 60:
                    st.error("MAXIMUM STINT REACHED — CHANGE DRIVER NOW")
                elif stint_elapsed >= 40 * 60:
                    st.error("URGENT — DRIVER APPROACHING 45-MINUTE LIMIT")
                elif stint_elapsed >= 30 * 60:
                    st.warning("DRIVER CHANGE DUE — 30-MINUTE TARGET")
                elif stint_elapsed >= 25 * 60:
                    st.warning("PREPARE FOR DRIVER CHANGE")

                if st.button(
                    "🛠️ START PIT STOP",
                    use_container_width=True,
                    key="rc_start_pit_stop",
                ):
                    if st.session_state.rc_stint_start_time is not None:
                        st.session_state.rc_stint_elapsed_seconds += max(
                            0,
                            time.time()
                            - st.session_state.rc_stint_start_time,
                        )
                    st.session_state.rc_stint_start_time = None
                    st.session_state.rc_in_pit = True
                    st.session_state.rc_pit_start_time = time.time()
                    st.rerun()

            if remaining <= 0:
                st.warning("RACE TIME EXPIRED")

        race_clock()
    else:
        st.info("Set up your race above, then press START RACE.")

    race_laps = lap_log[lap_log["Race"].astype(str) == race_name].copy()
    race_laps["Seconds"] = pd.to_numeric(race_laps["Seconds"], errors="coerce")
    race_laps["Lap"] = pd.to_numeric(race_laps["Lap"], errors="coerce")
    race_laps = race_laps.dropna(subset=["Seconds", "Lap"]).sort_values("Lap")

    pit_values = race_laps["Pit Stop"].astype(str).str.strip().str.lower()
    pit_mask = pit_values.isin(["true", "1", "yes"])
    clean_laps = race_laps.loc[
        (~pit_mask) & (race_laps["Seconds"] > 0) & (race_laps["Seconds"] <= 100),
        "Seconds",
    ]

    completed = len(race_laps)
    completed_pits = int(pit_mask.sum())
    elapsed_minutes = (
        max(0, time.time() - st.session_state.rc_start_time) / 60
        if st.session_state.rc_active and st.session_state.rc_start_time
        else 0
    )
    time_left = max(0, duration - elapsed_minutes)
    stops_left = max(0, planned_stops - completed_pits)
    driving_left = max(0, time_left - stops_left * 2)

    avg_pace = float(clean_laps.mean()) if len(clean_laps) else None
    recent_pace = (
        float(clean_laps.tail(5).mean()) if len(clean_laps) else None
    )
    laps_to_go = max(0, target - completed)
    target_pace = (
        driving_left * 60 / laps_to_go if laps_to_go > 0 else None
    )
    projected = (
        completed + driving_left * 60 / recent_pace
        if recent_pace and recent_pace > 0 else None
    )

    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("LAPS COMPLETED", completed)
    m2.metric("PROJECTED FINISH", f"{projected:.0f}" if projected is not None else "—")
    m3.metric("TARGET", target)

    if projected is None:
        st.info("Log a clean lap to calculate pace and projected finish.")
    elif projected >= target:
        st.success("ON PACE")
    else:
        st.error("OFF PACE")

    r1, r2 = st.columns(2)
    with r1:
        st.metric(
            "TARGET LAP PACE",
            fmt(target_pace) if target_pace is not None else "—",
        )
    with r2:
        st.metric(
            "RECENT LAP PACE",
            fmt(recent_pace) if recent_pace is not None else "—",
        )

    if completed_pits < planned_stops and planned_stops > 0:
        next_pit = max(
            completed + 1,
            round(target * (completed_pits + 1) / (planned_stops + 1)),
        )
        st.metric(
            "NEXT DRIVER-CHANGE PIT",
            f"Lap {next_pit}",
            delta="DUE NOW" if completed >= next_pit else None,
        )
    else:
        st.metric("NEXT DRIVER-CHANGE PIT", "No stops remaining")

    # Illustrative battery estimate; replace with measured data when available.
    usable_wh = 24 * 36 * 0.70
    assumed_watts = 400
    battery_percent = max(
        0, min(100, 100 * (usable_wh - assumed_watts * elapsed_minutes / 60) / usable_wh)
    )
    st.metric("ESTIMATED BATTERY REMAINING", f"{battery_percent:.0f}%")
    st.caption("Rough estimate only: assumes 24 V, 36 Ah, 70% usable capacity and 400 W average draw.")

    st.divider()
    st.subheader("➕ Log a lap")

    with st.form("rc_simple_lap_form", clear_on_submit=True):
        lap1, lap2 = st.columns(2)
        with lap1:
            lap_minutes = st.number_input(
                "Minutes", min_value=0, max_value=5, value=1, step=1
            )
        with lap2:
            lap_seconds = st.number_input(
                "Seconds", min_value=0.0, max_value=59.99,
                value=8.0, step=0.01, format="%.2f"
            )
        is_pit = st.checkbox("Driver-change / pit-stop lap")
        submitted = st.form_submit_button(
            "LOG LAP", type="primary", use_container_width=True
        )

    if submitted:
        lap_total_seconds = int(lap_minutes) * 60 + float(lap_seconds)
        if lap_total_seconds <= 0:
            st.error("Enter a valid lap time.")
        elif not st.session_state.rc_active:
            st.error("Press START RACE before logging laps.")
        else:
            try:
                st.session_state["supabase_client"].table("race_laps").insert({
                    "race": race_name,
                    "lap": int(completed + 1),
                    "seconds": float(lap_total_seconds),
                    "pit_stop": bool(is_pit),
                }).execute()
                st.success(f"Saved lap {int(completed + 1)} to the shared database.")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not save lap to the shared database: {exc}")

    if not race_laps.empty:
        with st.expander("Recorded laps"):
            display_laps = race_laps.copy()
            display_laps["Time"] = display_laps["Seconds"].apply(fmt)
            st.dataframe(
                display_laps[["Lap", "Time", "Pit Stop"]],
                use_container_width=True,
                hide_index=True,
            )


elif page == "Historical Races":
    st.title("🏁 Historical Races")
    st.caption("Review completed heats without changing their lap records.")

    client = st.session_state["supabase_client"]

    try:
        history_response = (
            client.table("race_history")
            .select("*")
            .execute()
        )
        history_rows = [
            {
                "Race": row["race"],
                "Status": row.get("status"),
                "Duration Minutes": row.get("duration_minutes"),
                "Target Lap Seconds": row.get("target_lap_seconds"),
                "Planned Stops": row.get("planned_stops"),
                "Finish Time": row.get("finish_time"),
            }
            for row in history_response.data
        ]
        history = pd.DataFrame(
            history_rows,
            columns=[
                "Race", "Status", "Duration Minutes",
                "Target Lap Seconds", "Planned Stops", "Finish Time"
            ],
        )
    except Exception as exc:
        st.error(f"Could not load shared race history: {exc}")
        st.stop()

    completed_history = history[
        history["Status"].astype(str).str.lower() == "completed"
    ].copy() if not history.empty else history.copy()

    if completed_history.empty:
        st.info("No completed races saved yet. Finish a race from Race dashboard.")
    else:
        race_options = completed_history["Race"].astype(str).tolist()
        selected_race = st.selectbox("Choose a completed race", race_options)
        st.divider()
        st.subheader("Manage race history")

        confirm_key = "confirm_delete_" + selected_race
        if confirm_key not in st.session_state:
            st.session_state[confirm_key] = False

        if st.button(
            "DELETE SELECTED RACE",
            type="secondary",
            key="delete_selected_race_button",
        ):
            st.session_state[confirm_key] = True

        if st.session_state[confirm_key]:
            st.warning(
                f"Are you sure you want to permanently delete "
                f"{selected_race} and its lap records?"
            )
            confirm_col, cancel_col = st.columns(2)

            with confirm_col:
                if st.button(
                    "YES, DELETE RACE",
                    type="primary",
                    key="confirm_delete_race_button",
                ):
                    try:
                        client.table("race_laps").delete().eq(
                            "race", selected_race
                        ).execute()
                        client.table("race_history").delete().eq(
                            "race", selected_race
                        ).execute()
                        st.session_state[confirm_key] = False
                        st.success(
                            f"{selected_race} and its lap records were deleted."
                        )
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Could not delete the race from Supabase: {exc}")

            with cancel_col:
                if st.button("CANCEL", key="cancel_delete_race_button"):
                    st.session_state[confirm_key] = False
                    st.rerun()

        race_info = completed_history[
            completed_history["Race"].astype(str) == selected_race
        ].iloc[-1]

        st.subheader(selected_race)
        st.caption(f"Finished: {race_info.get('Finish Time', 'Unknown')}")

        try:
            laps_response = (
                client.table("race_laps")
                .select("*")
                .eq("race", selected_race)
                .execute()
            )
            selected_laps = pd.DataFrame(
                [
                    {
                        "Race": row["race"],
                        "Lap": row["lap"],
                        "Seconds": row["seconds"],
                        "Pit Stop": row["pit_stop"],
                    }
                    for row in laps_response.data
                ],
                columns=["Race", "Lap", "Seconds", "Pit Stop"],
            )
        except Exception as exc:
            st.error(f"Could not load this race's shared lap records: {exc}")
            st.stop()

        if selected_laps.empty:
            st.warning("No lap records were found for this race.")
        else:
            selected_laps["Seconds"] = pd.to_numeric(
                selected_laps["Seconds"], errors="coerce"
            )
            selected_laps["Lap"] = pd.to_numeric(
                selected_laps["Lap"], errors="coerce"
            )
            pit_text = selected_laps["Pit Stop"].astype(str).str.lower()
            pit_mask = pit_text.isin(["true", "1", "yes"])
            valid = selected_laps[
                selected_laps["Seconds"].between(1, 100)
            ].copy()

            c1, c2, c3 = st.columns(3)
            c1.metric("LAPS RECORDED", len(valid))
            c2.metric(
                "AVERAGE LAP",
                fmt(valid["Seconds"].mean()) if not valid.empty else "—"
            )
            c3.metric("PIT-STOP LAPS", int(pit_mask.sum()))

            valid["Lap Time"] = valid["Seconds"].apply(
                lambda x: fmt(x) if pd.notna(x) else "—"
            )
            st.dataframe(
                valid[["Lap", "Lap Time", "Pit Stop"]],
                use_container_width=True,
                hide_index=True,
            )
            st.download_button(
                "Download this race's laps",
                data=selected_laps.to_csv(index=False).encode("utf-8"),
                file_name=f"{selected_race.replace(' ', '_')}_laps.csv",
                mime="text/csv",
            )

elif page == "Pace by segment":
    selected = st.sidebar.selectbox(
        "Choose race", list(races.keys()), index=1
    )
    data = races[selected]
    df = race_frame(data)
    df = df[df["Seconds"] <= 100].copy()
    df["Segment"] = ((df["Lap"] - 1) // 15 + 1) * 15
    df["Segment"] = df["Segment"].apply(
        lambda end: f"Laps {end-14}–{end}"
    )

    summary = df.groupby("Segment", sort=False).agg(
        Clean_laps=("Seconds", "count"),
        Median_seconds=("Seconds", "median"),
        Mean_seconds=("Seconds", "mean"),
    ).reset_index()

    summary = summary.rename(columns={
        "Clean_laps": "Clean laps recorded",
        "Median_seconds": "Median lap (sec)",
        "Mean_seconds": "Mean lap (sec)",
    })

    st.subheader("How pace changes over the race")
    st.write("Median lap time is less affected by one unusually slow lap.")
    st.bar_chart(
        summary.set_index("Segment")["Median lap (sec)"],
        y_label="Median seconds per lap",
    )
    st.dataframe(summary, use_container_width=True, hide_index=True)

    clean = clean_laps(data)
    if len(clean) >= 10:
        first = pd.Series(clean[:15]).median()
        last = pd.Series(clean[-15:]).median()
        st.metric(
            "Last clean-lap group vs first",
            f"{last-first:+.2f} sec per lap",
            help="Compares the first and last up to 15 clean recorded times, "
                 "not necessarily consecutive laps.",
        )


elif page == "Race pace calculator":
    st.subheader("90-minute race strategy")
    st.write(
        "Estimate theoretical lap counts after required driver changes "
        "and other delays."
    )

    duration = st.number_input(
        "Race duration (minutes)",
        min_value=1,
        max_value=240,
        value=90,
    )

    target = st.number_input(
        "Average lap time (seconds)",
        min_value=30.0,
        max_value=300.0,
        value=72.0,
        step=0.5,
    )

    st.markdown("### Required driver-change stops")

    pit_stops = st.number_input(
        "Number of required stops",
        min_value=0,
        max_value=10,
        value=2,
        step=1,
    )

    pit_duration = st.number_input(
        "Minutes per stop (including entry and exit)",
        min_value=0.0,
        max_value=15.0,
        value=1.0,
        step=0.25,
        help="Replace this example with Springwood's measured pit-stop time.",
    )

    extra_delays = st.number_input(
        "Other delays (total minutes)",
        min_value=0.0,
        max_value=60.0,
        value=0.0,
        step=0.5,
    )

    available_seconds = max(
        0,
        duration * 60
        - pit_stops * pit_duration * 60
        - extra_delays * 60,
    )

    estimated_laps = math.floor(available_seconds / target)

    a, b, c = st.columns(3)
    a.metric("Available driving time", f"{available_seconds / 60:.1f} min")
    b.metric("Theoretical laps", estimated_laps)
    c.metric("Time per lap", fmt(target))

    st.caption(
        "This is a simplified estimate. It assumes the entered average lap "
        "time applies throughout driving time and that stop durations are "
        "additional time outside that driving time. Real results depend on "
        "race timing rules, pit entry/exit timing, traffic, changing pace, "
        "and battery performance."
    )

    st.markdown("### Compare race strategies")

    target_laps = st.number_input(
        "Competitor lap-count target",
        min_value=1,
        max_value=150,
        value=74,
        help="Heat 1 comparison: Southwest Georgia STEM completed 74 laps.",
    )

    rows = []

    for pace in [66, 68, 70, 72, 74, 76]:
        possible = math.floor(available_seconds / pace)
        rows.append({
            "Average lap": fmt(pace),
            "Estimated laps": possible,
            "Difference vs target": possible - target_laps,
        })

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True,
    )

    st.info(
        "These are planning estimates, not predictions of battery endurance. "
        "We will improve them using Springwood's measured pit-stop and "
        "on-track test data."
    )


elif page == "Competitor Analysis":
    st.subheader("Competitor Analysis")
    st.write(
        "Compare Springwood's lap times against other teams "
        "by actual lap number."
    )

    heat_choice = st.selectbox(
        "Race to compare",
        ["Heat 1", "Heat 2"],
    )

    if heat_choice == "Heat 1":
        selected_teams = {
            "Springwood #468": heat1,
            "Southwest Georgia STEM #444": southwest,
        }
    else:
        selected_teams = {
            "Springwood #468": heat2,
            "Long Cane Middle #555": long_cane,
        }

    frames = []
    summary = []

    for team, data in selected_teams.items():
        df_team = race_frame(data)
        df_team = df_team[df_team["Seconds"] <= 100].copy()
        df_team["Team"] = team
        frames.append(df_team)

        clean = clean_laps(data)
        summary.append({
            "Team": team,
            "Recorded lap times": len(data),
            "Clean laps (under 100 sec)": len(clean),
            "Fastest clean lap (sec)": min(clean) if clean else None,
            "Median clean lap (sec)": (
                pd.Series(clean).median() if clean else None
            ),
        })

    plot_data = pd.concat(frames).pivot(
        index="Lap",
        columns="Team",
        values="Seconds",
    )

    st.subheader("Lap-by-lap comparison")
    st.line_chart(plot_data)

    st.caption(
        "Only laps of 100 seconds or less are displayed. "
        "Missing laps remain missing. Slower laps are excluded "
        "from this chart but may reflect real race events."
    )

    st.subheader("Team pace summary")
    st.dataframe(
        pd.DataFrame(summary).round(2),
        use_container_width=True,
        hide_index=True,
    )


elif page == "Late-Race Analysis":
    st.subheader("Late-Race Performance Analysis")
    st.write(
        "Measure how lap pace changes throughout the race. "
        "Laps over 100 seconds are excluded from the pace calculations "
        "but remain visible in the raw lap-time chart."
    )

    race_choice = st.selectbox(
        "Select race",
        [
            "Springwood — Heat 1",
            "Springwood — Heat 2",
            "Southwest Georgia STEM — Heat 1",
            "Long Cane Middle — Heat 2",
        ],
    )

    race_data = races[race_choice]

    df = race_frame(race_data).copy()
    df["Clean lap"] = df["Seconds"].le(100)

    st.subheader("1. Lap times across the race")
    st.line_chart(
        df.set_index("Lap")["Seconds"],
        y_label="Lap time (seconds)",
    )

    st.caption(
        "All recorded lap times are shown here. Spikes can reflect "
        "traffic, pit stops, timing anomalies, or other events; "
        "a spike alone does not identify its cause."
    )

    clean = df[df["Clean lap"]].copy()

    if len(clean) < 4:
        st.warning(
            "There are too few clean laps for a useful early-versus-late "
            "comparison."
        )
    else:
        total_laps = int(df["Lap"].max())
        split = total_laps / 2

        early = clean[clean["Lap"] <= split]["Seconds"]
        late = clean[clean["Lap"] > split]["Seconds"]

        if len(early) == 0 or len(late) == 0:
            st.warning(
                "Not enough clean laps in both halves to compare pace."
            )
        else:
            early_median = early.median()
            late_median = late.median()
            change = late_median - early_median
            percent = (change / early_median) * 100

            a, b, c = st.columns(3)
            a.metric(
                "Early-race median",
                fmt(early_median),
            )
            b.metric(
                "Late-race median",
                fmt(late_median),
            )
            c.metric(
                "Late-race pace change",
                f"{change:+.2f} sec/lap",
                delta=f"{percent:+.1f}%",
                delta_color="inverse",
            )

            st.write(
                f"The early half contains {len(early)} clean laps; "
                f"the late half contains {len(late)} clean laps."
            )

            if percent > 3:
                st.warning(
                    "The median clean lap is more than 3% slower in "
                    "the second half. Investigate possible causes; "
                    "this does not prove a battery problem."
                )
            elif percent < -3:
                st.success(
                    "The median clean lap is more than 3% faster "
                    "in the second half."
                )
            else:
                st.info(
                    "The early-versus-late median difference is within "
                    "3%. Review the lap chart and race events for context."
                )

            st.subheader("2. Pace by race segment")

            df["Segment"] = pd.cut(
                df["Lap"],
                bins=[0, 15, 30, 45, 60, float("inf")],
                labels=[
                    "Laps 1–15",
                    "Laps 16–30",
                    "Laps 31–45",
                    "Laps 46–60",
                    "Laps 61+",
                ],
            )

            segment_summary = (
                df[df["Clean lap"]]
                .groupby("Segment", observed=False)["Seconds"]
                .agg(["count", "median", "min"])
                .reset_index()
            )

            segment_summary.columns = [
                "Race segment",
                "Clean laps",
                "Median lap (sec)",
                "Fastest lap (sec)",
            ]

            st.dataframe(
                segment_summary.round(2),
                use_container_width=True,
                hide_index=True,
            )

            st.bar_chart(
                segment_summary.set_index("Race segment")[
                    "Median lap (sec)"
                ],
                y_label="Median lap time (seconds)",
            )

    st.caption(
        "Method: laps of 100 seconds or less are provisionally treated "
        "as clean laps. Early and late halves are based on lap number, "
        "not elapsed time. Missing laps are not imputed. This analysis "
        "describes pace trends but cannot independently diagnose "
        "battery health or driver effects."
    )


elif page == "Race Strategy Simulator":
    st.subheader("Springwood #468 — Race Strategy Simulator")

    mode = st.radio(
        "Choose simulation mode",
        ["Pre-Race Planning", "Live Race Coach"],
        horizontal=True,
    )

    st.caption(
        "Use measured lap times and realistic pit-stop estimates. "
        "Projections assume the entered pace remains representative."
    )

    st.markdown("### Historical race benchmarks")

    benchmark_rows = []

    for heat_name, heat_data in [
        ("Springwood — Heat 1", heat1),
        ("Springwood — Heat 2", heat2),
    ]:
        times = clean_laps(heat_data)

        if times:
            benchmark_rows.append({
                "Race": heat_name,
                "Clean laps": len(times),
                "Average lap": fmt(sum(times) / len(times)),
                "Median lap": fmt(float(pd.Series(times).median())),
                "Fastest lap": fmt(min(times)),
            })

    st.dataframe(
        pd.DataFrame(benchmark_rows),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Clean laps exclude recorded intervals over 100 seconds. "
        "These are historical pace benchmarks, not guaranteed future pace."
    )
    st.markdown("### Pace fade analysis")

    fade_rows = []

    for heat_name, heat_data in [
        ("Springwood — Heat 1", heat1),
        ("Springwood — Heat 2", heat2),
    ]:
        ordered_laps = sorted(heat_data.items())

        clean_entries = [
            (lap, seconds)
            for lap, seconds in ordered_laps
            if seconds is not None and seconds <= 100
        ]

        if len(clean_entries) >= 20:
            first_times = [seconds for _, seconds in clean_entries[:10]]
            last_times = [seconds for _, seconds in clean_entries[-10:]]

            first_avg = sum(first_times) / len(first_times)
            last_avg = sum(last_times) / len(last_times)
            change_pct = (last_avg - first_avg) / first_avg * 100

            fade_rows.append({
                "Race": heat_name,
                "First 10 clean laps": fmt(first_avg),
                "Final 10 clean laps": fmt(last_avg),
                "Pace change": f"{change_pct:+.1f}%",
            })

    if fade_rows:
        st.dataframe(
            pd.DataFrame(fade_rows),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Not enough clean laps to calculate pace fade.")

    if mode == "Pre-Race Planning":
        st.markdown("### Set your race goals")

        duration = st.number_input(
            "Race duration (minutes)",
            min_value=1,
            max_value=240,
            value=90,
        )

        target_laps = st.number_input(
            "Target completed laps",
            min_value=1,
            max_value=150,
            value=74,
        )

        stops = st.number_input(
            "Required driver-change stops",
            min_value=0,
            max_value=10,
            value=2,
        )

        stop_minutes = st.number_input(
            "Estimated minutes per stop",
            min_value=0.0,
            max_value=15.0,
            value=1.0,
            step=0.25,
        )

        total_stop_time = stops * stop_minutes
        driving_seconds = max(0, duration * 60 - total_stop_time * 60)

        required_pace = driving_seconds / target_laps

        a, b = st.columns(2)
        a.metric("Required average lap", fmt(required_pace))
        b.metric("Time reserved for stops", f"{total_stop_time:.1f} min")

        st.markdown("### Compare possible average lap times")

        strategy_rows = []

        historical_paces = [
            sum(clean_laps(heat1)) / len(clean_laps(heat1)),
            sum(clean_laps(heat2)) / len(clean_laps(heat2)),
        ]

        pace_options = sorted(set(
            [66, 68, 70, 72, 74, 76, 78, 80] + historical_paces
        ))

        for pace in pace_options:
            possible_laps = math.floor(driving_seconds / pace)
            strategy_rows.append({
                "Average lap": fmt(pace),
                "Estimated laps": possible_laps,
                "Laps above/below target": possible_laps - target_laps,
            })

        st.dataframe(
            pd.DataFrame(strategy_rows),
            use_container_width=True,
            hide_index=True,
        )

        if required_pace <= 0:
            st.warning("The available driving time is zero.")
        elif required_pace < 60:
            st.warning(
                "This target requires an average lap below 60 seconds. "
                "Check that the target and race inputs are realistic."
            )
        else:
            st.info(
                f"To reach {target_laps} laps, the car must average "
                f"approximately {fmt(required_pace)} while driving, "
                "assuming the entered pit-stop time is additional to "
                "driving time."
            )

    else:
        st.markdown("### Enter the current race situation")

        duration = st.number_input(
            "Total race duration (minutes)",
            min_value=1,
            max_value=240,
            value=90,
            key="live_duration",
        )

        target_laps = st.number_input(
            "Target completed laps",
            min_value=1,
            max_value=150,
            value=74,
            key="live_target",
        )

        elapsed_minutes = st.number_input(
            "Elapsed race time (minutes, including stops)",
            min_value=0.0,
            max_value=240.0,
            value=30.0,
            step=0.5,
        )

        completed_laps = st.number_input(
            "Completed laps",
            min_value=0,
            max_value=150,
            value=25,
        )

        average_lap = st.number_input(
            "Observed average lap time (seconds)",
            min_value=30.0,
            max_value=300.0,
            value=70.0,
            step=0.5,
        )

        latest_lap = st.number_input(
            "Latest lap time (seconds)",
            min_value=30.0,
            max_value=600.0,
            value=70.0,
            step=0.5,
        )

        required_stops = st.number_input(
            "Required driver-change stops",
            min_value=0,
            max_value=10,
            value=2,
            key="live_required_stops",
        )

        completed_stops = st.number_input(
            "Driver-change stops already completed",
            min_value=0,
            max_value=10,
            value=0,
            key="live_completed_stops",
        )

        stop_minutes = st.number_input(
            "Estimated minutes per remaining stop",
            min_value=0.0,
            max_value=15.0,
            value=1.0,
            step=0.25,
            key="live_stop_minutes",
        )

        remaining_minutes = max(0, duration - elapsed_minutes)
        remaining_stops = max(0, required_stops - completed_stops)
        remaining_driving_seconds = max(
            0,
            remaining_minutes * 60 - remaining_stops * stop_minutes * 60,
        )

        laps_needed = max(0, target_laps - completed_laps)

        projected_extra_laps = (
            math.floor(remaining_driving_seconds / average_lap)
            if average_lap > 0 else 0
        )
        projected_total = completed_laps + projected_extra_laps

        required_remaining_pace = (
            remaining_driving_seconds / laps_needed
            if laps_needed > 0 else None
        )

        st.markdown("### Live projections")

        a, b, c = st.columns(3)
        a.metric("Projected finish", f"{projected_total} laps")
        b.metric("Laps needed", laps_needed)
        c.metric("Driving time left", f"{remaining_driving_seconds / 60:.1f} min")

        if required_remaining_pace is not None:
            st.metric(
                "Required average for remaining laps",
                fmt(required_remaining_pace),
            )

            if average_lap <= required_remaining_pace:
                st.success(
                    "Your observed average is currently fast enough "
                    "to meet the target under these assumptions."
                )
            else:
                st.warning(
                    "Your observed average is currently slower than "
                    "the pace required for the target."
                )
        else:
            st.success("The entered lap target has already been reached.")

        if latest_lap > average_lap * 1.05:
            st.warning(
                "The latest lap is more than 5% slower than the entered "
                "average. Check whether this reflects traffic, a stop, "
                "driver variation, or a possible performance issue."
            )

        st.caption(
            "Enter elapsed time including time spent in the pits. "
            "Remaining stop time is subtracted from the remaining race "
            "time. This is a simplified projection, not a guarantee."
        )

    
    st.markdown("### Battery endurance")

    st.caption(
        "Prototype only: battery power consumption has not yet been "
        "measured. Adjust the assumptions to compare possible scenarios."
    )

    battery_voltage = 24
    battery_capacity_ah = 36
    nominal_energy_wh = battery_voltage * battery_capacity_ah

    col1, col2 = st.columns(2)

    with col1:
        race_minutes = st.number_input(
            "Planned race duration (minutes)",
            min_value=1,
            max_value=180,
            value=90,
            step=5,
            key="battery_race_minutes",
        )

    with col2:
        power_draw_w = st.number_input(
            "Assumed average power draw (watts)",
            min_value=50,
            max_value=1500,
            value=400,
            step=50,
            key="battery_power_draw",
            help=(
                "400 W is an illustrative starting assumption, "
                "not a measured value for Springwood #468."
            ),
        )

    usable_percent = st.slider(
        "Assumed usable battery capacity (%)",
        min_value=50,
        max_value=90,
        value=70,
        step=5,
        key="battery_usable_percent",
        help=(
            "Scenario assumption, not a measured battery characteristic. "
            "Actual usable energy depends on load, voltage cutoff, "
            "temperature, and battery condition."
        ),
    )

    usable_energy_wh = nominal_energy_wh * usable_percent / 100
    estimated_runtime_hours = usable_energy_wh / power_draw_w
    estimated_runtime_minutes = estimated_runtime_hours * 60
    estimated_energy_used_wh = power_draw_w * race_minutes / 60
    estimated_energy_remaining_wh = usable_energy_wh - estimated_energy_used_wh

    st.markdown("#### Estimated battery results")

    result1, result2, result3 = st.columns(3)

    result1.metric(
        "Nominal pack energy",
        f"{nominal_energy_wh:.0f} Wh",
    )

    result2.metric(
        "Assumed usable energy",
        f"{usable_energy_wh:.0f} Wh",
    )

    result3.metric(
        "Estimated runtime",
        f"{estimated_runtime_minutes:.0f} min",
    )

    st.metric(
        "Estimated energy remaining after race",
        f"{estimated_energy_remaining_wh:.0f} Wh",
    )

    if estimated_energy_remaining_wh < 0:
        st.warning(
            "Under these assumptions, estimated energy demand exceeds "
            "the assumed usable battery energy. The car may not sustain "
            "this power draw for the full race."
        )
    else:
        st.info(
            "Under these assumptions, estimated energy demand fits "
            "within the assumed usable energy. This does not guarantee "
            "the car will finish: voltage sag, motor load, and other "
            "factors can reduce actual endurance."
        )

    st.caption(
        "Assumes two 12 V, 36 Ah batteries connected in series, giving "
        "a nominal 24 V, 36 Ah pack. Confirm the battery labels and "
        "wiring. The power draw and usable-capacity percentage are "
        "illustrative assumptions, not measured Springwood data."
    )



elif page == "Live Lap Logger":
    st.title("Live Lap Logger")
    st.write("Record driving laps and driver-change pit stops. Records are shared with your team.")

    columns = ["Race", "Lap", "Seconds", "Pit Stop"]

    try:
        response = (
            st.session_state["supabase_client"]
            .table("race_laps")
            .select("*")
            .execute()
        )
        lap_log = pd.DataFrame(
            [
                {
                    "Race": row["race"],
                    "Lap": row["lap"],
                    "Seconds": row["seconds"],
                    "Pit Stop": row["pit_stop"],
                }
                for row in response.data
            ],
            columns=columns,
        )
    except Exception as exc:
        st.error(f"Could not load shared lap data from Supabase: {exc}")
        st.stop()

    if not all(c in lap_log.columns for c in ["Race", "Lap", "Seconds"]):
        st.error("The saved lap file is missing required columns. Please keep a backup before repairing it.")
        st.stop()

    if "Pit Stop" not in lap_log.columns:
        lap_log["Pit Stop"] = False

    lap_log["Pit Stop"] = (
        lap_log["Pit Stop"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "1", "yes"])
    )

    race_name = st.selectbox(
        "Race session",
        [
            "Springwood — Practice",
            "Springwood — Heat 1",
            "Springwood — Heat 2",
        ],
    )

    race_duration = st.number_input(
        "Race duration (minutes)",
        min_value=1,
        max_value=240,
        value=90,
        step=5,
    )
    target_laps = st.number_input(
        "Target laps",
        min_value=1,
        max_value=200,
        value=74,
    )
    required_stops = st.number_input(
        "Required driver-change stops",
        min_value=0,
        max_value=10,
        value=2,
    )
    stop_minutes = st.number_input(
        "Full time budget per remaining stop (minutes)",
        min_value=0.0,
        max_value=15.0,
        value=2.0,
        step=0.25,
        help="Estimate the entire time lost to exiting, changing drivers, securing the new driver, and rejoining. Replace this estimate with measured practice data.",
    )
    elapsed_minutes = st.number_input(
        "Elapsed race time, including stops (minutes)",
        min_value=0.0,
        max_value=float(race_duration),
        value=0.0,
        step=1.0,
    )
    completed_stops = st.number_input(
        "Driver-change stops already completed",
        min_value=0,
        max_value=int(required_stops),
        value=0,
    )

    race_laps = lap_log[lap_log["Race"] == race_name].copy()
    race_laps["Lap"] = pd.to_numeric(race_laps["Lap"], errors="coerce")
    race_laps["Seconds"] = pd.to_numeric(race_laps["Seconds"], errors="coerce")
    race_laps = (
        race_laps.dropna(subset=["Lap", "Seconds"])
        .sort_values("Lap")
    )

    st.subheader("Record a lap")

    with st.form("record_lap_form", clear_on_submit=True):
        next_lap = (
            int(race_laps["Lap"].max()) + 1
            if not race_laps.empty else 1
        )
        lap_number = st.number_input(
            "Lap number",
            min_value=1,
            max_value=200,
            value=next_lap,
            step=1,
        )
        lap_seconds = st.number_input(
            "Full lap interval in seconds",
            min_value=30.0,
            max_value=600.0,
            value=70.0,
            step=0.01,
            format="%.2f",
        )
        pit_stop = st.checkbox(
            "This interval includes a driver-change pit stop",
            value=False,
        )
        save_lap = st.form_submit_button("Save lap")

    if save_lap:
        if (race_laps["Lap"] == lap_number).any():
            st.error("That lap number is already recorded for this race.")
        else:
            try:
                st.session_state["supabase_client"].table("race_laps").insert({
                    "race": race_name,
                    "lap": int(lap_number),
                    "seconds": float(lap_seconds),
                    "pit_stop": bool(pit_stop),
                }).execute()
                st.success(f"Saved lap {int(lap_number)}: {fmt(float(lap_seconds))}")
                st.rerun()
            except Exception as exc:
                st.error(f"Could not save lap to the shared database: {exc}")

    # Separate ordinary driving intervals from pit-stop intervals.
    race_laps = lap_log[lap_log["Race"] == race_name].copy()
    race_laps["Lap"] = pd.to_numeric(race_laps["Lap"], errors="coerce")
    race_laps["Seconds"] = pd.to_numeric(race_laps["Seconds"], errors="coerce")
    race_laps = (
        race_laps.dropna(subset=["Lap", "Seconds"])
        .sort_values("Lap")
    )

    st.subheader("Live pace")

    if race_laps.empty:
        st.info("No laps recorded for this session yet.")
    else:
        clean_laps_df = race_laps[~race_laps["Pit Stop"]].copy()
        completed_laps = int(race_laps["Lap"].max())
        pit_lap_count = int(race_laps["Pit Stop"].sum())

        st.write(
            f"**Completed lap intervals:** {len(race_laps)}  |  "
            f"**Pit-stop intervals marked:** {pit_lap_count}"
        )

        if clean_laps_df.empty:
            st.warning("No ordinary driving laps are available to calculate pace.")
        else:
            times = clean_laps_df["Seconds"].tolist()
            average_pace = sum(times) / len(times)
            fastest_pace = min(times)
            recent_times = times[-5:]
            recent_average = sum(recent_times) / len(recent_times)

            a, b, c = st.columns(3)
            a.metric("Average clean lap", fmt(average_pace))
            b.metric("Fastest clean lap", fmt(fastest_pace))
            c.metric("Recent clean-lap average", fmt(recent_average))

            st.line_chart(
                clean_laps_df.set_index("Lap")["Seconds"],
                y_label="Driving interval (seconds)",
            )

            # Race clock includes completed stops. Only future stops
            # are deducted from the remaining clock.
            remaining_minutes = max(
                0.0, float(race_duration) - float(elapsed_minutes)
            )
            remaining_stops = max(
                0, int(required_stops) - int(completed_stops)
            )
            remaining_driving_seconds = max(
                0.0,
                remaining_minutes * 60
                - remaining_stops * float(stop_minutes) * 60,
            )

            extra_laps = int(remaining_driving_seconds // recent_average)
            projected_total = completed_laps + extra_laps
            laps_needed = max(0, int(target_laps) - completed_laps)

            st.subheader("Race-aware finish projection")

            a, b, c = st.columns(3)
            a.metric("Projected total laps", projected_total)
            b.metric("Target laps", int(target_laps))
            c.metric(
                "Projected laps above/below target",
                projected_total - int(target_laps),
            )

            st.write(
                f"**Remaining race time:** {remaining_minutes:.1f} minutes  \n"
                f"**Remaining stop allowance:** {remaining_stops} stops "
                f"({remaining_stops * float(stop_minutes):.1f} minutes)  \n"
                f"**Estimated driving time remaining:** "
                f"{remaining_driving_seconds / 60:.1f} minutes"
            )

            if laps_needed > 0 and remaining_driving_seconds > 0:
                required_pace = remaining_driving_seconds / laps_needed
                st.write(
                    f"**Driving pace needed to reach target:** "
                    f"{fmt(required_pace)} per lap"
                )
            elif laps_needed == 0:
                st.success("The target lap count has been reached.")
            else:
                st.warning("No driving time remains in this projection.")

            # Compare recent clean pace against the earlier clean pace.
            if len(times) >= 6:
                early_average = sum(times[:5]) / 5
                change_pct = (
                    (recent_average - early_average) / early_average * 100
                )
                if change_pct >= 5:
                    st.warning(
                        f"Recent clean-lap pace is {change_pct:.1f}% slower "
                        "than the first five clean laps. Check driver, "
                        "traffic, and battery data before concluding why."
                    )
                elif change_pct <= -5:
                    st.success(
                        f"Recent clean-lap pace is {abs(change_pct):.1f}% "
                        "faster than the first five clean laps."
                    )

            st.caption(
                "Pit-stop intervals are excluded from driving-pace metrics "
                "but their elapsed time remains part of the race clock. "
                "The projection uses recent clean-lap pace and an estimated "
                "allowance for future stops. It is not a battery-life prediction."
            )

        st.subheader("Recorded laps")
        display_laps = race_laps.copy()
        display_laps["Lap time"] = display_laps["Seconds"].apply(fmt)
        display_laps["Interval type"] = display_laps["Pit Stop"].map(
            {True: "Driver-change stop", False: "Driving"}
        )
        st.dataframe(
            display_laps[["Lap", "Lap time", "Interval type"]],
            use_container_width=True,
            hide_index=True,
        )

        with st.expander("Correct or delete a recorded lap"):
            lap_to_edit = st.selectbox(
                "Choose lap number",
                race_laps["Lap"].astype(int).tolist(),
            )
            selected_record = race_laps[
                race_laps["Lap"] == lap_to_edit
            ].iloc[0]

            corrected_seconds = st.number_input(
                "Correct interval time (seconds)",
                min_value=30.0,
                max_value=600.0,
                value=float(selected_record["Seconds"]),
                step=0.01,
                format="%.2f",
            )
            corrected_pit = st.checkbox(
                "Mark this interval as a driver-change pit stop",
                value=bool(selected_record["Pit Stop"]),
            )

            if st.button("Save correction"):
                try:
                    (
                        st.session_state["supabase_client"]
                        .table("race_laps")
                        .update({
                            "seconds": float(corrected_seconds),
                            "pit_stop": bool(corrected_pit),
                        })
                        .eq("race", str(race_name))
                        .eq("lap", int(lap_to_edit))
                        .execute()
                    )
                    st.success("Correction saved to the shared database.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not save the correction: {exc}")

            if st.button("Delete selected lap"):
                try:
                    (
                        st.session_state["supabase_client"]
                        .table("race_laps")
                        .delete()
                        .eq("race", str(race_name))
                        .eq("lap", int(lap_to_edit))
                        .execute()
                    )
                    st.success("Lap deleted from the shared database.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not delete the lap: {exc}")
elif page == "Export data":
    st.subheader("Export the supplied race data")
    selected = st.selectbox("Choose race", list(races.keys()))
    df = race_frame(races[selected])
    csv = df.to_csv(index=False).encode("utf-8")
    filename = selected.lower().replace(" ", "_").replace("—", "-") + ".csv"

    st.download_button(
        "Download CSV",
        data=csv,
        file_name=filename,
        mime="text/csv",
    )
    st.write("CSV columns: Lap, Seconds")
    st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
st.caption(
    "Springwood F24 Race Engineer | Local prototype | "
    "Verify all source timing data before making engineering decisions."
)