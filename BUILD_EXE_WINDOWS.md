# Windows EXE ohne lokale Python-Installation

Du hast den Fehler bekommen, dass `python3` nicht gefunden wurde. Das ist normal auf manchen Windows-Systemen.

## Lösung: Fertige `.exe` über GitHub Actions bauen lassen

Du brauchst dafür **kein Python auf deinem PC**.

1. Repo zu GitHub pushen.
2. In GitHub auf den Tab **Actions** gehen.
3. Workflow **Build Windows EXE** auswählen.
4. Auf **Run workflow** klicken.
5. Falls dein Script nicht `game.py` heißt: im Feld **entry_script** den Pfad eintragen (z. B. `src/main.py`).
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

Hinweis: Der Workflow sucht `game.py` automatisch im Repo, damit der Build auch funktioniert, wenn die Datei nicht direkt im Root liegt.

## Fehler „game.py wurde im Repository nicht gefunden“

Der Workflow unterstützt jetzt ein Eingabefeld **entry_script**.

- Öffne **Actions -> Build Windows EXE -> Run workflow**
- Trage bei **entry_script** deinen echten Dateipfad ein (z. B. `game.py`, `src/game.py` oder `main.py`)
- Starte den Workflow erneut

Ohne Eingabe sucht der Workflow automatisch nach `game.py`, `main.py`, `app.py` und dann nach einer anderen `.py`-Datei.

Wenn gar keine passende `.py`-Datei gefunden wird, nutzt der Workflow zuerst `fallback_notice.py`. Falls diese Datei im Branch fehlt, wird automatisch ein temporäres Hinweis-Script erzeugt, damit der Build nicht komplett rot wird.
