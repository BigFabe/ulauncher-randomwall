from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
import os
import logging
from src.servicedownload import unsplash_download, wallhaven_download

ext_icon = "images/icon.jpeg"

class DemoExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
    
        try:
            return RenderResultListAction([
                ExtensionResultItem(icon=ext_icon,
                                    name=event.get_argument(),
                                    on_enter=ExtensionCustomAction(data = event.get_argument()))
            ])
        
        except:
            return RenderResultListAction([
                ExtensionResultItem(icon=ext_icon,
                                    name="Enter Searchstring or leave empty for super random",
                                    on_enter = ExtensionCustomAction(data = event.get_argument()))
            ])

class ItemEnterEventListener(EventListener):


    def on_event(self, event, extension):
        search_term = event.get_data()
        img_dir = os.path.dirname(os.path.realpath(__file__))
        api_key = extension.preferences['api_key']
        chosen_service = extension.preferences["service"]
        
        if chosen_service == "Unsplash":
            try:
                unsplash_download(search_term, api_key, img_dir)
            except:
                return RenderResultListAction([ExtensionResultItem(icon = ext_icon,
                                                            name = "No API Key!",
                                                            on_enter = HideWindowAction())])
        elif chosen_service == "Wallhaven.cc":
            try:
                wallhaven_download(search_term, img_dir)
            except:
                return RenderResultListAction([ExtensionResultItem(icon = ext_icon,
                                                            name = f"No connection to {chosen_service}",
                                                            on_enter = HideWindowAction())])


        desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
        logging.info(img_dir)
        if "gnome" in desktop_env:
            os.system(f'gsettings set org.gnome.desktop.background picture-uri-dark "file://{img_dir}/randomimg.png"')
            os.system(f'gsettings set org.gnome.desktop.background picture-uri "file://{img_dir}/randomimg.png"')
        elif "kde" in desktop_env:
            os.system(f"plasma-apply-wallpaperimage {img_dir}/randomimg.png")
        elif "mate" in desktop_env:
            os.system(f'gsettings set org.mate.background picture-filename "{img_dir}/randomimg.png"')
        elif "cinnamon" in desktop_env:
            os.system(f'gsettings set org.cinnamon.desktop.background picture-uri-dark "file://{img_dir}/randomimg.png"')
            os.system(f'gsettings set org.cinnamon.desktop.background picture-uri "file://{img_dir}/randomimg.png"')
        else:
            return RenderResultListAction([ExtensionResultItem(icon = ext_icon,
                                                           name = f"{desktop_env} not supported!",
                                                           on_enter = HideWindowAction())])

        
        return RenderResultListAction([ExtensionResultItem(icon = ext_icon,
                                                           name = "Wallpaper set",
                                                           on_enter = HideWindowAction())])
        

if __name__ == '__main__':
    DemoExtension().run()