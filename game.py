import tkinter as tk
from dataclasses import dataclass


@dataclass
class Worker:
    name: str
    base_cost: int
    base_income: float
    level: int = 0

    @property
    def cost(self) -> int:
        return int(self.base_cost * (1.7 ** self.level))

    @property
    def income_per_second(self) -> float:
        # Kleine Skalierung wie in Idle-Games
        return self.level * self.base_income * (1 + self.level * 0.08)


class EatventureLikeGame:
    TICK_MS = 100

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Kitchen Hustle (Eatventure-Style)")
        self.root.geometry("900x560")
        self.root.configure(bg="#121212")

        self.money = 25.0
        self.reputation = 0
        self.multiplier = 1.0

        self.workers = [
            Worker("Koch", 20, 1.1),
            Worker("Kellner", 60, 2.6),
            Worker("Barista", 200, 7.0),
            Worker("Manager", 750, 22.0),
            Worker("Marketing", 2400, 65.0),
        ]

        self.selected_worker = 0
        self._build_ui()
        self._tick()

    def _build_ui(self):
        top = tk.Frame(self.root, bg="#1e1e1e", padx=16, pady=12)
        top.pack(fill="x")

        title = tk.Label(top, text="Kitchen Hustle", fg="#f5f5f5", bg="#1e1e1e", font=("Segoe UI", 22, "bold"))
        title.pack(anchor="w")

        self.money_label = tk.Label(top, text="", fg="#97ff9f", bg="#1e1e1e", font=("Segoe UI", 14, "bold"))
        self.money_label.pack(anchor="w")

        self.ips_label = tk.Label(top, text="", fg="#d0d0d0", bg="#1e1e1e", font=("Segoe UI", 12))
        self.ips_label.pack(anchor="w")

        self.rep_label = tk.Label(top, text="", fg="#ffd966", bg="#1e1e1e", font=("Segoe UI", 11))
        self.rep_label.pack(anchor="w")

        body = tk.Frame(self.root, bg="#121212", padx=16, pady=14)
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg="#181818", padx=12, pady=12)
        left.pack(side="left", fill="both", expand=True)

        right = tk.Frame(body, bg="#181818", padx=12, pady=12)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(left, text="Team", fg="#f0f0f0", bg="#181818", font=("Segoe UI", 16, "bold")).pack(anchor="w")

        self.worker_buttons = []
        for idx, worker in enumerate(self.workers):
            b = tk.Button(
                left,
                text="",
                command=lambda i=idx: self.select_worker(i),
                anchor="w",
                justify="left",
                padx=10,
                pady=8,
                bg="#2a2a2a",
                fg="#efefef",
                activebackground="#333333",
                activeforeground="#ffffff",
                relief="flat",
                width=45,
            )
            b.pack(fill="x", pady=5)
            self.worker_buttons.append(b)

        tk.Label(right, text="Aktionen", fg="#f0f0f0", bg="#181818", font=("Segoe UI", 16, "bold")).pack(anchor="w")

        self.details_label = tk.Label(right, text="", fg="#dcdcdc", bg="#181818", justify="left", font=("Segoe UI", 11))
        self.details_label.pack(anchor="w", pady=(10, 14))

        self.hire_button = tk.Button(right, text="Einstellen / Leveln", command=self.level_selected_worker, bg="#1f6f43", fg="white", relief="flat", padx=12, pady=10)
        self.hire_button.pack(fill="x", pady=4)

        self.tap_button = tk.Button(right, text="Service-Boost (+8$)", command=self.manual_boost, bg="#2d5cff", fg="white", relief="flat", padx=12, pady=10)
        self.tap_button.pack(fill="x", pady=4)

        self.upgrade_button = tk.Button(right, text="Küchen-Upgrade", command=self.buy_global_upgrade, bg="#b15b00", fg="white", relief="flat", padx=12, pady=10)
        self.upgrade_button.pack(fill="x", pady=4)

        self.goal_label = tk.Label(
            right,
            text="Nächstes Ziel: Erreiche 150$ für den ersten Restaurant-Boost!",
            wraplength=320,
            justify="left",
            fg="#ffd966",
            bg="#181818",
            font=("Segoe UI", 10, "italic"),
        )
        self.goal_label.pack(anchor="w", pady=(14, 8))

        self.log_box = tk.Text(right, height=10, bg="#101010", fg="#9be89b", relief="flat")
        self.log_box.pack(fill="both", expand=True)
        self.log_box.insert("end", "Willkommen Chef! Starte mit dem Koch und baue dein Restaurant aus.\n")
        self.log_box.configure(state="disabled")

        self._refresh_ui()

    def log(self, text: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"• {text}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def select_worker(self, index: int):
        self.selected_worker = index
        self._refresh_ui()

    def total_income(self) -> float:
        return sum(w.income_per_second for w in self.workers) * self.multiplier

    def manual_boost(self):
        self.money += 8 * self.multiplier
        self.reputation += 1
        self.log("Service-Boost durchgeführt!")
        self._check_goals()
        self._refresh_ui()

    def level_selected_worker(self):
        worker = self.workers[self.selected_worker]
        cost = worker.cost
        if self.money < cost:
            self.log(f"Nicht genug Geld für {worker.name} (benötigt {cost}$).")
            return
        self.money -= cost
        worker.level += 1
        self.reputation += 2
        self.log(f"{worker.name} auf Level {worker.level} verbessert.")
        self._check_goals()
        self._refresh_ui()

    def buy_global_upgrade(self):
        cost = int(120 * (self.multiplier ** 1.65))
        if self.money < cost:
            self.log(f"Küchen-Upgrade kostet {cost}$.")
            return
        self.money -= cost
        self.multiplier *= 1.22
        self.reputation += 7
        self.log(f"Küchen-Upgrade gekauft! Multiplikator: x{self.multiplier:.2f}")
        self._check_goals()
        self._refresh_ui()

    def _check_goals(self):
        if self.money >= 150 and self.multiplier < 1.2:
            self.goal_label.configure(text="Ziel erreicht! Kaufe ein Küchen-Upgrade und bringe den Multiplikator auf x1.22.")
        elif self.total_income() >= 40:
            self.goal_label.configure(text="Stark! Nächstes Ziel: 100 Reputation für das 'Street Food Empire'.")
        elif self.reputation >= 100:
            self.goal_label.configure(text="Du bist ein Restaurant-Magnet! Spiele weiter für höhere Scores.")

    def _refresh_ui(self):
        self.money_label.configure(text=f"Geld: {self.money:,.1f}$")
        self.ips_label.configure(text=f"Einnahmen/Sekunde: {self.total_income():,.2f}$   |   Multiplikator: x{self.multiplier:.2f}")
        self.rep_label.configure(text=f"Reputation: {self.reputation}")

        for idx, worker in enumerate(self.workers):
            selected = "▶ " if idx == self.selected_worker else "  "
            self.worker_buttons[idx].configure(
                text=(
                    f"{selected}{worker.name} | Level {worker.level}\n"
                    f"Einnahmen: {worker.income_per_second * self.multiplier:,.2f}$/s | Nächstes Upgrade: {worker.cost}$"
                ),
                bg="#334155" if idx == self.selected_worker else "#2a2a2a",
            )

        worker = self.workers[self.selected_worker]
        self.details_label.configure(
            text=(
                f"Ausgewählt: {worker.name}\n"
                f"Aktuelles Level: {worker.level}\n"
                f"Einnahmen pro Sekunde: {worker.income_per_second * self.multiplier:,.2f}$\n"
                f"Nächstes Level kostet: {worker.cost}$"
            )
        )

    def _tick(self):
        self.money += self.total_income() * (self.TICK_MS / 1000)
        self._check_goals()
        self._refresh_ui()
        self.root.after(self.TICK_MS, self._tick)


def main():
    root = tk.Tk()
    EatventureLikeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
