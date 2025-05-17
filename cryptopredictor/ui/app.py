import tkinter as tk
import customtkinter as ctk
from cryptopredictor.ui.base_page import BasePage
from cryptopredictor.ui.pages.data_selection_page import DataSelectionPage
from cryptopredictor.ui.pages.model_parameters_page import ModelParametersPage
from cryptopredictor.ui.pages.results_page import ResultsPage
from cryptopredictor.ui.pages.forecast_setup_page import ForecastSetupPage
from cryptopredictor.ui.pages.forecast_results_page import ForecastResultsPage
from cryptopredictor.ui.utils.state_manager import StateManager

class CryptoPredictorApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Crypto-AI - Price Prediction")
        
        # Position window at left uppermost corner (0,0)
        self.master.geometry("1920x1200+0+0")  # Format: widthxheight+x+y
        
        # Configure window to be in fullscreen windowed mode without decorations
        # Option 1: Without window decorations
        # self.master.overrideredirect(True)  # Uncomment to remove window frame/decorations completely
        
        # Option 2: Maximized but with window controls
        self.master.state('zoomed')  # Windows-specific zoomed state
        
        # Set up theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create state manager to share data between pages
        self.state_manager = StateManager()
        
        # Create main container frame
        self.main_frame = ctk.CTkFrame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create header
        self.create_header()
        
        # Create content frame where pages will be displayed
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create status bar
        self.create_status_bar()
        
        # Initialize pages
        self.pages = {}
        self.current_page = None
        self.initialize_pages()
        
        # Show initial page
        self.show_page("data_selection")
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title 
        title_label = ctk.CTkLabel(
            header_frame, 
            text="CRYPTO AI", 
            font=ctk.CTkFont(family="Helvetica", size=24, weight="bold")
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Advanced Price Prediction",
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color="gray"
        )
        subtitle_label.pack(side=tk.LEFT, padx=5, pady=10)
    
    def create_status_bar(self):
        status_frame = ctk.CTkFrame(self.main_frame, height=30, corner_radius=10)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.status_text = tk.StringVar(value="Ready to start")
        
        status_label = ctk.CTkLabel(
            status_frame, 
            textvariable=self.status_text,
            font=ctk.CTkFont(family="Helvetica", size=12)
        )
        status_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    def initialize_pages(self):
        self.pages = {
            "data_selection": DataSelectionPage(
                self.content_frame, 
                self.state_manager, 
                self.show_page,
                self.set_status_text
            ),
            "model_parameters": ModelParametersPage(
                self.content_frame, 
                self.state_manager, 
                self.show_page,
                self.set_status_text
            ),
            "results": ResultsPage(
                self.content_frame, 
                self.state_manager, 
                self.show_page,
                self.set_status_text
            ),
            "forecast_setup": ForecastSetupPage(
                self.content_frame, 
                self.state_manager, 
                self.show_page,
                self.set_status_text
            ),
            "forecast_results": ForecastResultsPage(
                self.content_frame, 
                self.state_manager, 
                self.show_page,
                self.set_status_text
            )
        }
    
    def show_page(self, page_name):
        if page_name not in self.pages:
            return
        
        # Hide current page if exists
        if self.current_page:
            self.pages[self.current_page].hide()
        
        # Show new page
        self.pages[page_name].show()
        self.current_page = page_name
    
    def set_status_text(self, text):
        """Update status bar text."""
        self.status_text.set(text)
        self.master.update_idletasks()

def launch_gui():
    root = ctk.CTk()
    app = CryptoPredictorApp(root)
    root.mainloop()

if __name__ == "__main__":
    launch_gui()
