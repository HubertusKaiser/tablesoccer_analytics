from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from datetime import datetime
from db import init_db, fetch_last_matches, delete_last_match, get_last_match
from config import text_parameter

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        title = Label(
            text=text_parameter.titel,
            font_size='24sp',
            size_hint_y=0.2
        )
        
        btn_entry = Button(
            text='Ergebnisse eintragen',
            size_hint_y=0.4,
            on_press=self.switch_to_entry
        )
        
        btn_history = Button(
            text='Letzte Spiele',
            size_hint_y=0.4,
            on_press=self.switch_to_history
        )
        
        layout.add_widget(title)
        layout.add_widget(btn_entry)
        layout.add_widget(btn_history)
        self.add_widget(layout)
    
    def switch_to_entry(self, instance):
        self.manager.current = 'entry'
    
    def switch_to_history(self, instance):
        self.manager.get_screen('history').load_matches()
        self.manager.current = 'history'

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
        
        return sm

if __name__ == '__main__':
    from entry_screen import EntryScreen
    from history_screen import HistoryScreen
    KickerApp().run()
else:
    # For kivy_ui.py backward compatibility
    from entry_screen import EntryScreen as KickerApp
    from history_screen import HistoryScreen
