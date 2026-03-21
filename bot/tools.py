TOOLS = [
    {"name": "get_items", "description": "Get all items"},
    {"name": "get_learners", "description": "Get all learners"},
    {"name": "get_groups", "description": "Get student groups"},
    {"name": "get_pass_rates", "description": "Get pass rates for a lab"},
    {"name": "get_timeline", "description": "Get submission timeline"},
    {"name": "sync_data", "description": "Sync data from autochecker"},
    {"name": "get_labs", "description": "List all labs"},
    {"name": "get_scores", "description": "Get scores for a lab"},
    {"name": "get_health", "description": "Check backend health"},
]

BUTTONS = [
    [{"text": "📚 Labs", "callback_data": "/labs"}],
    [{"text": "📊 Scores", "callback_data": "/scores lab-04"}],
    [{"text": "👥 Learners", "callback_data": "/learners"}],
    [{"text": "🔄 Sync", "callback_data": "/sync"}],
    [{"text": "📈 Pass Rates", "callback_data": "/pass-rates"}],
    [{"text": "📅 Timeline", "callback_data": "/timeline"}],
    [{"text": "🏆 Groups", "callback_data": "/groups"}],
]
