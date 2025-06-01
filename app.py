import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

shift_times = {
    "A": "0730 - 1630",
    "D": "0900 - 1800",
    "C": "1000 - 1900",
    "E": "1100 - 2000",
    "B": "1330 - 2230",
}

custom_order = ["Khyan", "Agnes", "Wayne", "Angel", "Yvonne", "Chyna", "Andy", "Xavier", "Gary", "Daniel", "Peggy"]

def custom_sort(names):
    order_map = {name: i for i, name in enumerate(custom_order)}
    return sorted(names, key=lambda x: (order_map.get(x, len(custom_order)), x))

st.title("📅 Clubhouse Schedule Viewer")
uploaded_file = st.file_uploader("📂 Upload your schedule Excel file (.xlsx)", type=["xlsx"])
selected_date = st.date_input("📅 Select a date to view schedule", datetime.today())

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        df = df.set_index("Name")

        days_to_check = [selected_date]
        if selected_date.weekday() == 3:
            days_to_check = [selected_date + timedelta(days=i) for i in range(4)]

        for date_obj in days_to_check:
            target_day = date_obj.day
            weekday_str = date_obj.strftime("%a")

            if target_day not in df.columns:
                st.warning(f"Day {target_day} not found in schedule.")
                continue

            output = [f"*{target_day}/{date_obj.month}/{date_obj.year} ({weekday_str}) 會所人手*"]
            assigned = {shift: [] for shift in shift_times}
            off_list = []

            for name, shift in df[target_day].items():
                if pd.isna(shift):
                    if "(PT)" not in name:
                        off_list.append(name)
                else:
                    shift_str = str(shift).strip().upper()
                    if shift_str in shift_times:
                        assigned[shift_str].append(name)
                    elif shift_str == "OFF":
                        if "(PT)" not in name:
                            off_list.append(name)
                    else:
                        if "(PT)" not in name:
                            off_list.append(name)

            for shift in ["A", "D", "C", "E", "B"]:
                if assigned[shift]:
                    names = ", ".join(custom_sort(assigned[shift]))
                    output.append(f"{shift}({shift_times[shift]}) : {names}")

            if off_list:
                output.append(f"\nOff: {', '.join(custom_sort(off_list))}")

            st.text_area(f"📋 Schedule for {target_day}/{date_obj.month} ({weekday_str})", "\n".join(output), height=250)

    except Exception as e:
        st.error(f"❌ Error: {e}")
