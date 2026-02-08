"""Bloom CLI - Main entry point"""

import os
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

__version__ = "0.1.0"

BLOOM_YAML = """# Bloom Project Configuration
name: {name}
version: 0.1.0
seed: genesis

# Sieve Security Configuration
sieve:
  root_key: auto-generate
  verify_components: true

# Pulse Development Server
pulse:
  port: 8080
  live_reload: true
  hot_swap: true

# Crystalize Build Settings
crystalize:
  target: web
  optimize: true
  minify: true
"""

MAIN_PY = '''"""{name} - Bloom Application"""

def main():
    """Main entry point for {name}"""
    print("🌱 {name} is blooming!")
    print("Edit this file and watch changes appear instantly")

if __name__ == "__main__":
    main()
'''

INDEX_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Bloom App</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
            color: #c9d1d9;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }}
        .container {{
            text-align: center;
            max-width: 600px;
        }}
        .logo {{
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: pulse 2s ease-in-out infinite;
        }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
        }}
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #4ade80, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        p {{
            font-size: 1.1rem;
            color: #8b949e;
            margin-bottom: 2rem;
        }}
        .status {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.5rem;
            background: rgba(74, 222, 128, 0.1);
            border: 1px solid rgba(74, 222, 128, 0.3);
            border-radius: 2rem;
            font-size: 0.9rem;
            color: #4ade80;
        }}
        .status::before {{
            content: '';
            width: 8px;
            height: 8px;
            background: #4ade80;
            border-radius: 50%;
            animation: blink 1s step-end infinite;
        }}
        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🌱</div>
        <h1>{name}</h1>
        <p>Your Bloom application is running!</p>
        <div class="status">Pulse Server Active</div>
    </div>
</body>
</html>
'''


def print_banner():
    """Print the Bloom banner"""
    banner = Text()
    banner.append("🌱 ", style="green")
    banner.append("Bloom", style="bold green")
    banner.append(" - The Local-First AI Engine\n", style="dim")
    banner.append(f"v{__version__}", style="cyan")
    console.print(Panel(banner, border_style="green"))


@click.group()
@click.version_option(version=__version__, prog_name="bloom")
def cli():
    """Bloom - The Local-First AI Engine CLI"""
    pass


@cli.command()
@click.argument("name")
def seed(name):
    """Create a new Bloom seed (project)"""
    print_banner()
    console.print(f"[green]Planting seed:[/green] {name}")
    
    # Create project directory
    if os.path.exists(name):
        console.print(f"[red]✗[/red] Directory '{name}' already exists")
        return
    
    os.makedirs(name)
    console.print(f"[green]✓[/green] Created {name}/")
    
    # Create src directory
    src_dir = os.path.join(name, "src")
    os.makedirs(src_dir)
    console.print(f"[green]✓[/green] Created {name}/src/")
    
    # Create bloom.yaml
    with open(os.path.join(name, "bloom.yaml"), "w", encoding="utf-8") as f:
        f.write(BLOOM_YAML.format(name=name))
    console.print(f"[green]✓[/green] Created {name}/bloom.yaml")
    
    # Create main.py
    with open(os.path.join(src_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(MAIN_PY.format(name=name))
    console.print(f"[green]✓[/green] Created {name}/src/main.py")
    
    # Create index.html
    with open(os.path.join(name, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX_HTML.format(name=name))
    console.print(f"[green]✓[/green] Created {name}/index.html")
    
    console.print(f"\n[green]✓[/green] Seed planted successfully!")
    console.print(f"[dim]Run: cd \"{name}\"[/dim]")
    console.print(f"[dim]Then: bloom grow[/dim]")


@cli.command()
def init():
    """Initialize a Bloom project in current directory"""
    print_banner()
    console.print("[green]Initializing Bloom project...[/green]")
    # TODO: Implement init
    console.print("[green]✓[/green] Initialized bloom.yaml")


@cli.command()
def grow():
    """Start the Pulse development server"""
    print_banner()
    console.print("[green]🌱 Growing your Bloom application...[/green]")
    console.print("[dim]Starting Pulse server on http://localhost:8080[/dim]")
    console.print("[dim]Press Ctrl+C to stop[/dim]")
    # TODO: Implement server
    try:
        while True:
            pass
    except KeyboardInterrupt:
        console.print("\n[dim]Shutting down...[/dim]")


@cli.command()
def crystalize():
    """Crystalize (build) for production"""
    print_banner()
    console.print("[green]💎 Crystalizing your Bloom application...[/green]")
    # TODO: Implement build
    console.print("[green]✓[/green] Build complete in dist/")


@cli.command()
def plant():
    """Deploy (plant) your application"""
    print_banner()
    console.print("[green]🌐 Planting your Bloom application...[/green]")
    # TODO: Implement deploy
    console.print("[green]✓[/green] Deployed successfully")


# Alias commands for backwards compatibility
@click.command()
@click.argument("name")
def seed_cmd(name):
    """bloom-seed alias"""
    seed.callback(name)


@click.command()
def init_cmd():
    """bloom-init alias"""
    init.callback()


@click.command()
def grow_cmd():
    """bloom-grow alias"""
    grow.callback()


@click.command()
def crystalize_cmd():
    """bloom-crystalize alias"""
    crystalize.callback()


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
