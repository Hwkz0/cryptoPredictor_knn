import tkinter as tk
import customtkinter as ctk

class BasePage:
    
    def __init__(self, parent, state_manager, navigation_callback, status_callback):

        self.parent = parent
        self.state_manager = state_manager
        self.navigate_to = navigation_callback
        self.set_status = status_callback
        
        # Frame to contain all page content
        self.frame = ctk.CTkFrame(self.parent)
        
        # Flag to track if page is already built
        self.is_built = False
    
    def show(self):

        # Build the page
        if not self.is_built:
            self.build()
            self.is_built = True
        
        # Update page content if needed
        self.update_content()
        
        # Show the frame
        self.frame.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        self.frame.pack_forget()
    
    def build(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def update_content(self):
        pass
    
    def create_title(self, title_text, description_text=None):
        # Page title
        page_title = ctk.CTkLabel(
            self.frame,
            text=title_text,
            font=ctk.CTkFont(family="Helvetica", size=20, weight="bold")
        )
        page_title.pack(anchor=tk.W, padx=20, pady=(20, 10))
        
        # Description (optional)
        if description_text:
            description = ctk.CTkLabel(
                self.frame,
                text=description_text,
                font=ctk.CTkFont(family="Helvetica", size=14),
                text_color="gray"
            )
            description.pack(anchor=tk.W, padx=20, pady=(0, 20))
    
    def create_navigation_buttons(self, back_page=None, next_page=None, 
                                  back_text=None, next_text=None,
                                  next_command=None):
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Back button
        if back_page:
            back_text = back_text or f"Back: {back_page.title()}"
            back_button = ctk.CTkButton(
                button_frame,
                text=back_text,
                command=lambda: self.navigate_to(back_page),
                width=200,
                font=ctk.CTkFont(family="Helvetica", size=14)
            )
            back_button.pack(side=tk.LEFT, padx=20)
        
        # Next button
        if next_page or next_command:
            next_text = next_text or f"Next: {next_page.title()}"
            next_button = ctk.CTkButton(
                button_frame,
                text=next_text,
                command=next_command if next_command else lambda: self.navigate_to(next_page),
                width=200,
                height=40,
                font=ctk.CTkFont(family="Helvetica", size=14, weight="bold")
            )
            next_button.pack(side=tk.RIGHT, padx=20)
