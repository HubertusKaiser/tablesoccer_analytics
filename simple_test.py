from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
Logger.setLevel(logging.DEBUG)

class SimpleApp(App):
    def build(self):
        try:
            Logger.info("SimpleApp: Building UI...")
            layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
            
            # Add a simple button
            btn = Button(
                text='Test Button',
                size_hint=(1, 0.2),
                font_size='24sp'
            )
            
            layout.add_widget(btn)
            Logger.info("SimpleApp: UI built successfully")
            return layout
            
        except Exception as e:
            Logger.error(f"SimpleApp: Error in build: {str(e)}")
            import traceback
            Logger.error(traceback.format_exc())
            raise

if __name__ == '__main__':
    try:
        Logger.info("SimpleApp: Starting...")
        SimpleApp().run()
    except Exception as e:
        Logger.error(f"SimpleApp: Fatal error: {str(e)}")
        import traceback
        Logger.error(traceback.format_exc())
