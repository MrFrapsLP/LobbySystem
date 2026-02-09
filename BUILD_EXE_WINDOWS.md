# Windows EXE ohne lokale Python-Installation

Du hast den Fehler bekommen, dass `python3` nicht gefunden wurde. Das ist normal auf manchen Windows-Systemen.

## Lösung: Fertige `.exe` über GitHub Actions bauen lassen

Du brauchst dafür **kein Python auf deinem PC**.

1. Repo zu GitHub pushen.
2. In GitHub auf den Tab **Actions** gehen.
3. Workflow **Build Windows EXE** auswählen.
4. Auf **Run workflow** klicken.
5. Warten bis der Job fertig ist.
6. Unter **Artifacts** die Datei **KitchenHustle-windows-exe** herunterladen.
7. ZIP entpacken und `KitchenHustle.exe` starten.

## Falls Windows SmartScreen warnt

- Auf **Weitere Informationen** klicken
- Dann **Trotzdem ausführen**

## Optional: Lokal mit Python bauen (falls später vorhanden)

```powershell
py -m pip install pyinstaller
py -m PyInstaller --noconfirm --onefile --windowed --name KitchenHustle game.py
```

Die EXE liegt dann in `dist\KitchenHustle.exe`.
