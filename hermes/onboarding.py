import os
import sys
import time
from pathlib import Path

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.live import Live
    from rich.layout import Layout
    from rich.align import Align
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


HERMES_ASCII = """
██╗  ██╗███████╗██████╗ ███╗   ███╗███████╗███████╗
██║  ██║██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝
███████║█████╗  ██████╔╝██╔████╔██║█████╗  ███████╗
██╔══██║██╔══╝  ██╔══██╗██║╚██╔╝██║██╔══╝  ╚════██║
██║  ██║███████╗██║  ██║██║ ╚═╝ ██║███████╗███████║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝
"""

WELCOME_TEXT = """[bold #FF950A]Hermes thinks through you![/bold #FF950A]

Your cultural syntax → Python

[dim]"Code in your language, your references, your worldview"[/dim]"""

SANGAM_EXAMPLE = """[yellow]scheme[/yellow] greet(name):
    [yellow]announce[/yellow]("Hello, " + name + "!")
    [yellow]abandon[/yellow] [cyan]truth[/cyan]

[yellow]fortify[/yellow] Person:
    [yellow]scheme initialize[/yellow]([magenta]myself[/magenta], name, age):
        [magenta]myself[/magenta].name = name
        [magenta]myself[/magenta].age = age
"""

PHILOSOPHY = """[bold]The Philosophy[/bold]

Why [cyan]scheme[/cyan] instead of [dim]def[/dim]?
  → Because a function is a [bold]scheme[/bold], a plan!

Why [cyan]abandon[/cyan] instead of [dim]return[/dim]?
  → Because you [bold]abandon[/bold] the flow, give up control!

Why [cyan]myself[/cyan] instead of [dim]self[/dim]?
  → Because [bold]myself[/bold] is personal, human!
"""

PYTHON_COMPARISON = """[bold green]Hermes[/bold green]           →    [bold blue]Python[/bold blue]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
scheme             →    def
abandon            →    return
fortify            →    class
myself             →    self
announce           →    print
aahaan             →    if
cascade            →    elif
thats_it           →    else
iterate            →    for
truth              →    True
falsehood          →    False
nothing            →    None
"""


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_onboarding_rich():
    console = Console()
    
    clear_screen()
    
    console.print(Align.center(HERMES_ASCII), style="bold #FF950A")
    time.sleep(0.5)
    
    console.print()
    console.print(Align.center("[bold #FF950A]Hermes thinks through you![/bold #FF950A]"))
    console.print()
    console.print(Align.center("Your cultural syntax → Python"))
    console.print()
    console.print(Align.center('[dim]"Code in your language, your references, your worldview"[/dim]'))
    console.print()
    console.print(Align.center("[dim]Press Enter to begin your journey...[/dim]"))
    input()
    
    clear_screen()
    console.print(Panel.fit(
        "[bold]Step 1: The Sangam Skin[/bold]\n\n"
        + SANGAM_EXAMPLE + "\n\n"
        + "[dim]This is the default skin inspired by Tamil cinema.[/dim]",
        border_style="#FF950A",
        title="🎬 Cultural Syntax"
    ))
    
    console.input("\n[dim]Press Enter to continue...[/dim]")
    
    clear_screen()
    console.print(Panel.fit(
        PHILOSOPHY,
        border_style="yellow",
        title="💭 Why This Matters"
    ))
    
    console.input("\n[dim]Press Enter to continue...[/dim]")
    
    clear_screen()
    console.print(Panel.fit(
        PYTHON_COMPARISON,
        border_style="green",
        title="🔄 The Translation"
    ))
    
    console.input("\n[dim]Press Enter to continue...[/dim]")
    
    clear_screen()
    
    console.print("[bold #FF950A]Let's run your first Hermes program![/bold #FF950A]\n")
    
    example_code = """scheme greet(name):
    announce("Hello, " + name)
    abandon truth

greet("World")"""
    
    console.print(Panel(example_code, border_style="#FF950A", title="hello.herm"))
    console.print()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[#FF950A]Transpiling...", total=None)
        time.sleep(0.8)
        progress.update(task, completed=True)
    
    console.print("\n[bold green]Output:[/bold green]")
    console.print("[dim]Hello, World[/dim]")
    console.print()
    
    console.input("[dim]Press Enter to finish setup...[/dim]")
    
    clear_screen()
    
    console.print(Panel.fit(
        "[bold green]✓ You're all set![/bold green]\n\n"
        + "Quick Start:\n"
        + "  [#FF950A]hermes run hello.herm[/#FF950A]     → Run a file\n"
        + "  [#FF950A]hermes compile file.herm[/#FF950A]  → Transpile to Python\n"
        + "  [#FF950A]hermes check file.herm[/#FF950A]    → Syntax validation\n\n"
        + "Learn more:\n"
        + "  → [link]https://github.com/Pilan-AI/hermes-lang[/link]\n"
        + "  → [link]https://pilan.ai[/link]\n\n"
        + "[dim italic]\"Code in your culture. Hermes translates.\"[/dim italic]",
        border_style="green",
        title="🚀 Welcome to Hermes"
    ))
    
    console.print()
    
    create_sample_project(console)


def show_onboarding_plain():
    clear_screen()
    
    print(HERMES_ASCII)
    time.sleep(0.5)
    
    print("\n" + "="*60)
    print("Hermes thinks through you!")
    print("Your cultural syntax → Python")
    print("="*60 + "\n")
    
    input("Press Enter to begin your journey...")
    
    clear_screen()
    
    print("\n" + "="*60)
    print("Step 1: The Sangam Skin")
    print("="*60)
    print("""
scheme greet(name):
    announce("Hello, " + name + "!")
    abandon truth

fortify Person:
    scheme initialize(myself, name, age):
        myself.name = name
        myself.age = age
""")
    print("This is the default skin inspired by Tamil cinema.")
    
    input("\nPress Enter to continue...")
    
    clear_screen()
    
    print("\n" + "="*60)
    print("The Philosophy")
    print("="*60)
    print("""
Why 'scheme' instead of 'def'?
  → Because a function is a scheme, a plan!

Why 'abandon' instead of 'return'?
  → Because you abandon the flow, give up control!

Why 'myself' instead of 'self'?
  → Because myself is personal, human!
""")
    
    input("\nPress Enter to continue...")
    
    clear_screen()
    
    print("\n" + "="*60)
    print("The Translation")
    print("="*60)
    print("""
Hermes          →    Python
━━━━━━━━━━━━━━━━━━━━━━━━━━━
scheme          →    def
abandon         →    return
fortify         →    class
myself          →    self
announce        →    print
aahaan          →    if
cascade         →    elif
thats_it        →    else
iterate         →    for
truth           →    True
falsehood       →    False
nothing         →    None
""")
    
    input("\nPress Enter to continue...")
    
    clear_screen()
    
    print("\n" + "="*60)
    print("Your First Hermes Program")
    print("="*60)
    print("""
scheme greet(name):
    announce("Hello, " + name)
    abandon truth

greet("World")
""")
    print("\nTranspiling... Done!")
    print("\nOutput:")
    print("Hello, World")
    print()
    
    input("Press Enter to finish setup...")
    
    clear_screen()
    
    print("\n" + "="*60)
    print("✓ You're all set!")
    print("="*60)
    print("""
Quick Start:
  hermes run hello.herm      → Run a file
  hermes compile file.herm   → Transpile to Python
  hermes check file.herm     → Syntax validation

Learn more:
  → https://github.com/Pilan-AI/hermes-lang
  → https://pilan.ai

"Code in your culture. Hermes translates."
""")
    
    create_sample_project_plain()


def create_sample_project(console):
    home = Path.home()
    hermes_dir = home / ".hermes"
    examples_dir = hermes_dir / "examples"
    
    hermes_dir.mkdir(exist_ok=True)
    examples_dir.mkdir(exist_ok=True)
    
    config_file = hermes_dir / "config.json"
    if not config_file.exists():
        config_file.write_text('{"onboarding_completed": true, "version": "0.1.0"}')
    
    hello_file = examples_dir / "hello.herm"
    hello_file.write_text("""scheme greet(name):
    announce("Hello, " + name + "!")
    abandon truth

scheme main():
    result = greet("World")
    aahaan result:
        announce("Greeting successful!")
    thats_it:
        announce("Something went wrong")

main()
""")
    
    console.print(f"[green]✓[/green] Created sample project at [cyan]{examples_dir}[/cyan]")
    console.print(f"\nTry it: [yellow]hermes run {hello_file}[/yellow]")


def create_sample_project_plain():
    home = Path.home()
    hermes_dir = home / ".hermes"
    examples_dir = hermes_dir / "examples"
    
    hermes_dir.mkdir(exist_ok=True)
    examples_dir.mkdir(exist_ok=True)
    
    config_file = hermes_dir / "config.json"
    if not config_file.exists():
        config_file.write_text('{"onboarding_completed": true, "version": "0.1.0"}')
    
    hello_file = examples_dir / "hello.herm"
    hello_file.write_text("""scheme greet(name):
    announce("Hello, " + name + "!")
    abandon truth

scheme main():
    result = greet("World")
    aahaan result:
        announce("Greeting successful!")
    thats_it:
        announce("Something went wrong")

main()
""")
    
    print(f"✓ Created sample project at {examples_dir}")
    print(f"\nTry it: hermes run {hello_file}")


def is_first_run():
    config_file = Path.home() / ".hermes" / "config.json"
    return not config_file.exists()


def run_onboarding():
    if RICH_AVAILABLE:
        show_onboarding_rich()
    else:
        show_onboarding_plain()
