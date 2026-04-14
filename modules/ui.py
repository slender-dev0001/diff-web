import time
import os
from colorama import Fore, Style
from pystyle import Center

class UI:
    """Gestion de l'interface utilisateur"""
    
    def __init__(self):
        pass
    
    def white_gradient(self, text):
        """Applique un gradient blanc au texte"""
        os.system("")
        faded = ""
        white = 120
        for line in text.splitlines():
            faded += (f"\033[38;2;{white};{white};{white}m{line}\033[0m\n")
            if white != 255:
                white += 15
                if white > 255:
                    white = 255
        return faded
    
    def slow_write(self, text):
        """Affiche le texte caractère par caractère"""
        for x in text:
            print('', x, end="", flush=True)
            time.sleep(0.0000)
    
    def clear_screen(self):
        """Efface l'écran"""
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except:
            pass
    
    def display_welcome(self):
        """Affiche le message de bienvenue initial"""
        self.clear_screen()
        print("\n" * 5)
        print(Center.XCenter(f"""
\033[96m╔═══════════════════════════════════════════════════════════════════════╗\033[0m
\033[96m║\033[0m                                                                       \033[96m║\033[0m
\033[96m║\033[0m        \033[92mBIENVENUE ET MERCI D'UTILISER LE \033[96mDIFF-TOOL\033[0m                     \033[96m║\033[0m
\033[96m║\033[0m        \033[37mCe logiciel est protégé. Tous droits réservés © Slender.\033[0m       \033[96m║\033[0m
\033[96m║\033[0m                                                                       \033[96m║\033[0m
\033[96m╚═══════════════════════════════════════════════════════════════════════╝\033[0m
        """))
        print("\n")
        input(Center.XCenter("\033[92m[ Appuyez sur ENTRÉE pour continuer ]\033[0m"))
        self.clear_screen()

    def display_logo(self):
        """Affiche le logo principal"""
        logo = Center.XCenter(f"""
\033[38;2;255;255;255m########  #### ######## ########         ########  #######   #######  ##       \033[0m
\033[38;2;230;230;230m##     ##  ##  ##       ##                  ##    ##     ## ##     ## ##       \033[0m
\033[38;2;205;205;205m##     ##  ##  ##       ##                  ##    ##     ## ##     ## ##       \033[0m
\033[38;2;180;180;180m##     ##  ##  ######   ######   #######    ##    ##     ## ##     ## ##       \033[0m
\033[38;2;155;155;155m##     ##  ##  ##       ##                  ##    ##     ## ##     ## ##       \033[0m
\033[38;2;130;130;130m##     ##  ##  ##       ##                  ##    ##     ## ##     ## ##       \033[0m
\033[38;2;105;105;105m########  #### ##       ##                  ##     #######   #######  ########\033[0m
        """)
        time.sleep(0.0002)
        print(self.white_gradient(logo), end='')
        self.slow_write(Center.XCenter(f""""""))
    
    def display_menu(self):
        """Affiche le menu principal cyberpunk/matrix"""
        print(Center.XCenter(f"""
\033[90m    ┌─────────────────────────────────────────────────────────────────────┐\033[0m
\033[90m    │\033[0m \033[92m>>>\033[0m \033[37mVERSION\033[0m: \033[92m1.1\033[0m              \033[92m>>>\033[0m \033[37mDEV\033[0m: \033[92mSlender\033[0m                      \033[90m│\033[0m
\033[90m    └─────────────────────────────────────────────────────────────────────┘\033[0m

\033[90m    ╔═══════════════════════════╦═══════════════════════════════════════════╗\033[0m
\033[90m    ║\033[0m  \033[92m[\033[96m01\033[92m]\033[0m \033[96m█\033[0m \033[37mSuppr. Channels\033[0m   \033[90m║\033[0m  \033[92m[\033[96m06\033[92m]\033[0m \033[96m█\033[0m \033[37mSpam Webhook\033[0m                      \033[90m║\033[0m
\033[90m    ║\033[0m  \033[92m[\033[96m02\033[92m]\033[0m \033[96m█\033[0m \033[37mSuppr. Rôles\033[0m      \033[90m║\033[0m  \033[92m[\033[96m08\033[92m]\033[0m \033[96m█\033[0m \033[37mSuppr. Emojis\033[0m                     \033[90m║\033[0m
\033[90m    ║\033[0m  \033[92m[\033[96m03\033[92m]\033[0m \033[96m█\033[0m \033[37mBannir Membres\033[0m    \033[90m║\033[0m  \033[92m[\033[96m09\033[92m]\033[0m \033[96m█\033[0m \033[37mSuppr. Stickers\033[0m                   \033[90m║\033[0m
\033[90m    ║\033[0m  \033[92m[\033[96m04\033[92m]\033[0m \033[96m█\033[0m \033[37mCréer Channels\033[0m    \033[90m║\033[0m  \033[92m[\033[96m10\033[92m]\033[0m \033[96m█\033[0m \033[37mRenommer Serveur\033[0m                  \033[90m║\033[0m
\033[90m    ║\033[0m  \033[92m[\033[96m05\033[92m]\033[0m \033[96m█\033[0m \033[37mCréer des Rôles\033[0m   \033[90m║\033[0m  \033[92m[\033[96m11\033[92m]\033[0m \033[96m█\033[0m \033[37mSpam Channels\033[0m                     \033[90m║\033[0m
\033[90m    ╠═══════════════════════════╩═══════════════════════════════════════════╣\033[0m
\033[90m    ║\033[0m  \033[92m[\033[92m12\033[92m]\033[0m\033[92m█ LANCER L'INTERFACE WEB (MODERNE)\033[0m                               \033[90m║\033[0m
\033[90m    ║\033[0m  \033[92m[\033[91m07\033[92m]\033[0m\033[91m█ MODE BOT NUKER\033[0m                                                 \033[90m║\033[0m
\033[90m    ║\033[0m  \033[92m[\033[96m20\033[92m]\033[0m\033[96m█ AIDE DU TOOL\033[0m                                                   \033[90m║\033[0m
\033[90m    ║\033[0m  \033[92m[\033[95m69\033[92m]\033[0m\033[95m█\033[0m \033[95mDiscord Support\033[0m                                                \033[90m║\033[0m
\033[90m    ║\033[0m  \033[92m[\033[91m0\033[92m]\033[0m \033[91m█\033[0m \033[91mDÉCONNEXION\033[0m                                                    \033[90m║\033[0m
\033[90m    ╚═══════════════════════════════════════════════════════════════════════╝\033[0m
    """))
    
    def display_help(self):
        """Affiche l'aide du tool"""
        self.clear_screen()
        print(Center.XCenter(f"""
\033[92m╔═══════════════════════════════════════════════════════════════════════╗\033[0m
\033[92m║\033[0m                          \033[96mAIDE DU DIFF-TOOL\033[0m                            \033[92m║\033[0m
\033[92m╠═══════════════════════════════════════════════════════════════════════╣\033[0m
\033[92m║\033[0m \033[37mCe tool est conçu pour tester vos serveurs Discord.\033[0m                   \033[92m║\033[0m
\033[92m║\033[0m                                                                       \033[92m║\033[0m
\033[92m║\033[0m \033[96m- Options 01-05 :\033[0m \033[37mGestion de base (Channels, Rôles, Membres).\033[0m         \033[92m║\033[0m
\033[92m║\033[0m \033[96m- Options 06, 11 :\033[0m \033[37mFonctions de Spam (Webhooks & Channels).\033[0m           \033[92m║\033[0m
\033[92m║\033[0m \033[96m- Option 07 :\033[0m \033[91mMode Bot Nuker\033[0m \033[37m(Lance un nuke complet).\033[0m                 \033[92m║\033[0m
\033[92m║\033[0m \033[96m- Options 08-10 :\033[0m \033[37mNettoyage d'emojis, stickers et renommage.\033[0m          \033[92m║\033[0m
\033[92m║\033[0m                                                                       \033[92m║\033[0m
\033[92m║\033[0m \033[37mUtilisez avec précaution. Développé par Slender.\033[0m                      \033[92m║\033[0m
\033[92m╚═══════════════════════════════════════════════════════════════════════╝\033[0m
        """))
        input("\033[92mAppuyez sur Entrée pour revenir au menu...\033[0m")

    def get_choice(self):
        """Demande et retourne le choix de l'utilisateur"""
        return input("\033[92m    ┌──[\033[96mSYSTEM\033[92m]─[\033[96mCMD\033[92m]\033[0m\n\033[92m    └──> \033[0m")
    
    def display_full_interface(self):
        """Affiche l'interface complète : logo + menu"""
        self.clear_screen()
        self.display_logo()
        self.display_menu()
        return self.get_choice()
    
    def display_simple_interface(self):
        """Affiche seulement le menu (sans logo)"""
        self.clear_screen()
        self.display_menu()
        return self.get_choice()
    
    def success(self, message):
        """Affiche un message de succès"""
        print(f"\033[92m[✓] {message}\033[0m")
    
    def error(self, message):
        """Affiche un message d'erreur"""
        print(f"\033[91m[✗] {message}\033[0m")
    
    def info(self, message):
        """Affiche un message d'information"""
        print(f"\033[96m[ℹ] {message}\033[0m")
    
    def warning(self, message):
        """Affiche un message d'avertissement"""
        print(f"\033[93m[⚠] {message}\033[0m")


# Pour les tests ou utilisation directe
if __name__ == "__main__":
    ui = UI()
    choice = ui.display_full_interface()
    print(f"\nVous avez choisi: {choice}")