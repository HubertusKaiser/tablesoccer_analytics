from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from db import fetch_last_matches, delete_last_match, get_last_match

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical')
        
        # Back button
        back_btn = Button(
            text='← Zurück',
            size_hint_y=0.1,
            on_press=self.go_back
        )
        
        # Title
        title = Label(
            text="Letzte Spiele",
            font_size='24sp',
            size_hint_y=0.1,
            halign='center'
        )
        
        # Scrollable container for matches
        scroll = ScrollView()
        self.matches_layout = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(5),
            padding=dp(10)
        )
        self.matches_layout.bind(minimum_height=self.matches_layout.setter('height'))
        scroll.add_widget(self.matches_layout)
        
        # Delete last match button
        delete_btn = Button(
            text="Letztes Spiel löschen",
            size_hint_y=0.1,
            background_color=(0.9, 0.3, 0.3, 1),
            on_press=self.confirm_delete_last_match
        )
        
        layout.add_widget(back_btn)
        layout.add_widget(title)
        layout.add_widget(scroll)
        layout.add_widget(delete_btn)
        
        self.add_widget(layout)
    
    def load_matches(self):
        # Clear existing matches
        self.matches_layout.clear_widgets()
        
        # Load matches from database
        matches = fetch_last_matches(limit=10)
        
        if not matches:
            self.matches_layout.add_widget(Label(
                text="Keine Spiele gefunden.",
                font_size='16sp',
                size_hint_y=None,
                height=dp(50)
            ))
            return
        
        # Add matches to layout
        for match in matches:
            datum, a1, a2, ta, tb, b1, b2, gewinner = match
            
            if gewinner == "Team A":
                text = f"{datum}:   {a1} & {a2}  {ta}:{tb}  {b1} & {b2}"
            else:
                text = f"{datum}:   {b1} & {b2}  {tb}:{ta}  {a1} & {a2}"
            
            label = Label(
                text=text,
                font_size='16sp',
                size_hint_y=None,
                height=dp(50),
                halign='left',
                text_size=(None, None),
                shorten=True,
                shorten_from='right',
                valign='middle'
            )
            self.matches_layout.add_widget(label)
    
    def confirm_delete_last_match(self, instance):
        match = get_last_match()
        if not match:
            self.show_message("Keine Spiele", "Es ist kein Spiel zum Löschen vorhanden.")
            return
            
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        message = (
            f"Letztes Spiel:\n"
            f"{match['team_a1']} & {match['team_a2']} ({match['tore_a']}) "
            f"vs {match['team_b1']} & {match['team_b2']} ({match['tore_b']})\n"
            f"Datum: {match['datum']}\n\n"
            f"Wirklich löschen?"
        )
        
        content.add_widget(Label(text=message))
        
        btn_layout = BoxLayout(spacing=dp(5))
        btn_yes = Button(text='Ja, löschen')
        btn_no = Button(text='Abbrechen')
        
        popup = Popup(
            title='Letztes Spiel löschen',
            content=content,
            size_hint=(0.9, 0.5)
        )
        
        def delete_and_close(instance):
            delete_last_match()
            popup.dismiss()
            self.load_matches()
            self.show_message("Gelöscht", "Letztes Spiel wurde gelöscht.")
        
        btn_yes.bind(on_press=delete_and_close)
        btn_no.bind(on_press=popup.dismiss)
        
        btn_layout.add_widget(btn_yes)
        btn_layout.add_widget(btn_no)
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
