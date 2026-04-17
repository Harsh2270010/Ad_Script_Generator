"""
Advanced Ad Script Generation Workflow
Features: Batch processing, queue management, performance analytics, and multiple output formats
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import csv
from ad_script_generator import AdScriptGenerator


class Platform(Enum):
    """Supported social media platforms"""
    INSTAGRAM_REELS = "Instagram Reels"
    META_ADS = "Meta Ads"
    TIKTOK = "TikTok"
    YOUTUBE_SHORTS = "YouTube Shorts"


@dataclass
class AdScript:
    """Data class for an individual ad script"""
    topic: str
    hook: str
    problem_statement: str
    solution: str
    cta: str
    full_script: str
    platform: str
    date_generated: str
    estimated_duration: str
    script_number: int


class AdvancedAdWorkflow:
    """Advanced workflow management for ad script generation"""
    
    def __init__(self, output_dir: str = "ad_script_outputs"):
        """
        Initialize advanced workflow
        
        Args:
            output_dir: Directory to store outputs
        """
        self.generator = AdScriptGenerator()
        self.output_dir = output_dir
        self.scripts_queue = []
        self.analytics = {
            "total_generated": 0,
            "total_saved": 0,
            "total_errors": 0,
            "start_time": None,
            "end_time": None
        }
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_batch(self, topics: List[str], scripts_per_topic: int = 3) -> Dict[str, List[Dict]]:
        """
        Generate scripts for multiple topics in batch
        
        Args:
            topics: List of topics to generate scripts for
            scripts_per_topic: Number of scripts per topic
            
        Returns:
            Dictionary mapping topics to their generated scripts
        """
        print("\n" + "="*80)
        print("🚀 BATCH PROCESSING STARTED".center(80))
        print("="*80)
        
        self.analytics["start_time"] = datetime.now()
        batch_results = {}
        
        for topic in topics:
            print(f"\n📌 Processing topic: {topic}")
            try:
                scripts = self.generator.create_workflow(topic, num_scripts=scripts_per_topic)
                batch_results[topic] = scripts
                self.analytics["total_generated"] += len(scripts)
                self.scripts_queue.extend(scripts)
            except Exception as e:
                print(f"❌ Error processing {topic}: {e}")
                self.analytics["total_errors"] += 1
        
        self.analytics["end_time"] = datetime.now()
        
        print("\n" + "="*80)
        print("✅ BATCH PROCESSING COMPLETED".center(80))
        print("="*80)
        
        return batch_results
    
    def export_to_json(self, scripts: List[Dict], filename: Optional[str] = None) -> str:
        """
        Export scripts to JSON format
        
        Args:
            scripts: List of script dictionaries
            filename: Custom filename (optional)
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ad_scripts_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(scripts, f, indent=2, ensure_ascii=False)
        
        self.analytics["total_saved"] += len(scripts)
        print(f"✓ JSON exported: {filepath}")
        return filepath
    
    def export_to_csv(self, scripts: List[Dict], filename: Optional[str] = None) -> str:
        """
        Export scripts to CSV format
        
        Args:
            scripts: List of script dictionaries
            filename: Custom filename (optional)
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ad_scripts_{timestamp}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        fieldnames = [
            'date', 'topic', 'hook', 'problem_statement', 
            'solution', 'cta', 'full_script', 'platform', 'estimated_duration'
        ]
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for script in scripts:
                row = {field: script.get(field, '') for field in fieldnames}
                writer.writerow(row)
        
        print(f"✓ CSV exported: {filepath}")
        return filepath
    
    def export_to_markdown(self, scripts: List[Dict], filename: Optional[str] = None) -> str:
        """
        Export scripts to Markdown format (human-readable)
        
        Args:
            scripts: List of script dictionaries
            filename: Custom filename (optional)
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ad_scripts_{timestamp}.md"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# Generated Ad Scripts\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total Scripts: {len(scripts)}\n\n")
            
            for i, script in enumerate(scripts, 1):
                f.write(f"## Script #{i}\n\n")
                f.write(f"**Topic:** {script.get('topic', 'N/A')}\n\n")
                f.write(f"**Date:** {script.get('date', 'N/A')}\n\n")
                
                f.write(f"### Viral Hook\n")
                f.write(f"> {script.get('hook', 'N/A')}\n\n")
                
                f.write(f"### Problem Statement\n")
                f.write(f"{script.get('problem_statement', 'N/A')}\n\n")
                
                f.write(f"### Solution\n")
                f.write(f"{script.get('solution', 'N/A')}\n\n")
                
                f.write(f"### Call to Action\n")
                f.write(f"**{script.get('cta', 'N/A')}**\n\n")
                
                f.write(f"### Full Script (15-20 seconds)\n")
                f.write(f"```\n{script.get('full_script', 'N/A')}\n```\n\n")
                
                f.write(f"**Platform:** {script.get('platform', 'N/A')}\n")
                f.write(f"**Duration:** {script.get('estimated_duration', '15-20 seconds')}\n\n")
                f.write("---\n\n")
        
        print(f"✓ Markdown exported: {filepath}")
        return filepath
    
    def export_to_html(self, scripts: List[Dict], filename: Optional[str] = None) -> str:
        """
        Export scripts to HTML format (for web viewing)
        
        Args:
            scripts: List of script dictionaries
            filename: Custom filename (optional)
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ad_scripts_{timestamp}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Ad Scripts</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .metadata {
            background: #f8f9fa;
            padding: 20px 30px;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
        }
        
        .metadata-item {
            text-align: center;
        }
        
        .metadata-item strong {
            display: block;
            color: #667eea;
            font-size: 1.2em;
        }
        
        .metadata-item span {
            color: #666;
            font-size: 0.95em;
        }
        
        .scripts-container {
            padding: 30px;
        }
        
        .script-card {
            background: white;
            border: 2px solid #667eea;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 25px;
            transition: all 0.3s ease;
        }
        
        .script-card:hover {
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
            transform: translateY(-5px);
        }
        
        .script-number {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        
        .script-section {
            margin: 20px 0;
        }
        
        .script-section-title {
            background: #f0f4ff;
            padding: 10px 15px;
            border-left: 4px solid #667eea;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
            border-radius: 3px;
        }
        
        .script-content {
            padding: 15px;
            background: #fafbff;
            border-radius: 5px;
            line-height: 1.6;
            color: #333;
        }
        
        .hook-highlight {
            font-style: italic;
            color: #764ba2;
            font-weight: 500;
        }
        
        .script-meta {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 0.9em;
            color: #666;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .meta-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 10px;
            background: #e7f3ff;
            color: #0066cc;
            border-radius: 3px;
            font-size: 0.85em;
            font-weight: 500;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 Generated Ad Scripts</h1>
            <p>High-Converting Instagram & Meta Ad Scripts</p>
        </div>
        
        <div class="metadata">
            <div class="metadata-item">
                <strong>{num_scripts}</strong>
                <span>Scripts Generated</span>
            </div>
            <div class="metadata-item">
                <strong>{timestamp}</strong>
                <span>Generation Date</span>
            </div>
        </div>
        
        <div class="scripts-container">
            {scripts_html}
        </div>
        
        <div class="footer">
            <p>Generated by AI Ad Script Automation Workflow</p>
        </div>
    </div>
</body>
</html>
        """
        
        scripts_html = ""
        for i, script in enumerate(scripts, 1):
            scripts_html += f"""
            <div class="script-card">
                <div class="script-number">Script #{i}</div>
                
                <div class="script-section">
                    <div class="script-section-title">📌 Viral Hook</div>
                    <div class="script-content">
                        <span class="hook-highlight">{script.get('hook', 'N/A')}</span>
                    </div>
                </div>
                
                <div class="script-section">
                    <div class="script-section-title">⚠️ Problem Statement</div>
                    <div class="script-content">{script.get('problem_statement', 'N/A')}</div>
                </div>
                
                <div class="script-section">
                    <div class="script-section-title">✨ Solution</div>
                    <div class="script-content">{script.get('solution', 'N/A')}</div>
                </div>
                
                <div class="script-section">
                    <div class="script-section-title">🎯 Call to Action</div>
                    <div class="script-content">{script.get('cta', 'N/A')}</div>
                </div>
                
                <div class="script-section">
                    <div class="script-section-title">🎞️ Full Script (15-20 seconds)</div>
                    <div class="script-content">{script.get('full_script', 'N/A')}</div>
                </div>
                
                <div class="script-meta">
                    <div class="meta-item">
                        <span>📱 Platform:</span>
                        <span class="badge">{script.get('platform', 'N/A')}</span>
                    </div>
                    <div class="meta-item">
                        <span>⏱️ Duration:</span>
                        <span class="badge">{script.get('estimated_duration', '15-20 seconds')}</span>
                    </div>
                    <div class="meta-item">
                        <span>📅 Topic:</span>
                        <span class="badge">{script.get('topic', 'N/A')}</span>
                    </div>
                </div>
            </div>
            """
        
        final_html = html_content.format(
            num_scripts=len(scripts),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            scripts_html=scripts_html
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"✓ HTML exported: {filepath}")
        return filepath
    
    def print_analytics(self):
        """Print workflow analytics"""
        print("\n" + "="*80)
        print("📊 WORKFLOW ANALYTICS".center(80))
        print("="*80)
        print(f"Total Scripts Generated: {self.analytics['total_generated']}")
        print(f"Total Scripts Saved: {self.analytics['total_saved']}")
        print(f"Total Errors: {self.analytics['total_errors']}")
        
        if self.analytics['start_time'] and self.analytics['end_time']:
            duration = (self.analytics['end_time'] - self.analytics['start_time']).total_seconds()
            print(f"Total Time: {duration:.2f} seconds")
        
        print("="*80 + "\n")


def main():
    """Main execution for advanced workflow"""
    
    # Initialize advanced workflow
    workflow = AdvancedAdWorkflow(output_dir="ad_script_outputs")
    
    # Topics to process
    topics = [
        "Skincare",
        "Fitness",
        "E-commerce"
    ]
    
    # Generate batch
    results = workflow.generate_batch(topics, scripts_per_topic=3)
    
    # Flatten all scripts
    all_scripts = []
    for topic_scripts in results.values():
        all_scripts.extend(topic_scripts)
    
    # Export in multiple formats
    print("\n💾 Exporting Results...")
    workflow.export_to_json(all_scripts)
    workflow.export_to_csv(all_scripts)
    workflow.export_to_markdown(all_scripts)
    workflow.export_to_html(all_scripts)
    
    # Display analytics
    workflow.print_analytics()
    
    print("✅ Workflow completed! Check 'ad_script_outputs' folder for results.")


if __name__ == "__main__":
    main()