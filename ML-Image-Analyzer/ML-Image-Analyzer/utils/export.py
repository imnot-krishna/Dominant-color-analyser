import os
import shutil
import json
from datetime import datetime

def create_export_directory(base_dir):
    """Create a timestamped directory for exports."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = os.path.join(base_dir, f"image_analysis_{timestamp}")
    os.makedirs(export_dir, exist_ok=True)
    return export_dir

def export_csv_data(csv_path, export_dir):
    """Export CSV data to the specified directory."""
    if not os.path.exists(csv_path):
        return False
    
    # Create a subdirectory for data
    data_dir = os.path.join(export_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Copy CSV file
    filename = os.path.basename(csv_path)
    destination = os.path.join(data_dir, filename)
    shutil.copy2(csv_path, destination)
    return True

def export_graph_figure(figure, name, export_dir):
    """Export a matplotlib figure in multiple formats."""
    # Create a subdirectory for figures
    figures_dir = os.path.join(export_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    # Save in multiple formats
    base_name = name.lower().replace(" ", "_")
    
    # Save as PNG (good for web/presentation)
    png_path = os.path.join(figures_dir, f"{base_name}.png")
    figure.savefig(png_path, dpi=300, bbox_inches='tight')
    
    # Save as PDF (good for publications)
    pdf_path = os.path.join(figures_dir, f"{base_name}.pdf")
    figure.savefig(pdf_path, bbox_inches='tight')
    
    # Save as SVG (good for editing)
    svg_path = os.path.join(figures_dir, f"{base_name}.svg")
    figure.savefig(svg_path, bbox_inches='tight')

def export_analysis_report(stats, export_dir):
    """Export a JSON report with analysis statistics."""
    # Create a subdirectory for reports
    reports_dir = os.path.join(export_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    # Save statistics as JSON
    report_path = os.path.join(reports_dir, "analysis_report.json")
    with open(report_path, 'w') as f:
        json.dump(stats, f, indent=4)

def create_html_report(stats, figures_paths, export_dir):
    """Create an HTML report combining all analysis results."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Image Analysis Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .stats { margin: 20px 0; }
            .figure { margin: 20px 0; }
            img { max-width: 100%; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Image Analysis Report</h1>
            <div class="stats">
                <h2>Statistics</h2>
                <table>
    """
    
    # Add statistics
    for key, value in stats.items():
        html_content += f"<tr><td><b>{key.replace('_', ' ').title()}</b></td><td>{value:.4f}</td></tr>"
    
    html_content += """
                </table>
            </div>
            <div class="figures">
                <h2>Figures</h2>
    """
    
    # Add figures
    for name, path in figures_paths.items():
        rel_path = os.path.relpath(path, export_dir)
        html_content += f"""
            <div class="figure">
                <h3>{name}</h3>
                <img src="{rel_path}" alt="{name}">
            </div>
        """
    
    html_content += """
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save HTML report
    report_path = os.path.join(export_dir, "analysis_report.html")
    with open(report_path, 'w') as f:
        f.write(html_content)
