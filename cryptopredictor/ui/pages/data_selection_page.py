import os
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from cryptopredictor.ui.base_page import BasePage

class DataSelectionPage(BasePage):

    
    def build(self):

        # Title and description with crypto-style
        self.create_title(
            "Step 1: Data Selection",
            "Select cryptocurrency data file and set up the output directory."
        )
        
        # Main container to hold both frames side by side
        main_container = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # Left container for data file selection
        data_frame = ctk.CTkFrame(main_container, corner_radius=10)
        data_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)
        
        # Crypto icon at the top of the data frame
        crypto_icon = ctk.CTkLabel(
            data_frame,
            text="₿ ",  # Bitcoin symbol
            font=ctk.CTkFont(family="Helvetica", size=50, weight="bold"),
        )
        crypto_icon.pack(pady=(20, 0))
        
        # Data file selection
        file_label = ctk.CTkLabel(
            data_frame,
            text="Cryptocurrency Data File (CSV):",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold")
        )
        file_label.pack(anchor=tk.CENTER, pady=(20, 5))
        
        file_description = ctk.CTkLabel(
            data_frame,
            text="Select CSV file containing historical cryptocurrency price data.",
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color="gray"
        )
        file_description.pack(anchor=tk.CENTER, pady=(0, 15))
        
        # File entry and browse button in a container
        file_input_frame = ctk.CTkFrame(data_frame, fg_color="transparent")
        file_input_frame.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        file_entry = ctk.CTkEntry(
            file_input_frame,
            textvariable=self.state_manager.data_file_path,
            placeholder_text="Path to your cryptocurrency data file",
            height=40
        )
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        file_button = ctk.CTkButton(
            file_input_frame,
            text="Browse Files",
            command=self._browse_file,
            width=150,
            height=40,
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        file_button.pack(side=tk.RIGHT)
        
        # Right container for output directory selection
        output_frame = ctk.CTkFrame(main_container, corner_radius=10)
        output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=10)
        
        # Crypto graph icon for output frame
        graph_icon = ctk.CTkLabel(
            output_frame,
            text="📈",  # Chart up emoji
            font=ctk.CTkFont(size=50)
        )
        graph_icon.pack(pady=(20, 0))
        
        # Output directory selection
        output_label = ctk.CTkLabel(
            output_frame,
            text="Output Directory:",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold")
        )
        output_label.pack(anchor=tk.CENTER, pady=(20, 5))
        
        output_description = ctk.CTkLabel(
            output_frame,
            text="Select a directory where analysis results and forecasts will be saved.",
            font=ctk.CTkFont(family="Helvetica", size=14),
            text_color="gray"
        )
        output_description.pack(anchor=tk.CENTER, pady=(0, 15))
        
        # Output directory entry and browse button container
        output_input_frame = ctk.CTkFrame(output_frame, fg_color="transparent")
        output_input_frame.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        output_entry = ctk.CTkEntry(
            output_input_frame,
            textvariable=self.state_manager.output_dir,
            placeholder_text="Path to output directory",
            height=40
        )
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        output_button = ctk.CTkButton(
            output_input_frame,
            text="Browse Folders",
            command=self._browse_output_dir,
            width=150,
            height=40,
            font=ctk.CTkFont(family="Helvetica", size=14)
        )
        output_button.pack(side=tk.RIGHT)

        # Bottom info section
        info_frame = ctk.CTkFrame(self.frame, corner_radius=10, fg_color="#1A2C42")
        info_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="Getting Started with Crypto Prophet",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color="#00A3FF"
        )
        info_title.pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        info_text = ctk.CTkLabel(
            info_frame,
            text="1. Select a CSV file containing historical cryptocurrency price data\n"
                 "2. Choose where to save your analysis results\n"
                 "3. Click 'Next' to proceed to model configuration\n\n"
                 "Your data should include columns like Date, Open, High, Low, Close, and Volume.",
            font=ctk.CTkFont(family="Helvetica", size=14),
            justify=tk.LEFT
        )
        info_text.pack(anchor=tk.W, padx=20, pady=(0, 15))
        
        # Navigation buttons with larger size for better visibility
        self.create_navigation_buttons(
            next_page="model_parameters",
            next_text="Next: Model Parameters",
            next_command=self._validate_and_navigate
        )
    
    def _browse_file(self):
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select Cryptocurrency Data File",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if filename:
            self.state_manager.data_file_path.set(filename)
    
    def _browse_output_dir(self):
        directory = filedialog.askdirectory(
            initialdir=os.getcwd(),
            title="Select Output Directory"
        )
        if directory:
            self.state_manager.output_dir.set(directory)
    
    def _validate_and_navigate(self):
        if not self.state_manager.data_file_path.get():
            from tkinter import messagebox
            messagebox.showwarning("Missing Data", "Please select a data file before proceeding.")
            return
        
        # Navigate to model parameters page
        self.navigate_to("model_parameters")
