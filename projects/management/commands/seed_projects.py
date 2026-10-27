"""Load the initial collection without overwriting later admin edits."""
from django.core.management.base import BaseCommand
from django.db import transaction
from projects.models import Project, Screenshot

PROJECTS = [
    {
        "title": "Dungeon Descent", "slug": "dungeon-descent", "sort_order": 1,
        "summary": "A dungeon crawler about finding your way down. Fight through rooms, collect upgrades, and take on a changing lineup of bosses.",
        "category": "game", "status": "Playable prototype", "technologies": "Python, Pygame",
        "description": "Dungeon Descent is a top-down dungeon game built with Python and Pygame. Explore connected rooms, find the key, build up your abilities, and descend to the next floor.\n\nThe current source supports five floors. Four boss encounters shuffle across the first four floors, while later areas introduce pits, destructible cover, and paired elite enemies. A separate practice mode lets players jump straight into a boss encounter.",
        "works_today": "Five floors of connected rooms and exploration\nFour shuffled boss encounters\nWeapon upgrades, dashing, and unlockable blocking\nAn explored-floor map and a separate boss practice mode",
        "next_steps": "Quality-of-life improvements and further playtesting\nDesign and implement the fifth floor's final boss",
        "limitations": "The fifth floor's final chamber currently displays a completion message. The game is still being balanced and developed.",
        "source_url": "https://github.com/snehardt/Personal-Project",
        "download_url": "",
        "controls": "WASD to move · Left mouse to shoot · Space to dash · Shift or right mouse to block when unlocked · E to interact · M for the map · Escape to pause",
        "run_instructions": "Install Python 3.11 or newer, download the source, and open a terminal in the game folder.\npython -m pip install -r requirements.txt\npython dungeon.py\nFor boss practice: python playtest_bosses.py",
    },
    {
        "title": "Hazardous Lies", "slug": "hazardous-lies", "sort_order": 2,
        "summary": "A multiplayer golf platformer where players jump through obstacles and race to get their ball into the hole.",
        "category": "game", "status": "Playable prototype", "technologies": "TypeScript, JavaScript, WebSockets, Cloudflare",
        "description": "",
        "works_today": "A playable prototype with the core gameplay in place\n10 levels\nLocal and online multiplayer",
        "next_steps": "Add more levels\nFix bugs in collision handling and magnet mechanics\nImprove online connections between computers",
        "limitations": "",
        "contribution": "I designed and developed Hazardous Lies independently, including the gameplay, levels, and multiplayer systems.",
        "source_url": "https://github.com/snehardt/Hazardous-Lies",
        "demo_url": "https://hazardous-lies-relay.spencer-ehardt.workers.dev",
        "controls": "",
    },
    {
        "title": "Blockwood", "slug": "blockwood", "sort_order": 3,
        "summary": "A Minecraft-inspired browser game built quickly with AI coding agents, using prompts to turn the idea into a playable world.",
        "category": "game", "status": "Finished", "technologies": "JavaScript, Three.js, WebGL",
        "description": "",
        "works_today": "A complete, playable browser game set in a small block world\nExplore, mine resources, and build\nZombie combat and survival mechanics",
        "next_steps": "No further development is currently planned\nPossible bug fixes or a larger world in a future update",
        "limitations": "",
        "contribution": "I directed AI coding agents through prompt engineering to build the game and its features in less than 30 minutes.",
        "source_url": "https://github.com/snehardt/blockwood",
        "demo_url": "https://snehardt.github.io/blockwood/", "demo_label": "Open in browser",
        "controls": "",
        "run_instructions": "",
    },
    {
        "title": "Parachute", "slug": "parachute", "sort_order": 4,
        "summary": "A peer-to-peer web app designed to make sharing files and folders easy, without links or logins.",
        "category": "web", "status": "Interactive prototype", "technologies": "HTML, CSS, JavaScript, PeerJS, WebRTC, Node.js",
        "description": "",
        "works_today": "Connect two browsers using unique page IDs\nSend animated packages in both directions with delivery confirmations\nChoose package artwork and interact with falling parachutes\nDisconnect, reconnect, and retry connections\nAnimation sharing is working; file and folder transfers are still in development",
        "next_steps": "Implement file and folder transfers\nAdd saving for received files\nImprove connection reliability across different networks",
        "limitations": "",
        "contribution": "Built with Michael Becker, Sam Pickett, and Conner Madsen. I built the peer-to-peer connection system and the entire front end, including the animations and interactive visuals. I am continuing to develop these features as the project grows.",
        "source_url": "https://github.com/21beckem/parachute",
        "demo_url": "https://21beckem.github.io/parachute/index.html", "demo_label": "Open in browser",
        "controls": "",
        "run_instructions": "",
    },
    {
        "title": "Snake", "slug": "snake", "sort_order": 5,
        "summary": "A classic Snake game built to practice Python and learn Pygame. Collect apples, grow longer, and avoid the walls and your own tail.",
        "category": "game", "status": "Completed for now", "technologies": "Python, Pygame",
        "description": "",
        "works_today": "Complete Snake gameplay with scoring and replay controls\nAdjustable board size and speed for different difficulty levels\nBackground music",
        "next_steps": "No updates currently planned\nAdditional game modes are a possibility, but nothing is confirmed",
        "limitations": "",
        "contribution": "I built this game independently to practice Python and learn Pygame, including the gameplay, difficulty settings, and background music.",
        "source_url": "https://github.com/snehardt/Snake_Game",
        "download_url": "",
        "controls": "",
        "run_instructions": "Install Python and open a terminal in the project folder.\npython -m pip install pygame==2.6.1\npython main.py",
    },
]

class Command(BaseCommand):
    help = "Add the five initial projects; keep existing project edits intact."

    @transaction.atomic
    def handle(self, *args, **options):
        for data in PROJECTS:
            project, created = Project.objects.get_or_create(slug=data["slug"], defaults=data)
            self.stdout.write(f'{"Added" if created else "Kept"}: {project.title}')
        for slug, asset, caption in [
            ("dungeon-descent", "dungeon-bosses.png", "Boss encounter preview from the development build."),
            ("dungeon-descent", "dungeon-map.png", "The explored-floor map in a development preview."),
            ("blockwood", "blockwood.png", "Blockwood browser verification capture from the local project."),
            ("parachute", "parachute.png", "The current Parachute interface running locally."),
            ("hazardous-lies", "hazardous-lies.png", "Hazardous Lies running locally in the browser."),
            ("snake", "snake.png", "Snake's board rendered with the project's Pygame drawing code."),
        ]:
            Screenshot.objects.get_or_create(project=Project.objects.get(slug=slug), asset=f"projects/images/{asset}", defaults={"caption": caption})
