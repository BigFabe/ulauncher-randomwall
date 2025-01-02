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
from gi.repository import Notify

ext_icon = "images/icon.jpeg"

class RandomwallU(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
    
    def show_notification(self, title, text=None, icon=ext_icon):
        Notify.init("RandomwallU")
        Notify.Notification.new(title, text, icon).show()


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        
        chosen_copy_shortcut = extension.preferences["copy_shortcut"]
        
        try:
            if event.get_argument() == chosen_copy_shortcut:
                return RenderResultListAction([
                    ExtensionResultItem(icon=ext_icon,
                                        name="Enter name of file.",
                                        on_enter=ExtensionCustomAction(data = event.get_argument()))
                ])
            
            return RenderResultListAction([
                ExtensionResultItem(icon=ext_icon,
                                    name=event.get_argument(),
                                    on_enter=ExtensionCustomAction(data = event.get_argument()))
            ])
        
        except:
            return RenderResultListAction([
                ExtensionResultItem(icon=ext_icon,
                                    name="Enter a category or press enter to search everything.",
                                    on_enter = ExtensionCustomAction(data = ""))
            ])


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        search_term = event.get_data()
        img_dir = os.path.dirname(os.path.realpath(__file__))
        api_key = extension.preferences['api_key']
        chosen_service = extension.preferences["service"]
        chosen_copy_location = extension.preferences["copy_location"]
        chosen_copy_shortcut = extension.preferences["copy_shortcut"]
        
        if chosen_copy_shortcut in search_term:
            
            try:    
                if chosen_copy_location[-1]=="/":
                    chosen_copy_location = chosen_copy_location[:-1]
            except IndexError:
                extension.show_notification("Error", "Set location in Extension Settings.")
                return RenderResultListAction([ExtensionResultItem(icon = ext_icon,
                                                            name = "Set location in Extension Settings.",
                                                            on_enter = HideWindowAction())])
            
            source = f"{img_dir}/randomimg.png"
            dest = os.path.expanduser(f"{chosen_copy_location}/{search_term[len(chosen_copy_shortcut)+1:]}")
            os.system(f"cp '{source}' '{dest}'")
            extension.show_notification("Success", f"Copied image to {dest}")
            return RenderResultListAction([ExtensionResultItem(icon = ext_icon,
                                                            name = "Copied image.",
                                                            on_enter = HideWindowAction())])

        if chosen_service == "Unsplash":
            try:
                unsplash_download(search_term, api_key, img_dir)
            except:
                extension.show_notification("Error", "No Results")
                return RenderResultListAction([ExtensionResultItem(icon = ext_icon,
                                                            name = "No API Key!",
                                                            on_enter = HideWindowAction())])
        elif chosen_service == "Wallhaven.cc":
            try:
                wallhaven_download(search_term, img_dir)
            except:
                extension.show_notification("Error", "No Results")
                return RenderResultListAction([ExtensionResultItem(icon = ext_icon,
                                                            name = f"No connection to {chosen_service}",
                                                            on_enter = HideWindowAction())])
        else:
            try:
                wallhaven_download(search_term, img_dir)
            except:
                extension.show_notification("Error", "No Results")
                return RenderResultListAction([ExtensionResultItem(icon = ext_icon,
                                                            name = f"No connection to {chosen_service}",
                                                            on_enter = HideWindowAction())])            


        desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
        
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
            extension.show_notification("Error", f"{desktop_env} not supported")
            return RenderResultListAction([ExtensionResultItem(icon = ext_icon,
                                                           name = f"{desktop_env} not supported!",
                                                           on_enter = HideWindowAction())])

       
        return RenderResultListAction([ExtensionResultItem(icon = ext_icon,
                                                           name = "Wallpaper set",
                                                           on_enter = HideWindowAction())])
        

if __name__ == '__main__':
    RandomwallU().run()