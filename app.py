from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Home page with instructions"""
    return render_template('index.html')

@app.route('/<username>/<repo>')
def analyze_repo(username, repo):
    """
    Main route for analyzing GitHub repositories
    Pattern: epistemicme.ai/username/repo
    """
    try:
        # Validate input
        if not username or not repo:
            return render_template('error.html', 
                                 error="Invalid repository format",
                                 message="Please use format: username/repo"), 400
        
        # Log the analysis request
        logger.info(f"Analyzing repository: {username}/{repo}")
        
        # For now, return the analysis template with placeholder data
        analysis_data = {
            'username': username,
            'repo': repo,
            'timestamp': datetime.now().isoformat(),
            'status': 'scanning'
        }
        
        return render_template('analysis.html', **analysis_data)
        
    except Exception as e:
        logger.error(f"Error analyzing {username}/{repo}: {str(e)}")
        return render_template('error.html', 
                             error="Analysis failed",
                             message=f"Could not analyze {username}/{repo}"), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """Custom 404 page"""
    return render_template('error.html', 
                         error="Repository not found",
                         message="Please check the username and repository name"), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 page"""
    return render_template('error.html', 
                         error="Internal server error",
                         message="Something went wrong on our end"), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting ContextBuilder on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)