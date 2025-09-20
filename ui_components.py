from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty

class StyledButton(Button):
    """Base styled button with common properties"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.9, 0.9, 0.9, 1)  # Default color
        self.font_size = '16sp'
        self.size_hint_y = None
        self.height = dp(50)
        self.padding = [dp(10), dp(5)]
        # Ensure dark text on light backgrounds
        self.color = (0, 0, 0, 1)

class PlayerButton(StyledButton):
    """Custom button for player selection"""
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.text = name

class TeamButton(StyledButton):
    """Button for team switching"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "⇆ Team wechseln"
        self.size_hint_y = 0.2

class NumpadButton(StyledButton):
    """Button for numpad input"""
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.size_hint = (1, 0.2)

class SaveButton(StyledButton):
    """Button for saving the match"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Spiel speichern"
        self.size_hint_y = 0.1
        self.background_color = (0.2, 0.7, 0.2, 1)  # Green color

class SettingsButton(StyledButton):
    """Base button for settings screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 0.4
        self.font_size = '20sp'
        self.background_color = COLORS['default']

class DeletePlayerGamesButton(SettingsButton):
    """Button for deleting all games of a player"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Alle Spiele eines Spielers löschen'
        handler = kwargs.get('on_press')
        if handler:
            self.bind(on_press=handler)

class RenamePlayerButton(SettingsButton):
    """Button for renaming a player"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Spieler umbenennen'
        handler = kwargs.get('on_press')
        if handler:
            self.bind(on_press=handler)

class BackButton(StyledButton):
    """Back button for navigation"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '← Zurück'
        self.size_hint_y = 0.1
        self.font_size = '20sp'
        handler = kwargs.get('on_press')
        if handler:
            self.bind(on_press=handler)

class DialogButton(StyledButton):
    """Base button for dialog boxes"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 0.4
        self.font_size = '16sp'

class ConfirmButton(DialogButton):
    """Confirmation button for dialogs"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = COLORS['delete']
        handler = kwargs.get('on_press')
        if handler:
            self.bind(on_press=handler)

class CancelButton(DialogButton):
    """Cancel button for dialogs"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Abbrechen'
        handler = kwargs.get('on_press')
        if handler:
            self.bind(on_press=handler)

class DeleteConfirmButton(ConfirmButton):
    """Delete confirmation button"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Ja, löschen'

class MenuButton(StyledButton):
    """Base button for main menu"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 0.4
        self.font_size = '24sp'
        self.background_color = COLORS['default']

class EntryButton(MenuButton):
    """Button for entering match results"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Ergebnisse eintragen'

class HistoryButton(MenuButton):
    """Button for viewing match history"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Letzte Spiele'

class SettingsButton(MenuButton):
    """Button for accessing settings"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Einstellungen und Setup'

class RenameButton(DialogButton):
    """Button for renaming actions"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = 'Umbenennen'
        self.background_color = COLORS['save']

class AddPlayerButton(StyledButton):
    """Button for adding a new player"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Neuen Spieler hinzufügen"
        self.size_hint_y = 0.1
        self.background_color = COLORS['add']

class StyledLabel(Label):
    """Base styled label with common properties"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '16sp'
        self.color = (0, 0, 0, 1)  # Black text
        self.halign = 'center'
        self.valign = 'middle'

class ScoreLabel(StyledLabel):
    """Label for displaying scores"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '24sp'
        self.size_hint_x = 0.2

class TeamLabel(StyledLabel):
    """Label for team information"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = 0.3

# Color constants for easy reference
COLORS = {
    'team_a': (0.56, 0.93, 0.56, 1),  # lightgreen
    'team_b': (0.68, 0.85, 0.9, 1),    # lightblue
    'default': (0.9, 0.9, 0.9, 1),     # lightgray
    'save': (0.2, 0.7, 0.2, 1),        # green
    'add': (0.2, 0.5, 0.8, 1),         # blue
    'delete': (0.8, 0.2, 0.2, 1)       # red
}

# Common dimensions
DIMENSIONS = {
    'button_height': dp(50),
    'small_button_height': dp(40),
    'padding': dp(10),
    'spacing': dp(5)
}
