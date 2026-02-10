# Windows EXE ohne lokale Python-Installation

Du hast den Fehler bekommen, dass `python3` nicht gefunden wurde. Das ist normal auf manchen Windows-Systemen.

## Lösung: Fertige `.exe` über GitHub Actions bauen lassen

Du brauchst dafür **kein Python auf deinem PC**.

1. Repo zu GitHub pushen.
2. In GitHub auf den Tab **Actions** gehen.
3. Workflow **Build Windows EXE** auswählen.
4. Auf **Run workflow** klicken.
5. Das Feld **entry_script** ist standardmäßig `game.py`. Nur ändern, wenn deine Startdatei anders heißt (z. B. `src/main.py`).
6. Warten bis der Job fertig ist.
7. Unter **Artifacts** die Datei **KitchenHustle-windows-exe** herunterladen.
8. ZIP entpacken und `KitchenHustle.exe` starten.

## Wenn bei „Actions“ nichts angezeigt wird (wichtig)

Prüfe diese Punkte:

1. **Workflow-Datei ist auf GitHub gepusht?**
   - Datei muss vorhanden sein: `.github/workflows/build-windows-exe.yml`.
2. **Du bist auf dem richtigen Branch?**
   - Der Workflow reagiert auf `main` und `work`.
   - Wenn dein Branch anders heißt, erscheint er evtl. nicht automatisch bei Push.
3. **Actions im Repo aktiviert?**
   - In GitHub: `Settings -> Actions -> General`.
   - Erlaubt sein muss mindestens „Allow all actions and reusable workflows“.
4. **Erster Push schon erfolgt?**
   - Vor dem ersten Push gibt es in GitHub noch keine Workflow-Datei, daher auch keinen Action-Eintrag.

Wenn du möchtest, kann ich den Workflow auch so anpassen, dass er auf **allen Branches** bei Push läuft.

## Falls Windows SmartScreen warnt

- Auf **Weitere Informationen** klicken
- Dann **Trotzdem ausführen**

## Optional: Lokal mit Python bauen (falls später vorhanden)

```powershell
py -m pip install pyinstaller
py -m PyInstaller --noconfirm --onefile --windowed --name KitchenHustle game.py
```

Die EXE liegt dann in `dist\KitchenHustle.exe`.

Hinweis: Der Workflow verwendet das Feld `entry_script` (Standard `game.py`). Passe es an, wenn deine Startdatei in einem Unterordner liegt.

## Fehler „game.py wurde im Repository nicht gefunden“

Der Workflow hat ein Eingabefeld **entry_script** (Standard: `game.py`).

- Öffne **Actions -> Build Windows EXE -> Run workflow**
- Trage bei **entry_script** deinen echten Dateipfad ein (z. B. `game.py`, `src/game.py` oder `main.py`)
- Starte den Workflow erneut

Der Workflow baut jetzt **nur** das Script aus `entry_script` (Standard: `game.py`).
Wenn diese Datei im gewählten Branch nicht existiert, bricht der Run mit einer klaren Fehlermeldung ab.


Wichtig: Wähle beim **Run workflow** den Branch aus, in dem `game.py` liegt. Sonst bricht der Build mit Fehler ab (statt eine Hinweis-EXE zu erzeugen).


Hinweis: Bei `push`-Runs ist `entry_script` technisch leer (weil es kein manuelles Formular gibt). Der Workflow nutzt dann automatisch `game.py`.


Hinweis: Push-Runs ohne `game.py` werden jetzt **ohne Fehler übersprungen**. Für eine echte EXE nutze **Run workflow** und wähle den Branch mit deiner Startdatei.
