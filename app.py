from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime
import logging
from github_client import GitHubClient
from epistemic_client import EpistemicClient
from belief_extractor import BeliefExtractor

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
github_client = GitHubClient()
epistemic_client = EpistemicClient()
belief_extractor = BeliefExtractor()

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
        
        # Return the analysis template - actual analysis happens via AJAX
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

@app.route('/api/analyze/<username>/<repo>')
def api_analyze_repo(username, repo):
    """
    API endpoint for real-time repository analysis
    """
    try:
        # Validate input
        if not username or not repo:
            return jsonify({'error': 'Invalid repository format'}), 400
        
        logger.info(f"API: Analyzing repository: {username}/{repo}")
        
        # Fetch GitHub data
        github_data = github_client.get_repository_data(username, repo)
        
        # Extract beliefs
        beliefs = belief_extractor.extract_beliefs(github_data)
        
        # Extract developer archetype
        archetype = belief_extractor.extract_archetype(github_data)
        
        # Create Epistemic Me models
        self_model = epistemic_client.create_self_model(username, name=github_data.get('user', {}).get('name', username))
        
        # Create beliefs in Epistemic Me
        epistemic_beliefs = []
        for belief in beliefs:
            epistemic_belief = epistemic_client.create_belief(
                self_model['id'],
                belief['content'],
                belief_type='STATEMENT',
                confidence=belief['confidence'],
                source='github'
            )
            epistemic_beliefs.append(epistemic_belief)
        
        # Create belief system
        belief_system = epistemic_client.create_belief_system(self_model['id'], epistemic_beliefs)
        
        # Create dialectic for analysis
        dialectic = epistemic_client.create_dialectic(self_model['id'])
        
        # Calculate epistemic score
        actions = github_data.get('commits', [])
        epistemic_score = epistemic_client.calculate_epistemic_score(beliefs, actions)
        
        # Generate predictions
        predictions = generate_predictions(beliefs, github_data)
        
        # Format response
        response = {
            'username': username,
            'repo': repo,
            'repository': github_data.get('repository', {}),
            'user': github_data.get('user', {}),
            'beliefs': beliefs,
            'archetype': archetype,
            'predictions': predictions,
            'epistemic_score': epistemic_score,
            'self_model': self_model,
            'belief_system': belief_system,
            'dialectic': dialectic,
            'analyzed_at': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"API: Error analyzing {username}/{repo}: {str(e)}")
        return jsonify({
            'error': 'Analysis failed',
            'message': str(e)
        }), 500

def generate_predictions(beliefs: list, github_data: dict) -> dict:
    """Generate predictions based on beliefs and GitHub data"""
    try:
        # Simple prediction logic based on belief patterns
        likely_actions = []
        unlikely_actions = []
        
        belief_categories = [belief.get('category', '') for belief in beliefs]
        
        # Educational focus predictions
        if 'educational' in belief_categories:
            likely_actions.append({
                'text': 'Will create educational content or tutorials',
                'probability': 85
            })
            unlikely_actions.append('Will avoid documenting code')
        
        # Minimalist predictions
        if 'minimalist' in belief_categories:
            likely_actions.append({
                'text': 'Will prefer simple, lightweight solutions',
                'probability': 78
            })
            unlikely_actions.append('Will adopt heavy frameworks')
        
        # Open source predictions
        if 'open_source' in belief_categories:
            likely_actions.append({
                'text': 'Will continue contributing to open source',
                'probability': 92
            })
            unlikely_actions.append('Will move to proprietary solutions')
        
        # Quality focus predictions
        if 'quality' in belief_categories:
            likely_actions.append({
                'text': 'Will invest in testing and code quality',
                'probability': 88
            })
            unlikely_actions.append('Will skip code reviews')
        
        # Default predictions if no specific patterns found
        if not likely_actions:
            likely_actions = [
                {
                    'text': 'Will continue current development patterns',
                    'probability': 70
                }
            ]
        
        if not unlikely_actions:
            unlikely_actions = ['Will abandon current projects']
        
        return {
            'likely_actions': likely_actions,
            'unlikely_actions': unlikely_actions
        }
        
    except Exception as e:
        logger.error(f"Error generating predictions: {e}")
        return {
            'likely_actions': [{'text': 'Will continue coding', 'probability': 80}],
            'unlikely_actions': ['Will stop programming']
        }

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