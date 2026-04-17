def example_basic_usage():
    """Example 1: Basic usage - generate scripts for one topic"""
    print("=" * 80)
    print("EXAMPLE 1: Basic Usage".center(80))
    print("=" * 80)
    
    from ad_script_generator import AdScriptGenerator
    
    # Initialize the generator
    generator = AdScriptGenerator()
    
    # Step 1: Get viral hooks for skincare
    print("\n Fetching viral hooks for Skincare topic...")
    hooks_data = generator.get_viral_hooks("Skincare")
    print(f"Found {len(hooks_data['hooks'])} trending hooks:")
    for i, hook in enumerate(hooks_data['hooks'], 1):
        print(f"  {i}. {hook['hook']} (Platform: {hook['platform']})")
    
    # Step 2: Generate ad scripts
    print("\n Generating ad scripts...")
    scripts = generator.create_workflow("Skincare", num_scripts=3)
    
    # Step 3: Display results
    generator.display_scripts(scripts)
    
    # Step 4: Save to JSON
    import json
    from datetime import datetime
    
    filename = f"example_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(scripts, f, indent=2)
    
    print(f"\n✓ Results saved to {filename}")
    return scripts


def example_batch_processing():
    """Example 2: Batch processing - generate for multiple topics"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Batch Processing Multiple Topics".center(80))
    print("=" * 80)
    
    from advanced_workflow import AdvancedAdWorkflow
    
    # Initialize workflow
    workflow = AdvancedAdWorkflow(output_dir="example_outputs")
    
    # Generate scripts for multiple topics
    topics = ["Skincare", "Fitness"]  # Using fewer topics for demo
    print(f"\nProcessing {len(topics)} topics...")
    
    results = workflow.generate_batch(topics, scripts_per_topic=2)
    
    # Flatten results
    all_scripts = []
    for topic_scripts in results.values():
        all_scripts.extend(topic_scripts)
    
    # Export to multiple formats
    print("\n Exporting to multiple formats...")
    workflow.export_to_json(all_scripts, "example_batch.json")
    workflow.export_to_csv(all_scripts, "example_batch.csv")
    workflow.export_to_markdown(all_scripts, "example_batch.md")
    workflow.export_to_html(all_scripts, "example_batch.html")
    
    # Show analytics
    workflow.print_analytics()


def example_custom_topic():
    """Example 3: Custom topic with manual hooks"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Custom Topic with Manual Hooks".center(80))
    print("=" * 80)
    
    from ad_script_generator import AdScriptGenerator
    
    generator = AdScriptGenerator()
    
    # Define custom topic and hooks
    custom_topic = "Fitness App"
    custom_hooks = [
        "This 5-minute workout changed my body completely",
        "Gyms hate this one app",
        "I lost 30 pounds without the gym"
    ]
    
    print(f"\nGenerating scripts for custom topic: {custom_topic}")
    print(f"Using {len(custom_hooks)} custom hooks\n")
    
    scripts = []
    for i, hook in enumerate(custom_hooks, 1):
        print(f"Generating script {i}/{len(custom_hooks)}...")
        script = generator.generate_ad_script(custom_topic, hook)
        script["date"] = __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        script["topic"] = custom_topic
        scripts.append(script)
    
    # Display results
    generator.display_scripts(scripts)
    
    return scripts


def example_single_script():
    """Example 4: Generate a single script with detailed output"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Single Script Generation with Details".center(80))
    print("=" * 80)
    
    from ad_script_generator import AdScriptGenerator
    
    generator = AdScriptGenerator()
    
    topic = "Skincare"
    hook = "POV: Your dermatologist hates this one simple trick"
    
    print(f"\nTopic: {topic}")
    print(f"Hook: {hook}\n")
    print("Generating script...")
    
    script = generator.generate_ad_script(topic, hook)
    
    # Pretty print the result
    print("\n" + "─" * 80)
    print(f"{'GENERATED SCRIPT'.center(80)}")
    print("─" * 80)
    
    print(f"\n Hook:\n   {script.get('hook', 'N/A')}\n")
    print(f"  Problem:\n   {script.get('problem_statement', 'N/A')}\n")
    print(f" Solution:\n   {script.get('solution', 'N/A')}\n")
    print(f" CTA:\n   {script.get('cta', 'N/A')}\n")
    print(f"  Full Script:\n")
    
    script_text = script.get('full_script', 'N/A')
    for line in script_text.split('\n'):
        print(f"   {line}")
    
    print(f"\n Platform: {script.get('platform', 'N/A')}")
    print(f"  Duration: {script.get('estimated_duration', 'N/A')}")


def show_menu():
    """Display menu of examples"""
    print("\n" + "=" * 80)
    print(" AD SCRIPT GENERATOR - EXAMPLE USAGE MENU".center(80))
    print("=" * 80)
    print("""
1. Basic Usage - Generate scripts for one topic (Skincare)
2. Batch Processing - Generate for multiple topics
3. Custom Topic - Use your own hooks
4. Single Script - See detailed output for one script
5. Exit

Choose an example to run (1-5):
    """)


def main():
    """Main menu-driven example runner"""
    import sys
    
    try:
        while True:
            show_menu()
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                example_basic_usage()
                input("\nPress Enter to continue...")
            
            elif choice == '2':
                example_batch_processing()
                input("\nPress Enter to continue...")
            
            elif choice == '3':
                example_custom_topic()
                input("\nPress Enter to continue...")
            
            elif choice == '4':
                example_single_script()
                input("\nPress Enter to continue...")
            
            elif choice == '5':
                print("\n Goodbye!")
                sys.exit(0)
            
            else:
                print("\n Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\n\n Interrupted by user. Goodbye!")
        sys.exit(0)
    
    except ImportError as e:
        print(f"\n Import Error: {e}")
        print("\nMake sure you have installed all dependencies:")
        print("  pip install -r requirements.txt")
    
    except Exception as e:
        print(f"\n Error: {e}")
        print("\nMake sure you have:")
        print("  1. Set ANTHROPIC_API_KEY in .env file")
        print("  2. Installed all requirements: pip install -r requirements.txt")


if __name__ == "__main__":
    main()
