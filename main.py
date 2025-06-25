from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from datetime import datetime
from db import init_db, fetch_last_matches, delete_last_match, get_last_match
from config import text_parameter

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create main layout
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Create title layout
        title_layout = BoxLayout(orientation='vertical', size_hint_y=0.2)
        title = Label(
            text='Einstellungen und Setup',
            font_size='30sp'
        )
        title_layout.add_widget(title)
        
        # Create buttons layout
        buttons_layout = BoxLayout(orientation='vertical', spacing=dp(10))
        
        # Delete player games button
        btn_delete_player_games = Button(
            text='Alle Spiele eines Spielers löschen',
            size_hint_y=0.4,
            font_size='20sp',
            on_press=self.confirm_delete_player_games
        )
        
        # Rename player button
        btn_rename_player = Button(
            text='Spieler umbenennen',
            size_hint_y=0.4,
            font_size='20sp',
            on_press=self.show_rename_player_popup
        )
        
        # Back button
        btn_back = Button(
            text='← Zurück',
            size_hint_y=0.1,
            font_size='20sp',
            on_press=self.go_back
        )
        
        buttons_layout.add_widget(btn_delete_player_games)
        buttons_layout.add_widget(btn_rename_player)
        buttons_layout.add_widget(btn_back)
        
        # Add layouts to main layout
        layout.add_widget(title_layout)
        layout.add_widget(buttons_layout)
        
        self.add_widget(layout)
    
    def confirm_delete_player_games(self, instance):
        from db import get_all_players
        
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Get all players
        players = get_all_players()
        if not players:
            self.show_message("Keine Spieler", "Keine Spieler im System gefunden.")
            return
            
        # Create buttons for each player
        player_buttons = GridLayout(cols=2, spacing=dp(5), size_hint_y=None)
        player_buttons.bind(minimum_height=player_buttons.setter('height'))
        
        for player in players:
            btn = Button(
                text=player,
                size_hint_y=None,
                height=dp(40),
                on_press=lambda x, p=player: self.confirm_delete_player_games_final(p)
            )
            player_buttons.add_widget(btn)
            
        content.add_widget(Label(
            text="Wähle einen Spieler, dessen Spiele gelöscht werden sollen:",
            size_hint_y=None,
            height=dp(40)
        ))
        content.add_widget(player_buttons)
        
        popup = Popup(
            title='Spielerauswahl',
            content=content,
            size_hint=(0.9, 0.8)
        )
        popup.open()

    def show_rename_player_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Get all players
        from db import get_all_players
        players = get_all_players()
        if not players:
            self.show_message("Keine Spieler", "Keine Spieler im System gefunden.")
            return
            
        # Create buttons for each player
        player_buttons = GridLayout(cols=2, spacing=dp(5), size_hint_y=None)
        player_buttons.bind(minimum_height=player_buttons.setter('height'))
        
        for player in players:
            btn = Button(
                text=player,
                size_hint_y=None,
                height=dp(40),
                on_press=lambda x, p=player: self.show_rename_input_popup(p)
            )
            player_buttons.add_widget(btn)
            
        content.add_widget(Label(
            text="Wähle einen Spieler zum Umbenennen:",
            size_hint_y=None,
            height=dp(40),
            font_size='20sp'
        ))
        content.add_widget(player_buttons)
        
        popup = Popup(
            title='Spieler auswählen',
            content=content,
            size_hint=(0.9, 0.8)
        )
        popup.open()

    def show_rename_input_popup(self, old_name):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Label and input field
        content.add_widget(Label(
            text=f"Neuer Name für {old_name}:",
            font_size='20sp'
        ))
        
        name_input = TextInput(
            multiline=False,
            font_size='20sp'
        )
        content.add_widget(name_input)
        
        # Buttons
        btn_layout = BoxLayout(spacing=dp(5))
        btn_rename = Button(
            text='Umbenennen',
            font_size='20sp'
        )
        btn_cancel = Button(
            text='Abbrechen',
            font_size='20sp'
        )
        
        popup = Popup(
            title='Spieler umbenennen',
            content=content,
            size_hint=(0.9, 0.5)
        )
        
        def rename_and_close(instance):
            new_name = name_input.text.strip()
            if not new_name:
                self.show_message("Fehler", "Bitte gib einen neuen Namen ein.")
                return
                
            from db import rename_player
            try:
                rename_player(old_name, new_name)
                popup.dismiss()
                self.show_message("Erfolgreich", "Spieler wurde erfolgreich umbenannt.")
            except Exception as e:
                self.show_message("Fehler", f"Fehler beim Umbenennen: {str(e)}")
        
        btn_rename.bind(on_press=rename_and_close)
        btn_cancel.bind(on_press=popup.dismiss)
        
        btn_layout.add_widget(btn_rename)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)
        
        popup.content = content
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'menu'

    def show_message(self, title, message):
        content = BoxLayout(orientation='vertical', padding=dp(10))
        content.add_widget(Label(text=message))
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4)
        )
        
        ok_btn = Button(text='OK')
        ok_btn.bind(on_press=popup.dismiss)
        content.add_widget(ok_btn)
        
        popup.open()

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        title = Label(
            text=text_parameter.titel,
            font_size='36sp',
            size_hint_y=0.2
        )
        
        btn_entry = Button(
            text='Ergebnisse eintragen',
            size_hint_y=0.4,
            font_size='24sp',
            on_press=self.switch_to_entry
        )
        
        btn_history = Button(
            text='Letzte Spiele',
            size_hint_y=0.4,
            font_size='24sp',
            on_press=self.switch_to_history
        )
        
        btn_settings = Button(
            text='Einstellungen und Setup',
            size_hint_y=0.4,
            font_size='24sp',
            on_press=self.switch_to_settings
        )
        
        layout.add_widget(title)
        layout.add_widget(btn_entry)
        layout.add_widget(btn_history)
        layout.add_widget(btn_settings)
        self.add_widget(layout)
    
    def switch_to_entry(self, instance):
        self.manager.current = 'entry'
    
    def switch_to_history(self, instance):
        self.manager.get_screen('history').load_matches()
        self.manager.current = 'history'
    
    def switch_to_settings(self, instance):
        self.manager.current = 'settings'

class KickerApp(App):
    def build(self):
        # Initialize database
        init_db()
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(EntryScreen(name='entry'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm

if __name__ == '__main__':
    from entry_screen import EntryScreen
    from history_screen import HistoryScreen
    KickerApp().run()
else:
    # For kivy_ui.py backward compatibility
    from entry_screen import EntryScreen as KickerApp
    from history_screen import HistoryScreen
