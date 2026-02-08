import sys
import time
import os
import subprocess
import json
import hashlib
import requests
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import init, Fore, Style
from datetime import datetime

# Initialize colorama for Windows support
init()

class BloomWatcher(FileSystemEventHandler):
    def __init__(self, project_root):
        self.project_root = project_root
        self.cli_path = os.path.join(project_root, "cli", "sprout.py")
        self.cache_dir = os.path.join(project_root, ".bloom", "brain_cache")
        os.makedirs(self.cache_dir, exist_ok=True)

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.bloom'):
            self.trigger_sprout()

    def trigger_sprout(self):
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Fore.GREEN}{Style.BRIGHT}[SEED] Seed is growing... [{timestamp}]{Style.RESET_ALL}")
        
        # Process AI hints before compiling
        self.process_ai_hints()
        
        try:
            # Run the sprout compiler
            result = subprocess.run([sys.executable, self.cli_path], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(result.stdout)
                print(f"{Fore.CYAN}{Style.BRIGHT}[SUCCESS] Bloom refreshed!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[ERROR] Compiler Error:{Style.RESET_ALL}")
                print(result.stderr)
        except Exception as e:
            print(f"{Fore.RED}[ERROR] Error running sprout: {e}{Style.RESET_ALL}")

    def process_ai_hints(self):
        """Process AI hints in Bloom markup and generate content."""
        bloom_file = os.path.join(self.project_root, "src", "index.bloom")
        
        if not os.path.exists(bloom_file):
            return
        
        try:
            with open(bloom_file, 'r') as f:
                content = f.read()
            
            # Look for elements with hint="ai" attribute
            import re
            ai_hints = re.findall(r'<(\w+)[^>]*hint="ai"[^>]*>(.*?)</\1>', content, re.DOTALL)
            
            if ai_hints:
                print(f"{Fore.MAGENTA}[BRAIN] Processing {len(ai_hints)} AI hint(s)...{Style.RESET_ALL}")
                
                for tag, inner_content in ai_hints:
                    # Generate prompt based on tag and context
                    prompt = self.generate_ai_prompt(tag, inner_content)
                    ai_response = self.ask_brain(prompt)
                    
                    if ai_response:
                        # Cache the response
                        cache_key = hashlib.md5(prompt.encode()).hexdigest()
                        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
                        
                        with open(cache_file, 'w') as f:
                            json.dump({
                                'prompt': prompt,
                                'response': ai_response,
                                'timestamp': time.time()
                            }, f, indent=2)
                        
                        # Update the bloom file with AI-generated content
                        self.update_bloom_with_ai(content, ai_response)
                        break  # Process one hint at a time for now
                        
        except Exception as e:
            print(f"{Fore.RED}[ERROR] AI processing failed: {e}{Style.RESET_ALL}")

    def generate_ai_prompt(self, tag, content):
        """Generate AI prompt based on tag and content."""
        base_prompts = {
            'button': f"Create a modern, accessible button design with the text '{content.strip()}'. Suggest improvements for UX and visual appeal.",
            'text': f"Generate compelling text content for: {content.strip()}. Make it engaging and user-friendly.",
            'container': f"Design a responsive container layout for: {content.strip()}. Include modern CSS grid/flexbox suggestions.",
            'card': f"Create a beautiful card component for: {content.strip()}. Suggest styling, animations, and interactions.",
        }
        
        return base_prompts.get(tag, f"Generate creative content for {tag} element: {content.strip()}")

    def ask_brain(self, prompt):
        """Query local AI models (Ollama, WebLLM, etc.)."""
        # Try Ollama first (most common local AI)
        try:
            response = requests.post('http://localhost:11434/api/generate', 
                                   json={
                                       'model': 'llama3.2:3b',
                                       'prompt': prompt,
                                       'stream': False
                                   }, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
                
        except requests.exceptions.RequestException:
            pass
        
        # Fallback: Try WebLLM or other local AI services
        # For now, return a mock response if no local AI is available
        print(f"{Fore.YELLOW}[BRAIN] Local AI not detected. Using fallback suggestions.{Style.RESET_ALL}")
        
        # Simple fallback responses based on prompt keywords
        if 'button' in prompt.lower():
            return "Modern gradient button with hover effects and accessibility features"
        elif 'text' in prompt.lower():
            return "Welcome to the future of app development with Bloom!"
        elif 'card' in prompt.lower():
            return "Elegant card with glass morphism effect and smooth animations"
        else:
            return "AI-generated content placeholder"

    def update_bloom_with_ai(self, content, ai_response):
        """Update Bloom file with AI-generated content."""
        bloom_file = os.path.join(self.project_root, "src", "index.bloom")
        
        # Simple replacement: replace first hint="ai" with AI response
        updated_content = content.replace('hint="ai"', 'ai-generated="true"', 1)
        
        # Add AI response as content
        # This is a simplified approach - in production you'd parse and update specific elements
        with open(bloom_file, 'w') as f:
            f.write(updated_content)

def main():
    if len(sys.argv) < 2 or sys.argv[1] != "--growing":
        print(f"{Fore.YELLOW}Bloom Dev Server{Style.RESET_ALL}")
        print("Usage: python cli/seed.py --growing")
        print("\nFlags:")
        print("  --growing    Watch src/ for changes and auto-compile")
        print("\nAI Features:")
        print("  hint=\"ai\"    Add to any element for AI-generated content")
        print("  Local AI      Uses Ollama (recommended) or fallback suggestions")
        print("  Caching       AI responses cached in .bloom/brain_cache/")
        return

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_path = os.path.join(project_root, "src")
    
    # Initial compile
    event_handler = BloomWatcher(project_root)
    event_handler.trigger_sprout()

    observer = Observer()
    observer.schedule(event_handler, src_path, recursive=False)
    observer.start()

    print(f"{Fore.CYAN}Watching for changes in {src_path}...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Press Ctrl+C to stop{Style.RESET_ALL}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print(f"\n{Fore.YELLOW}Stopping Bloom Dev Server...{Style.RESET_ALL}")
    
    observer.join()

if __name__ == "__main__":
    main()
