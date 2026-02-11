import tkinter as tk


def main() -> None:
    root = tk.Tk()
    root.title("Kitchen Hustle")
    root.geometry("520x260")

    label = tk.Label(
        root,
        text=(
            "Kein Python-Startscript im Repo gefunden.\n"
            "Bitte setze im Workflow das Feld 'entry_script'."
        ),
        padx=20,
        pady=20,
        justify="center",
    )
    label.pack(expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
