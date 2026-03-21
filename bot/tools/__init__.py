"""Tools for autochecker."""

TOOLS = [
    {
        "name": "get_items",
        "description": "Get all items",
        "parameters": []
    },
    {
        "name": "get_learners",
        "description": "Get all learners",
        "parameters": []
    },
    {
        "name": "get_groups",
        "description": "Get student groups",
        "parameters": []
    },
    {
        "name": "get_pass_rates",
        "description": "Get pass rates for a lab",
        "parameters": ["lab"]
    },
    {
        "name": "get_timeline",
        "description": "Get submission timeline",
        "parameters": []
    },
    {
        "name": "sync_data",
        "description": "Sync data from autochecker",
        "parameters": []
    },
    {
        "name": "get_labs",
        "description": "List all labs",
        "parameters": []
    },
    {
        "name": "get_scores",
        "description": "Get scores for a lab",
        "parameters": ["lab"]
    },
    {
        "name": "get_health",
        "description": "Check backend health",
        "parameters": []
    },
]

BUTTONS = [
    {"text": "📚 Labs", "command": "/labs"},
    {"text": "📊 Scores", "command": "/scores lab-04"},
    {"text": "👥 Learners", "command": "/learners"},
    {"text": "🔄 Sync", "command": "/sync"},
    {"text": "📈 Pass Rates", "command": "/pass-rates lab-04"},
    {"text": "📅 Timeline", "command": "/timeline"},
    {"text": "🏆 Groups", "command": "/groups"},
]
