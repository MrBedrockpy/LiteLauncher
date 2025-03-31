import subprocess, string, random

import minecraft_launcher_lib as mll
from customtkinter import CTk, CTkLabel, CTkFont, CTkEntry, CTkComboBox, CTkButton, CTkCheckBox

MINECRAFT_DIRECTORY = "./.minecraft"


def get_random_username() -> str:
    return "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=random.randint(3, 16)))


class LauncherApp(CTk):

    WIDGET_WIDTH = 180
    WIDGET_HEIGHT = 40

    label: CTkLabel
    usernameEntry: CTkEntry
    randomUsername: CTkCheckBox
    versionEntry: CTkComboBox
    showSnapshots: CTkCheckBox
    playButton: CTkButton

    def __init__(self):
        super().__init__()
        self.setup_Ui()

    def get_options(self) -> mll.types.MinecraftOptions:
        if self.randomUsername:
            username: str = get_random_username()
        else:
            username: str = self.usernameEntry.get()
        return {
            'username': username,
            'uuid': '',
            'token': ''
        }

    def get_versions(self) -> list[str]:
        arr: list[str] = list()
        for version in mll.utils.get_version_list():
            if version['type'] == 'release' and self.showSnapshots.get() == 0:
                arr.append(version['id'])
            else:
                arr.append(version['id'])
        return arr

    def setup_Ui(self) -> None:

        self.geometry("400x600")
        self.resizable(False, False)
        self.title("LiteLauncher")

        font = CTkFont(size=14, weight='bold')
        self.label = CTkLabel(self, text="LiteLauncher", font=font)
        self.usernameEntry = CTkEntry(self, placeholder_text="Enter username", font=font, width=self.WIDGET_WIDTH, height=self.WIDGET_HEIGHT)
        self.randomUsername = CTkCheckBox(self, text="random username", font=font, width=self.WIDGET_WIDTH, height=self.WIDGET_HEIGHT)
        self.showSnapshots = CTkCheckBox(self, text="show snapshots", font=font, width=self.WIDGET_WIDTH, height=self.WIDGET_HEIGHT)
        self.versionEntry = CTkComboBox(self, values=self.get_versions(), font=font, width=self.WIDGET_WIDTH, height=self.WIDGET_HEIGHT)
        self.playButton = CTkButton(self, text="Play", command=self.launch_minecraft, width=self.WIDGET_WIDTH, height=self.WIDGET_HEIGHT)

        self.label.pack(pady=100)
        self.usernameEntry.pack(pady=20)
        self.randomUsername.pack(pady=0)
        self.versionEntry.pack(pady=15)
        self.showSnapshots.pack(pady=0)
        self.playButton.pack(pady=15)

    def launch_minecraft(self) -> None:
        if len(self.usernameEntry.get()) < 3 or len(self.usernameEntry.get()) > 16:
            return None
        print("Installing Minecraft")
        mll.install.install_minecraft_version(self.versionEntry.get(), MINECRAFT_DIRECTORY)
        print("Launching Minecraft")
        subprocess.call(mll.command.get_minecraft_command(self.versionEntry.get(), MINECRAFT_DIRECTORY, options=self.get_options()))


def main() -> None:
    app = LauncherApp()
    app.mainloop()


if __name__ == '__main__':
    main()
