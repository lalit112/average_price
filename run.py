"""
Module where the application gets started
"""

from application.app import create_app
app = create_app()
app.run(debug=True)
