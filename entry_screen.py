from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, ListProperty
from kivy.metrics import dp
from kivy.clock import Clock
from datetime import datetime
from db import get_player_frequencies, insert_match
from ui_components import PlayerButton, AddPlayerButton, ScoreLabel, StyledButton

PLAYER_COLUMNS = ["team_a_spieler1", "team_a_spieler2", "team_b_spieler1", "team_b_spieler2"]

class Numpad(GridLayout):
    active_team = StringProperty('A')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.spacing = dp(5)
        self.padding = dp(5)
        self.build_ui()
    
    def build_ui(self):
        self.team_label = Label(
            text="Aktiv: Team A",
            font_size='24sp',
            size_hint_y=0.2
        )
        self.add_widget(self.team_label)
        
        switch_btn = Button(
            text="⇆ Team wechseln",
            size_hint_y=0.2,
            font_size='24sp',
            on_press=self.toggle_team
        )
        self.add_widget(switch_btn)
        
        buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            '10', '0', '←'
        ]
        
        for btn in buttons:
            button = Button(
                text=btn,
                font_size='24sp',
                on_press=self.on_button_press
            )
            self.add_widget(button)
    
    def toggle_team(self, instance):
        self.active_team = 'B' if self.active_team == 'A' else 'A'
        self.team_label.text = f"Aktiv: Team {self.active_team}"
    
    def on_button_press(self, instance):
        if not self.parent:
            return
        if self.active_team == 'A':
            current = self.parent.parent.tore_team_a
            if instance.text == '←':
                new_score = current[:-1]
                self.parent.parent.tore_team_a = new_score
            else:
                new_score = current + instance.text
                self.parent.parent.tore_team_a = new_score
                self.toggle_team(None)
        else:
            current = self.parent.parent.tore_team_b
            if instance.text == '←':
                new_score = current[:-1]
                self.parent.parent.tore_team_b = new_score
            else:
                new_score = current + instance.text
                self.parent.parent.tore_team_b = new_score
                self.toggle_team(None)

class EntryScreen(Screen):
    selected_players = ListProperty([])
    tore_team_a = StringProperty('')
    tore_team_b = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.players = [name for name, _ in get_player_frequencies()]
        self.player_buttons = {}
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical')
        back_btn = StyledButton(
            text='← Zurück',
            size_hint_y=0.1,
            font_size='24sp',
            on_press=self.go_back
        )
        self.player_grid = GridLayout(cols=3, spacing=dp(5), padding=dp(5), size_hint_y=0.5)
        self.build_player_buttons()
        add_player_btn = AddPlayerButton(on_press=self.show_add_player_popup)
        score_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, padding=dp(5), spacing=dp(5))
        team_a_label = ScoreLabel(text="Tore Team A:")
        self.score_a = ScoreLabel(text=self.tore_team_a)
        team_b_label = ScoreLabel(text="Tore Team B:")
        self.score_b = ScoreLabel(text=self.tore_team_b)
        score_layout.add_widget(team_a_label)
        score_layout.add_widget(self.score_a)
        score_layout.add_widget(team_b_label)
        score_layout.add_widget(self.score_b)
        self.numpad = Numpad(size_hint_y=0.5)
        save_btn = Button(
            text="Spiel speichern",
            size_hint_y=0.1,
            on_press=self.save_match
        )
        layout.add_widget(back_btn)
        layout.add_widget(self.player_grid)
        layout.add_widget(add_player_btn)
        layout.add_widget(score_layout)
        layout.add_widget(self.numpad)
        layout.add_widget(save_btn)
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'menu'
    
    def build_player_buttons(self):
        self.player_grid.clear_widgets()
        self.player_buttons = {}
        for name in self.players:
            btn = PlayerButton(name, screen=self)
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
                btn.background_color = (0.3, 0.8, 0.3, 1) if idx < 2 else (0.2, 0.5, 0.8, 1)
                btn.color = (1, 1, 1, 1)
            else:
                btn.background_color = (0.9, 0.9, 0.9, 1)
                btn.color = (0.1, 0.1, 0.1, 1)
    
    def show_add_player_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        name_input = TextInput(hint_text='Name des neuen Spielers', multiline=False)
        btn_layout = BoxLayout(spacing=dp(5))
        btn_ok = Button(text='OK')
        btn_cancel = Button(text='Abbrechen')
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
        self.selected_players = []
        self.tore_team_a = ''
        self.tore_team_b = ''
        self.update_button_colors()
        self.show_message("Erfolg", "Spiel gespeichert!")
        def return_to_menu(dt):
            self.manager.current = 'menu'
        Clock.schedule_once(return_to_menu, 1.5)
    
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
