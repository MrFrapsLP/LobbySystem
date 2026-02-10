# Kitchen Hustle (Eatventure-ähnliches PC-Spiel)

Ein kleines **PC-Idle-Game in Python/Tkinter**, inspiriert von Eatventure:

- Stelle Team-Mitglieder ein (Koch, Kellner, Barista …)
- Verdiene automatisch Geld pro Sekunde
- Nutze manuelle Service-Boosts
- Kaufe globale Küchen-Upgrades für Multiplikatoren
- Erreiche Ziele über Einkommen und Reputation

## Start

```bash
python3 game.py
```

> Voraussetzung: Python 3 mit Tkinter (auf vielen Systemen bereits enthalten).

## Steuerung

- **Team-Button klicken**: Mitarbeiter auswählen
- **„Einstellen / Leveln“**: ausgewählten Mitarbeiter verbessern
- **„Service-Boost“**: sofort Geld verdienen
- **„Küchen-Upgrade“**: globalen Einkommensmultiplikator erhöhen

Viel Spaß beim Ausbauen deines Restaurant-Imperiums 🚀


## Windows ohne Python: EXE erstellen

Wenn bei dir `python3` nicht gefunden wird, nutze die EXE-Anleitung in:

- `BUILD_EXE_WINDOWS.md`

Dort ist beschrieben, wie du über GitHub Actions eine fertige `KitchenHustle.exe` bauen und herunterladen kannst.

Wenn in GitHub unter **Actions** nichts angezeigt wird, nutze den Abschnitt **„Wenn bei Actions nichts angezeigt wird“** in `BUILD_EXE_WINDOWS.md`.

Wenn dein Startscript anders heißt oder in einem Unterordner liegt, trage den Pfad beim Starten des Workflows im Feld **entry_script** ein (z. B. `src/main.py`).

Hinweis: Falls im gewählten Branch `game.py` fehlt, bricht der Workflow jetzt mit klarer Fehlermeldung ab. Wähle dann den richtigen Branch oder setze `entry_script` korrekt.


Beim Workflow ist **entry_script** standardmäßig auf `game.py` gesetzt. Wenn der Build fehlschlägt, ist meist der falsche Branch gewählt oder der Pfad in `entry_script` stimmt nicht.


Bei automatischen Push-Runs wird automatisch `game.py` verwendet, auch ohne manuelle Eingabe.


Push-Runs ohne `game.py` werden ohne Fehler übersprungen. Starte dann den Workflow manuell auf dem richtigen Branch.
