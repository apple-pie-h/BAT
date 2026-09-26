import customtkinter as ctk
from battery import refresh_battery_data
from PIL import Image, ImageTk


class BatteryApp:
    def __init__(self, battery):
        self.battery = battery
        self.current_page = "dashboard"
        self.refresh_interval = 5000

        self.app = ctk.CTk()
        
        self.app.title("BAT — Battery Analysis Tool")
        self.app.geometry("1000x650")
        self.app.minsize(850, 550)

        icon=Image.open("assets/bat.png")
        icon=ImageTk.PhotoImage(icon)
        self.app.iconphoto(False, icon)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)

        self.percentage_label = None
        self.state_label = None
        self.progress = None
        self.health_value = None
        self.cycles_value = None
        self.detail_value_labels = {}

        self.health_value_page = None
        self.health_progress = None

        self.create_layout()
        self.show_dashboard()

        self.app.after(self.refresh_interval, self.refresh_battery)

    def refresh_battery(self):
        new_battery = refresh_battery_data(self.battery)

        if new_battery is not None:
            self.battery = new_battery

            if self.current_page == "dashboard":
                self.update_dashboard_values()

            elif self.current_page == "health":
                self.update_health_values()

        self.app.after(self.refresh_interval, self.refresh_battery)

    def update_dashboard_values(self):
        percentage = self.battery.percentage

        if percentage is None:
            percentage = 0

        self.percentage_label.configure(
            text=f"{percentage:.0f}%"
        )

        state = self.battery.state or "Unknown"

        self.state_label.configure(
            text=f"State: {state}"
        )

        self.progress.set(percentage / 100)

        health = self.battery.health

        if health is None:
            health_text = "Not available"
        else:
            health_text = f"{health:.1f}%"

        self.health_value.configure(
            text=health_text
        )

        cycles = self.battery.charge_cycles

        if cycles is None:
            cycles_text = "Not available"
        else:
            cycles_text = str(cycles)

        self.cycles_value.configure(
            text=cycles_text
        )

        detail_data = {
            "Current Energy": (self.battery.energy, "Wh"),
            "Full Capacity": (self.battery.energy_full, "Wh"),
            "Design Capacity": (self.battery.energy_full_design, "Wh"),
            "Voltage": (self.battery.voltage, "V"),
            "Power": (self.battery.energy_rate, "W"),
            "Technology": (self.battery.technology, ""),
            "Vendor": (self.battery.vendor, ""),
            "Model": (self.battery.model, "")
        }

        for name, (value, unit) in detail_data.items():
            if value is None:
                value_text = "Not available"
            elif isinstance(value, float):
                value_text = f"{value:.2f}"
            else:
                value_text = str(value)

            if unit and value_text != "Not available":
                value_text = f"{value_text} {unit}"

            self.detail_value_labels[name].configure(
                text=value_text
            )

    def update_health_values(self):
        health = self.battery.health

        if health is None:
            self.health_value_page.configure(
                text="Not available"
            )

            self.health_progress.set(0)

        else:
            self.health_value_page.configure(
                text=f"{health:.1f}%"
            )

            self.health_progress.set(health / 100)

    def create_layout(self):
        self.sidebar = ctk.CTkFrame(
            self.app,
            width=220,
            corner_radius=0
        )
        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        self.sidebar.grid_propagate(False)

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="BAT",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        )
        self.logo_label.pack(
            pady=(30, 5)
        )

        self.subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Battery Analysis Tool",
            font=ctk.CTkFont(size=14)
        )
        self.subtitle.pack(
            pady=(0, 30)
        )

        self.dashboard_button = ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            anchor="w",
            font=ctk.CTkFont(size=16),
            command=self.show_dashboard
        )
        self.dashboard_button.pack(
            padx=15,
            pady=5,
            fill="x"
        )

        self.health_button = ctk.CTkButton(
            self.sidebar,
            text="Battery Health",
            anchor="w",
            font=ctk.CTkFont(size=16),
            command=self.show_health
        )
        self.health_button.pack(
            padx=15,
            pady=5,
            fill="x"
        )

        self.care_button = ctk.CTkButton(
            self.sidebar,
            text="Battery Care",
            anchor="w",
            font=ctk.CTkFont(size=16),
            command=self.show_care
        )
        self.care_button.pack(
            padx=15,
            pady=5,
            fill="x"
        )

        self.about_button = ctk.CTkButton(
            self.sidebar,
            text="About BAT",
            anchor="w",
            font=ctk.CTkFont(size=16),
            command=self.show_about
        )
        self.about_button.pack(
            padx=15,
            pady=5,
            fill="x"
        )

        self.content = ctk.CTkScrollableFrame(
            self.app,
            corner_radius=0
        )
        self.content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=0,
            pady=0
        )

    def set_active_button(self, active):
        buttons = {
            "dashboard": self.dashboard_button,
            "health": self.health_button,
            "care": self.care_button,
            "about": self.about_button
        }

        for name, button in buttons.items():
            if name == active:
                button.configure(
                    fg_color=("#3B8ED0", "#1F6AA5")
                )
            else:
                button.configure(
                    fg_color="transparent"
                )

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        self.percentage_label = None
        self.state_label = None
        self.progress = None
        self.health_value = None
        self.cycles_value = None
        self.detail_value_labels = {}

        self.health_value_page = None
        self.health_progress = None

    def show_dashboard(self):
        self.current_page = "dashboard"
        self.clear_content()
        self.set_active_button("dashboard")

        title = ctk.CTkLabel(
            self.content,
            text="Battery Overview",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        title.pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        subtitle = ctk.CTkLabel(
            self.content,
            text="Current battery status",
            font=ctk.CTkFont(size=16)
        )
        subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        overview = ctk.CTkFrame(
            self.content,
            corner_radius=15
        )
        overview.pack(
            fill="x",
            padx=25,
            pady=10
        )

        percentage = self.battery.percentage

        if percentage is None:
            percentage = 0

        self.percentage_label = ctk.CTkLabel(
            overview,
            text=f"{percentage:.0f}%",
            font=ctk.CTkFont(
                size=50,
                weight="bold"
            )
        )
        self.percentage_label.pack(
            pady=(25, 5)
        )

        state = self.battery.state or "Unknown"

        self.state_label = ctk.CTkLabel(
            overview,
            text=f"State: {state}",
            font=ctk.CTkFont(size=16)
        )
        self.state_label.pack(
            pady=(0, 15)
        )

        self.progress = ctk.CTkProgressBar(
            overview,
            width=400
        )
        self.progress.pack(
            padx=30,
            pady=(0, 25)
        )
        self.progress.set(percentage / 100)

        cards = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        cards.pack(
            fill="x",
            padx=25,
            pady=10
        )

        cards.grid_columnconfigure(
            0,
            weight=1
        )

        cards.grid_columnconfigure(
            1,
            weight=1
        )

        health_card = ctk.CTkFrame(
            cards,
            corner_radius=15
        )
        health_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 7)
        )

        health = self.battery.health

        if health is None:
            health_text = "Not available"
        else:
            health_text = f"{health:.1f}%"

        ctk.CTkLabel(
            health_card,
            text="Battery Health",
            font=ctk.CTkFont(size=17)
        ).pack(
            pady=(20, 5)
        )

        self.health_value = ctk.CTkLabel(
            health_card,
            text=health_text,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        self.health_value.pack(
            pady=(0, 20)
        )

        cycles_card = ctk.CTkFrame(
            cards,
            corner_radius=15
        )
        cycles_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(7, 0)
        )

        cycles = self.battery.charge_cycles

        if cycles is None:
            cycles_text = "Not available"
        else:
            cycles_text = str(cycles)

        ctk.CTkLabel(
            cycles_card,
            text="Charge Cycles",
            font=ctk.CTkFont(size=17)
        ).pack(
            pady=(20, 5)
        )

        self.cycles_value = ctk.CTkLabel(
            cycles_card,
            text=cycles_text,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        self.cycles_value.pack(
            pady=(0, 20)
        )

        details = ctk.CTkFrame(
            self.content,
            corner_radius=15
        )
        details.pack(
            fill="x",
            padx=25,
            pady=10
        )

        ctk.CTkLabel(
            details,
            text="Battery Details",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 15)
        )

        detail_data = [
            ("Current Energy", self.battery.energy, "Wh"),
            ("Full Capacity", self.battery.energy_full, "Wh"),
            ("Design Capacity", self.battery.energy_full_design, "Wh"),
            ("Voltage", self.battery.voltage, "V"),
            ("Power", self.battery.energy_rate, "W"),
            ("Technology", self.battery.technology, ""),
            ("Vendor", self.battery.vendor, ""),
            ("Model", self.battery.model, "")
        ]

        for name, value, unit in detail_data:
            if value is None:
                value_text = "Not available"
            elif isinstance(value, float):
                value_text = f"{value:.2f}"
            else:
                value_text = str(value)

            if unit and value_text != "Not available":
                value_text = f"{value_text} {unit}"

            row = ctk.CTkFrame(
                details,
                fg_color="transparent"
            )
            row.pack(
                fill="x",
                padx=20,
                pady=4
            )

            ctk.CTkLabel(
                row,
                text=name,
                font=ctk.CTkFont(size=15),
                anchor="w"
            ).pack(
                side="left"
            )

            value_label = ctk.CTkLabel(
                row,
                text=value_text,
                font=ctk.CTkFont(size=15),
                anchor="e"
            )
            value_label.pack(
                side="right"
            )

            self.detail_value_labels[name] = value_label

        ctk.CTkLabel(
            details,
            text=""
        ).pack(
            pady=5
        )

    def show_health(self):
        self.current_page = "health"
        self.clear_content()
        self.set_active_button("health")

        title = ctk.CTkLabel(
            self.content,
            text="Battery Health",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        title.pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        subtitle = ctk.CTkLabel(
            self.content,
            text="Battery capacity and aging information",
            font=ctk.CTkFont(size=16)
        )
        subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        card = ctk.CTkFrame(
            self.content,
            corner_radius=15
        )
        card.pack(
            fill="x",
            padx=25,
            pady=10
        )

        health = self.battery.health

        if health is None:
            health_text = "Not available"
        else:
            health_text = f"{health:.1f}%"

        self.health_value_page = ctk.CTkLabel(
            card,
            text=health_text,
            font=ctk.CTkFont(
                size=50,
                weight="bold"
            )
        )
        self.health_value_page.pack(
            pady=(30, 5)
        )

        ctk.CTkLabel(
            card,
            text="Current Battery Capacity",
            font=ctk.CTkFont(size=16)
        ).pack(
            pady=(0, 20)
        )

        self.health_progress = ctk.CTkProgressBar(card)

        self.health_progress.pack(
            fill="x",
            padx=40,
            pady=(0, 30)
        )

        if health is None:
            self.health_progress.set(0)
        else:
            self.health_progress.set(health / 100)

    def show_care(self):
        self.current_page = "care"
        self.clear_content()
        self.set_active_button("care")

        title = ctk.CTkLabel(
            self.content,
            text="Battery Care",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        title.pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        subtitle = ctk.CTkLabel(
            self.content,
            text="Simple practices that can help maintain battery health",
            font=ctk.CTkFont(size=16)
        )
        subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        tips = [
            (
                "Avoid excessive heat",
                "High temperatures can accelerate battery aging."
            ),
            (
                "Avoid unnecessary deep discharges",
                "Frequently draining the battery very low can increase battery stress."
            ),
            (
                "Use the original charger when possible",
                "Use a charger that meets your laptop's required specifications."
            ),
            (
                "Keep your laptop ventilated",
                "Good airflow helps prevent excessive heat during heavy workloads."
            ),
            (
                "Monitor battery health",
                "BAT can help you keep track of capacity and charge cycles over time."
            )
        ]

        for title_text, description in tips:
            card = ctk.CTkFrame(
                self.content,
                corner_radius=15
            )
            card.pack(
                fill="x",
                padx=25,
                pady=7
            )

            ctk.CTkLabel(
                card,
                text=title_text,
                font=ctk.CTkFont(
                    size=18,
                    weight="bold"
                ),
                anchor="w"
            ).pack(
                anchor="w",
                padx=20,
                pady=(15, 5)
            )

            ctk.CTkLabel(
                card,
                text=description,
                font=ctk.CTkFont(size=15),
                anchor="w",
                justify="left",
                wraplength=700
            ).pack(
                anchor="w",
                padx=20,
                pady=(0, 15)
            )

    def show_about(self):
        self.current_page = "about"
        self.clear_content()
        self.set_active_button("about")

        title = ctk.CTkLabel(
            self.content,
            text="About BAT",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        title.pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        card = ctk.CTkFrame(
            self.content,
            corner_radius=15
        )
        card.pack(
            fill="x",
            padx=25,
            pady=20
        )

        ctk.CTkLabel(
            card,
            text="BAT — Battery Analysis Tool",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        ).pack(
            pady=(30, 10)
        )

        ctk.CTkLabel(
            card,
            text=(
                "A simple Linux desktop application for "
                "monitoring and understanding laptop battery information."
            ),
            font=ctk.CTkFont(size=15),
            wraplength=650,
            justify="center"
        ).pack(
            padx=30,
            pady=(0, 30)
        )

    def run(self):
        self.app.mainloop()
