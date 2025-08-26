from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.clock import Clock
from datetime import datetime
from db import get_player_frequencies, insert_match
from config import text_parameter
from ui_components import (PlayerButton, TeamButton, NumpadButton, 
                          SaveButton, AddPlayerButton, ScoreLabel, 
                          TeamLabel, COLORS, DIMENSIONS)

def on_button_press(self, instance):
        self.parent.parent.parent.toggle_player(self.name)

class Numpad(GridLayout):
    """Numpad for score input"""
    active_team = StringProperty('A')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.spacing = dp(5)
        self.padding = dp(5)
        self.active_score = None
        self.build_ui()
    
    def build_ui(self):
        # Team indicator and switch
        self.team_label = TeamLabel(text="Aktiv: Team A")
        self.add_widget(self.team_label)
        
        switch_btn = TeamButton(on_press=self.toggle_team)
        self.add_widget(switch_btn)
        
        # Numpad buttons
        buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            '10', '0', '←'
        ]
        
        for btn in buttons:
            button = NumpadButton(text=btn, on_press=self.on_button_press)
            self.add_widget(button)
    
    def toggle_team(self, instance):
        self.active_team = 'B' if self.active_team == 'A' else 'A'
        self.team_label.text = f"Aktiv: Team {self.active_team}"
    
    def on_button_press(self, instance):
        if not self.parent:
            return
            
        score_var = self.parent.tore_team_a if self.active_team == 'A' else self.parent.tore_team_b
        current = score_var.text
        
        if instance.text == '←':
            score_var.text = current[:-1]
        else:
            score_var.text = current + instance.text
            self.toggle_team(None)

class KickerApp(App):
    selected_players = ListProperty([])
    tore_team_a = StringProperty('')
    tore_team_b = StringProperty('')
    
    def build(self):
        self.title = text_parameter.titel
        self.root = BoxLayout(orientation='vertical')
        self.players = [name for name, _ in get_player_frequencies()]
        self.player_buttons = {}
        
        # Player grid
        self.player_grid = GridLayout(cols=3, spacing=dp(5), padding=dp(5), size_hint_y=0.6)
        self.build_player_buttons()
        
        # Add player button
        add_player_btn = AddPlayerButton(on_press=self.show_add_player_popup)
        
        # Score display
        score_layout = BoxLayout(
            orientation='horizontal', 
            size_hint_y=0.1,
            padding=DIMENSIONS['padding'],
            spacing=DIMENSIONS['spacing']
        )
        score_layout.add_widget(TeamLabel(text="Tore Team A:"))
        self.score_a = ScoreLabel(text=self.tore_team_a)
        score_layout.add_widget(self.score_a)
        score_layout.add_widget(TeamLabel(text="Tore Team B:"))
        self.score_b = ScoreLabel(text=self.tore_team_b)
        score_layout.add_widget(self.score_b)
        
        # Numpad
        self.numpad = Numpad(size_hint_y=0.5)
        
        # Save button
        save_btn = SaveButton(on_press=self.save_match)
        
        # Add all widgets to root
        self.root.add_widget(self.player_grid)
        self.root.add_widget(add_player_btn)
        self.root.add_widget(score_layout)
        self.root.add_widget(self.numpad)
        self.root.add_widget(save_btn)
        
        return self.root
    
    def build_player_buttons(self):
        self.player_grid.clear_widgets()
        self.player_buttons = {}
        
        for name in self.players:
            btn = PlayerButton(name, on_press=self.toggle_player)
            self.player_buttons[name] = btn
            self.player_grid.add_widget(btn)
    
    def toggle_player(self, name):
        if name in self.selected_players:
            self.selected_players.remove(name)
        elif len(self.selected_players) < 4:
            self.selected_players.append(name)
        else:
            self.show_message("Maximal 4 Spieler", "Du kannst nur 4 Spieler auswählen.")
            return
        
        self.update_button_colors()
    
    def update_button_colors(self):
        for name, btn in self.player_buttons.items():
            if name in self.selected_players:
                idx = self.selected_players.index(name)
                btn.background_color = COLORS['team_a'] if idx < 2 else COLORS['team_b']
            else:
                btn.background_color = COLORS['default']
    
    def show_add_player_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10))
        name_input = TextInput(hint_text='Name des neuen Spielers', multiline=False)
        
        btn_layout = BoxLayout(spacing=dp(5))
        btn_ok = StyledButton(text='OK', size_hint_y=0.4)
        btn_cancel = StyledButton(text='Abbrechen', size_hint_y=0.4)
        
        popup = Popup(
            title='Neuer Spieler',
            size_hint=(0.8, 0.4)
        )
        
        def add_player(instance):
            name = name_input.text.strip()
            if name and name not in self.players:
                self.players.append(name)
                self.build_player_buttons()
                self.update_button_colors()
                popup.dismiss()
        
        btn_ok.bind(on_press=add_player)
        btn_cancel.bind(on_press=popup.dismiss)
        
        btn_layout.add_widget(btn_ok)
        btn_layout.add_widget(btn_cancel)
        
        content.add_widget(name_input)
        content.add_widget(btn_layout)
        
        popup.content = content
        popup.open()
        
        # Focus the input field
        def focus_input(dt):
            name_input.focus = True
        Clock.schedule_once(focus_input, 0.1)
    
    def save_match(self, instance):
        if len(self.selected_players) != 4:
            self.show_message("Fehler", "Bitte genau 4 Spieler auswählen.")
            return
            
        a1, a2, b1, b2 = self.selected_players
        
        try:
            ta = int(self.tore_team_a or 0)
            tb = int(self.tore_team_b or 0)
        except ValueError:
            self.show_message("Fehler", "Ungültige Toranzahl.")
            return
            
        if ta == tb:
            self.show_message("Fehler", "Unentschieden ist nicht erlaubt.")
            return
            
        gewinner = "Team A" if ta > tb else "Team B"
        datum = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        insert_match(a1, a2, b1, b2, ta, tb, gewinner, datum)
        
        # Reset UI
        self.selected_players = []
        self.tore_team_a = ''
        self.tore_team_b = ''
        self.update_button_colors()
        
        self.show_message("Erfolg", "Spiel gespeichert!")
    
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
    
    def on_tore_team_a(self, instance, value):
        self.score_a.text = value
    
    def on_tore_team_b(self, instance, value):
        self.score_b.text = value

if __name__ == '__main__':
    KickerApp().run()
