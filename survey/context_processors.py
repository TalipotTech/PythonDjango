"""
Context processor to add database information to admin templates
"""
from django.conf import settings

def database_info(request):
    """
    Add database connection information to template context
    """
    db_config = settings.DATABASES.get('default', {})
    db_engine = db_config.get('ENGINE', '')
    
    # Determine database type and details
    if 'postgresql' in db_engine:
        db_type = 'PostgreSQL'
        db_host = db_config.get('HOST', 'Unknown')
        db_name = db_config.get('NAME', 'Unknown')
        
        # Check if it's Azure
        if 'azure' in db_host.lower() or 'postgres.database.azure.com' in db_host.lower():
            environment = 'PRODUCTION'
            location = 'Azure Cloud'
            color = 'success'  # Green
            icon = '☁️'
        else:
            environment = 'DEVELOPMENT'
            location = 'Remote Server'
            color = 'info'  # Blue
            icon = '🌐'
            
        db_info = {
            'type': db_type,
            'host': db_host,
            'name': db_name,
            'environment': environment,
            'location': location,
            'color': color,
            'icon': icon,
            'is_cloud': 'azure' in db_host.lower()
        }
    else:
        # SQLite (local database)
        db_info = {
            'type': 'SQLite',
            'host': 'Local File',
            'name': db_config.get('NAME', 'db.sqlite3'),
            'environment': 'DEVELOPMENT',
            'location': 'Local Machine',
            'color': 'warning',  # Yellow/Orange
            'icon': '💾',
            'is_cloud': False
        }
    
    return {
        'database_info': db_info
    }
