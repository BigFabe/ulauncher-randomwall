from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
import os
import requests


class DemoExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        
        img_dir = os.path.dirname(os.path.realpath(__file__))
        
        
        api_key = extension.preferences['api_key']
        
        
        query = extension.preferences['query']
        if len(query) != 0:
            params={"query":query, "orientation":"landscape"}
        else:
            params={"orientation":"landscape"}
      
            

        request = requests.get(f"https://api.unsplash.com/photos/random?client_id={api_key}", params=params)
        
        if request.status_code != 200:
            return RenderResultListAction([ExtensionResultItem(icon = "images/icon.jpeg",
                                                               name = "No API Key!",
                                                               on_enter = HideWindowAction())])
        
        link=request.json()["links"]["download"]

        os.system(f"wget {link} -O {img_dir}/randomimg.png")

        desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
        
        if "gnome" in desktop_env:
            os.system(f'gsettings set org.gnome.desktop.background picture-uri-dark "file:///{img_dir}/randomimg.png"')
            os.system(f'gsettings set org.gnome.desktop.background picture-uri "file:///{img_dir}/randomimg.png"')
        elif "kde" in desktop_env:
            os.system(f"plasma-apply-wallpaperimage {img_dir}/randomimg.png")
        elif "mate" in desktop_env:
            os.system(f'gsettings set org.mate.background picture-filename "{img_dir}/randomimg.png"')
        elif "cinnamon" in desktop_env:
            os.system(f'gsettings set org.cinnamon.desktop.background picture-uri-dark "file:///{img_dir}/randomimg.png"')
            os.system(f'gsettings set org.cinnamon.desktop.background picture-uri "file:///{img_dir}/randomimg.png"')
        else:
            return RenderResultListAction([ExtensionResultItem(icon = "images/icon.jpeg",
                                                           name = f"{desktop_env} not supported!",
                                                           on_enter = HideWindowAction())])


        return RenderResultListAction([ExtensionResultItem(icon = "images/icon.jpeg",
                                                           name = "Wallpaper set",
                                                           on_enter = HideWindowAction())])
        

if __name__ == '__main__':
    DemoExtension().run()