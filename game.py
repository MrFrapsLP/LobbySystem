import json
import os
import tkinter as tk
from dataclasses import asdict, dataclass


SAVE_FILE = "savegame.json"


@dataclass
class Station:
    name: str
    unlock_cost: float
    base_price: float
    base_prep_time: float
    level: int = 0
    manager: bool = False
    progress: float = 0.0
    active: bool = False

    @property
    def unlocked(self) -> bool:
        return self.level > 0

    @property
    def upgrade_cost(self) -> float:
        if self.level == 0:
            return self.unlock_cost
        return int(self.unlock_cost * (1.55 ** self.level))

    @property
    def dish_price(self) -> float:
        lvl = max(self.level, 1)
        return self.base_price * (1 + (lvl - 1) * 0.35)

    @property
    def prep_time(self) -> float:
        lvl = max(self.level, 1)
        speed = 1 + (lvl - 1) * 0.08
        return max(0.35, self.base_prep_time / speed)


class EatventurePC:
    TICK_MS = 100

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Kitchen Hustle - Eatventure PC")
        self.root.geometry("1080x640")
        self.root.configure(bg="#121212")

        self.money = 25.0
        self.customers = 2
        self.customer_progress = 0.0
        self.reputation = 0
        self.city = 1
        self.total_earned = 0.0
        self.multiplier = 1.0
        self.selected_idx = 0

        self.stations = [
            Station("Limonaden-Stand", 20, 6, 1.8),
            Station("Pommes-Station", 90, 18, 2.5),
            Station("Burger-Grill", 350, 55, 3.1),
            Station("Sushi-Bar", 1300, 160, 3.8),
            Station("Steak-Küche", 4500, 420, 4.5),
        ]

        self._build_ui()
        self._refresh_ui()
        self._tick()

    def _build_ui(self):
        top = tk.Frame(self.root, bg="#1c1c1c", padx=16, pady=10)
        top.pack(fill="x")

        tk.Label(top, text="Kitchen Hustle", bg="#1c1c1c", fg="white", font=("Segoe UI", 22, "bold")).pack(anchor="w")

        self.stats_label = tk.Label(top, text="", bg="#1c1c1c", fg="#e8e8e8", font=("Segoe UI", 11))
        self.stats_label.pack(anchor="w")

        self.flow_label = tk.Label(top, text="", bg="#1c1c1c", fg="#8bd5ff", font=("Segoe UI", 10, "italic"))
        self.flow_label.pack(anchor="w")

        body = tk.Frame(self.root, bg="#121212", padx=16, pady=12)
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg="#181818", padx=12, pady=12)
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(body, bg="#181818", padx=12, pady=12)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(left, text="Stationen", bg="#181818", fg="white", font=("Segoe UI", 16, "bold")).pack(anchor="w")

        self.station_buttons = []
        for i, _ in enumerate(self.stations):
            b = tk.Button(
                left,
                text="",
                command=lambda idx=i: self.select_station(idx),
                anchor="w",
                justify="left",
                relief="flat",
                bg="#2a2a2a",
                fg="#f1f1f1",
                activebackground="#3a3a3a",
                activeforeground="white",
                padx=10,
                pady=8,
                width=58,
            )
            b.pack(fill="x", pady=5)
            self.station_buttons.append(b)

        tk.Label(right, text="Aktionen", bg="#181818", fg="white", font=("Segoe UI", 16, "bold")).pack(anchor="w")

        self.station_details = tk.Label(right, text="", bg="#181818", fg="#dddddd", justify="left", font=("Segoe UI", 11))
        self.station_details.pack(anchor="w", pady=(8, 10))

        self.upgrade_btn = tk.Button(right, text="Station freischalten / leveln", command=self.upgrade_station, bg="#1f6f43", fg="white", relief="flat", padx=10, pady=9)
        self.upgrade_btn.pack(fill="x", pady=4)

        self.manager_btn = tk.Button(right, text="Manager einstellen", command=self.buy_manager, bg="#7e4cb4", fg="white", relief="flat", padx=10, pady=9)
        self.manager_btn.pack(fill="x", pady=4)

        self.boost_btn = tk.Button(right, text="Werbe-Boost (+25$)", command=self.manual_boost, bg="#2d5cff", fg="white", relief="flat", padx=10, pady=9)
        self.boost_btn.pack(fill="x", pady=4)

        self.kitchen_btn = tk.Button(right, text="Globales Upgrade", command=self.global_upgrade, bg="#b15b00", fg="white", relief="flat", padx=10, pady=9)
        self.kitchen_btn.pack(fill="x", pady=4)

        save_row = tk.Frame(right, bg="#181818")
        save_row.pack(fill="x", pady=(8, 2))
        tk.Button(save_row, text="Speichern", command=self.save_game, bg="#225b8a", fg="white", relief="flat").pack(side="left", expand=True, fill="x", padx=(0, 4))
        tk.Button(save_row, text="Laden", command=self.load_game, bg="#225b8a", fg="white", relief="flat").pack(side="left", expand=True, fill="x", padx=(4, 0))

        self.goal_label = tk.Label(right, text="", bg="#181818", fg="#ffd966", justify="left", wraplength=340, font=("Segoe UI", 10, "italic"))
        self.goal_label.pack(anchor="w", pady=(10, 8))

        self.log_box = tk.Text(right, height=10, bg="#101010", fg="#9be89b", relief="flat")
        self.log_box.pack(fill="both", expand=True)
        self._log("Willkommen! Starte mit Limonaden-Stand und baue dein Restaurant aus.")

    def _log(self, txt: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"• {txt}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def select_station(self, idx: int):
        self.selected_idx = idx
        self._refresh_ui()

    def station_income_estimate(self, s: Station) -> float:
        if not s.unlocked:
            return 0.0
        return (s.dish_price / s.prep_time) * self.multiplier

    def total_income_estimate(self) -> float:
        return sum(self.station_income_estimate(s) for s in self.stations)

    def manual_boost(self):
        self.money += 25 * self.multiplier
        self.total_earned += 25 * self.multiplier
        self.reputation += 1
        self._log("Werbung geschaltet: +Sofortumsatz!")
        self._refresh_ui()

    def upgrade_station(self):
        s = self.stations[self.selected_idx]
        c = s.upgrade_cost
        if self.money < c:
            self._log(f"Zu wenig Geld für {s.name} ({c}$ benötigt).")
            return
        self.money -= c
        s.level += 1
        self.reputation += 2
        if s.level == 1:
            self._log(f"{s.name} freigeschaltet!")
        else:
            self._log(f"{s.name} auf Level {s.level} verbessert.")
        self._refresh_ui()

    def buy_manager(self):
        s = self.stations[self.selected_idx]
        if not s.unlocked:
            self._log("Station zuerst freischalten.")
            return
        if s.manager:
            self._log("Manager ist bereits eingestellt.")
            return
        cost = int(140 + s.unlock_cost * 0.9)
        if self.money < cost:
            self._log(f"Manager für {s.name} kostet {cost}$.")
            return
        self.money -= cost
        s.manager = True
        self.reputation += 5
        self._log(f"Manager für {s.name} eingestellt (Auto-Produktion aktiv).")
        self._refresh_ui()

    def global_upgrade(self):
        cost = int(220 * (self.multiplier ** 1.55))
        if self.money < cost:
            self._log(f"Globales Upgrade kostet {cost}$.")
            return
        self.money -= cost
        self.multiplier *= 1.2
        self.reputation += 6
        self._log(f"Globale Effizienz gesteigert! Multiplikator x{self.multiplier:.2f}")
        self._refresh_ui()

    def save_game(self):
        data = {
            "money": self.money,
            "customers": self.customers,
            "customer_progress": self.customer_progress,
            "reputation": self.reputation,
            "city": self.city,
            "total_earned": self.total_earned,
            "multiplier": self.multiplier,
            "selected_idx": self.selected_idx,
            "stations": [asdict(s) for s in self.stations],
        }
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self._log("Spielstand gespeichert.")

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            self._log("Kein Savegame gefunden.")
            return
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.money = data.get("money", self.money)
        self.customers = data.get("customers", self.customers)
        self.customer_progress = data.get("customer_progress", 0.0)
        self.reputation = data.get("reputation", self.reputation)
        self.city = data.get("city", self.city)
        self.total_earned = data.get("total_earned", self.total_earned)
        self.multiplier = data.get("multiplier", self.multiplier)
        self.selected_idx = min(data.get("selected_idx", 0), len(self.stations) - 1)

        stations_data = data.get("stations", [])
        for i, raw in enumerate(stations_data[: len(self.stations)]):
            self.stations[i] = Station(**raw)

        self._log("Spielstand geladen.")
        self._refresh_ui()

    def _update_customers(self, dt: float):
        # Kundenfluss: je höher Reputation, desto schneller neue Kunden
        spawn_rate = 0.7 + self.reputation * 0.004
        self.customer_progress += spawn_rate * dt
        while self.customer_progress >= 1:
            self.customer_progress -= 1
            self.customers = min(40, self.customers + 1)

    def _process_stations(self, dt: float):
        for s in self.stations:
            if not s.unlocked:
                continue
            if not s.active:
                if self.customers > 0 and (s.manager or s == self.stations[self.selected_idx]):
                    self.customers -= 1
                    s.active = True
                    s.progress = 0.0
            else:
                s.progress += dt
                if s.progress >= s.prep_time:
                    payout = s.dish_price * self.multiplier
                    self.money += payout
                    self.total_earned += payout
                    self.reputation += 1
                    s.active = False
                    s.progress = 0.0

    def _check_city_progression(self):
        need = 8000 * self.city
        if self.total_earned >= need:
            self.city += 1
            self.reputation += 20
            self.multiplier *= 1.15
            self._log(f"Neue Stadt erreicht! Willkommen in Stadt {self.city}.")

    def _goal_text(self) -> str:
        city_target = 8000 * self.city
        return (
            f"Ziel: Verdiene insgesamt {city_target:,.0f}$ für Stadt {self.city + 1}.\n"
            f"Tipp: Manager kaufen + Globales Upgrade für starken Auto-Fortschritt."
        )

    def _refresh_ui(self):
        self.stats_label.configure(
            text=(
                f"Geld: {self.money:,.1f}$   |   Reputation: {self.reputation}   |   Stadt: {self.city}   |   Multiplikator: x{self.multiplier:.2f}"
            )
        )
        self.flow_label.configure(text=f"Kunden in Warteschlange: {self.customers}   |   Geschätzte Einnahmen/Sekunde: {self.total_income_estimate():,.2f}$")

        for idx, s in enumerate(self.stations):
            marker = "▶ " if idx == self.selected_idx else "  "
            status = "LOCKED" if not s.unlocked else ("AUTO" if s.manager else "MANUELL")
            progress = f" | Fortschritt: {int((s.progress / max(s.prep_time, 0.01)) * 100)}%" if s.active else ""
            self.station_buttons[idx].configure(
                text=(
                    f"{marker}{s.name} [{status}] | Level {s.level}\n"
                    f"Gericht: {s.dish_price * self.multiplier:,.1f}$ | Zeit: {s.prep_time:,.2f}s | Nächstes Upgrade: {s.upgrade_cost}$"
                    f"{progress}"
                ),
                bg="#334155" if idx == self.selected_idx else "#2a2a2a",
            )

        s = self.stations[self.selected_idx]
        manager_cost = int(140 + s.unlock_cost * 0.9)
        self.station_details.configure(
            text=(
                f"Ausgewählt: {s.name}\n"
                f"Level: {s.level} | Freigeschaltet: {'Ja' if s.unlocked else 'Nein'}\n"
                f"Gericht-Wert: {s.dish_price * self.multiplier:,.1f}$\n"
                f"Zubereitung: {s.prep_time:,.2f}s\n"
                f"Manager: {'Aktiv' if s.manager else f'Nicht aktiv ({manager_cost}$)'}"
            )
        )

        self.goal_label.configure(text=self._goal_text())

    def _tick(self):
        dt = self.TICK_MS / 1000
        self._update_customers(dt)
        self._process_stations(dt)
        self._check_city_progression()
        self._refresh_ui()
        self.root.after(self.TICK_MS, self._tick)


def main():
    root = tk.Tk()
    EatventurePC(root)
    root.mainloop()


if __name__ == "__main__":
    main()
