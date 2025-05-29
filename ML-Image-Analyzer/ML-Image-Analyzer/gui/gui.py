import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import cv2

from analysis.analyzer import analyze_image
from analysis.image_stats import calculate_image_statistics
from analysis.image_comparison import compare_images
from utils.image_loader import load_image_thumbnail
from utils.export import export_csv_data, export_graph_figure

class ColorAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Analyzer")
        self.root.geometry("1200x800")
        self.root.configure(bg="#e0f7fa")

        self.image_path = None
        self.comparison_image_path = None
        self.clusters = tk.IntVar(value=5)
        self.export_csv_path = ""
        self.figures = {}
        self.tabs = {}
        self.comparison_mode = tk.BooleanVar(value=False)

        self.create_styles()
        self.setup_ui()

    def create_styles(self):
        style = ttk.Style()
        style.configure('Info.TButton', padding=5)
        style.configure('Help.TLabel', background='#f0f0f0', padding=10)
        style.configure('Action.TButton', padding=10, font=('Arial', 10, 'bold'))

    def setup_ui(self):
        # Main container
        self.main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left frame with scrollbar
        left_outer_frame = ttk.Frame(self.main_container)
        self.main_container.add(left_outer_frame, weight=1)

        # Create canvas and scrollbar for left panel
        canvas = tk.Canvas(left_outer_frame)
        scrollbar = ttk.Scrollbar(left_outer_frame, orient="vertical", command=canvas.yview)
        self.left_frame = ttk.Frame(canvas)

        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas
        canvas_frame = canvas.create_window((0, 0), window=self.left_frame, anchor="nw")

        # Configure canvas scrolling
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_frame, width=event.width)

        self.left_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_width)

        # Control Panel
        self.setup_control_panel()

        # Right frame for results
        self.right_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.right_frame, weight=3)

        # Notebook for results
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_control_panel(self):
        # Image Selection Frame
        image_frame = ttk.LabelFrame(self.left_frame, text="Image Selection", padding=10)
        image_frame.pack(fill=tk.X, padx=5, pady=5)

        self.image_label = ttk.Label(image_frame)
        self.image_label.pack(pady=5)

        ttk.Button(image_frame, text="Select Primary Image", command=self.select_image).pack(fill=tk.X, pady=2)
        
        # Comparison Frame
        comparison_frame = ttk.LabelFrame(self.left_frame, text="Image Comparison", padding=10)
        comparison_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add info button for comparison features
        info_frame = ttk.Frame(comparison_frame)
        info_frame.pack(fill=tk.X)
        
        ttk.Checkbutton(info_frame, text="Enable Comparison", variable=self.comparison_mode).pack(side=tk.LEFT)
        ttk.Button(info_frame, text="?", width=3, style='Info.TButton', 
                  command=self.show_comparison_info).pack(side=tk.RIGHT, padx=5)
        
        self.comparison_label = ttk.Label(comparison_frame)
        self.comparison_label.pack(pady=5)
        ttk.Button(comparison_frame, text="Select Comparison Image", 
                  command=self.select_comparison_image).pack(fill=tk.X, pady=2)

        # Analysis Options Frame
        analysis_frame = ttk.LabelFrame(self.left_frame, text="Analysis Options", padding=10)
        analysis_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(analysis_frame, text="Number of Dominant Colors:").pack()
        ttk.Spinbox(analysis_frame, from_=2, to=10, textvariable=self.clusters, width=5).pack(pady=5)

        # Action Buttons Frame - Now with more prominent styling
        action_frame = ttk.LabelFrame(self.left_frame, text="Actions", padding=10)
        action_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.BOTTOM)

        analyze_btn = ttk.Button(action_frame, text="Analyze Images", 
                               command=self.analyze, 
                               style='Action.TButton')
        analyze_btn.pack(fill=tk.X, pady=5)
        
        export_btn = ttk.Button(action_frame, text="Export Results", 
                              command=self.export_results, 
                              style='Action.TButton')
        export_btn.pack(fill=tk.X, pady=5)

    def show_comparison_info(self):
        """Show information about image comparison features and use cases."""
        info_text = """
Image Comparison Features and Use Cases

1. Quality Control:
   • Compare product photos for consistency
   • Detect manufacturing defects
   • Verify image reproduction quality

2. Photo Editing:
   • Compare before/after edits
   • Verify color corrections
   • Check image compression quality

3. Scientific Analysis:
   • Compare experimental results
   • Track changes over time
   • Analyze microscopy images

4. Design Verification:
   • Compare design iterations
   • Check brand color consistency
   • Verify print proofs

5. Security Applications:
   • Detect image tampering
   • Verify document authenticity
   • Compare surveillance footage

Comparison Metrics:
• Structural Similarity (SSIM)
• Color Channel Analysis
• Histogram Comparison
• Edge Detection
• Texture Analysis

How to Use:
1. Enable comparison mode
2. Load two images
3. Click Analyze to see:
   - Side-by-side comparison
   - Difference visualization
   - Similarity metrics
   - Channel-wise analysis
"""
        info_window = tk.Toplevel(self.root)
        info_window.title("Image Comparison Guide")
        info_window.geometry("600x700")
        
        # Make window modal
        info_window.transient(self.root)
        info_window.grab_set()
        
        # Add scrolled text widget
        text_widget = tk.Text(info_window, wrap=tk.WORD, padx=15, pady=15)
        scrollbar = ttk.Scrollbar(info_window, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Insert text with formatting
        text_widget.insert(tk.END, info_text)
        text_widget.configure(state='disabled')
        
        # Center window on screen
        info_window.update_idletasks()
        width = info_window.winfo_width()
        height = info_window.winfo_height()
        x = (info_window.winfo_screenwidth() // 2) - (width // 2)
        y = (info_window.winfo_screenheight() // 2) - (height // 2)
        info_window.geometry(f'{width}x{height}+{x}+{y}')

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            self.image_path = path
            self.tk_img = load_image_thumbnail(path)
            self.image_label.configure(image=self.tk_img)
            self.status_var.set(f"Primary image loaded: {os.path.basename(path)}")

    def select_comparison_image(self):
        if not self.comparison_mode.get():
            return
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            self.comparison_image_path = path
            self.comparison_tk_img = load_image_thumbnail(path)
            self.comparison_label.configure(image=self.comparison_tk_img)
            self.status_var.set(f"Comparison image loaded: {os.path.basename(path)}")

    def clear_tabs(self):
        for tab in self.tabs.values():
            tab.destroy()
        self.tabs.clear()
        self.figures.clear()

    def analyze(self):
        if not self.image_path:
            self.status_var.set("Please select an image first!")
            return

        self.clear_tabs()
        self.status_var.set("Analyzing image...")

        # Basic color analysis
        results = analyze_image(self.image_path, self.clusters.get())
        self.export_csv_path = results['csv_path']

        # Add basic analysis tabs
        for name, fig in results['figures'].items():
            self.add_tab(name, fig)

        # Add advanced statistics
        img = cv2.imread(self.image_path)
        stats = calculate_image_statistics(img)
        self.add_stats_tab("Image Statistics", stats)

        # Comparison analysis if enabled
        if self.comparison_mode.get() and self.comparison_image_path:
            img2 = cv2.imread(self.comparison_image_path)
            comparison_results = compare_images(img, img2)
            self.add_tab("Image Comparison", comparison_results['comparison_figure'])

        self.status_var.set("Analysis complete!")

    def add_tab(self, name, figure):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=name)
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.tabs[name] = frame
        self.figures[name] = figure

    def add_stats_tab(self, name, stats):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=name)
        
        # Create a text widget to display statistics
        text = tk.Text(frame, wrap=tk.WORD, height=20, width=40)
        text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Insert statistics with formatting
        text.tag_configure("heading", font=("Arial", 12, "bold"))
        text.tag_configure("value", font=("Arial", 10))
        
        for key, value in stats.items():
            text.insert(tk.END, f"{key.replace('_', ' ').title()}:\n", "heading")
            text.insert(tk.END, f"{value:.4f}\n\n", "value")
        
        text.configure(state='disabled')

    def export_results(self):
        if not self.export_csv_path:
            self.status_var.set("No analysis results to export!")
            return

        export_dir = filedialog.askdirectory(title="Select Export Directory")
        if not export_dir:
            return

        # Export CSV
        export_csv_data(self.export_csv_path, export_dir)

        # Export all figures
        for name, fig in self.figures.items():
            export_graph_figure(fig, name, export_dir)

        self.status_var.set(f"Results exported to {export_dir}")
