import requests
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class GitHubClient:
    """GitHub API client for fetching repository data"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'ContextBuilder/1.0'
        }
        
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_repository(self, username: str, repo: str) -> Dict[str, Any]:
        """Get repository metadata"""
        try:
            url = f"{self.base_url}/repos/{username}/{repo}"
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            return {
                'name': data['name'],
                'full_name': data['full_name'],
                'description': data.get('description', ''),
                'language': data.get('language', ''),
                'topics': data.get('topics', []),
                'stars': data['stargazers_count'],
                'forks': data['forks_count'],
                'created_at': data['created_at'],
                'updated_at': data['updated_at'],
                'owner': {
                    'login': data['owner']['login'],
                    'type': data['owner']['type']
                }
            }
        except requests.RequestException as e:
            logger.error(f"Error fetching repository {username}/{repo}: {e}")
            raise
    
    def get_readme(self, username: str, repo: str) -> str:
        """Get repository README content"""
        try:
            url = f"{self.base_url}/repos/{username}/{repo}/readme"
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            if data['encoding'] == 'base64':
                import base64
                content = base64.b64decode(data['content']).decode('utf-8')
                return content
            return data['content']
        except requests.RequestException as e:
            logger.warning(f"Could not fetch README for {username}/{repo}: {e}")
            return ""
    
    def get_commits(self, username: str, repo: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent commits"""
        try:
            url = f"{self.base_url}/repos/{username}/{repo}/commits"
            params = {'per_page': limit}
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            commits = []
            for commit_data in response.json():
                commits.append({
                    'sha': commit_data['sha'][:7],
                    'message': commit_data['commit']['message'],
                    'author': commit_data['commit']['author']['name'],
                    'date': commit_data['commit']['author']['date'],
                    'url': commit_data['html_url']
                })
            return commits
        except requests.RequestException as e:
            logger.error(f"Error fetching commits for {username}/{repo}: {e}")
            return []
    
    def get_issues(self, username: str, repo: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent issues and discussions"""
        try:
            url = f"{self.base_url}/repos/{username}/{repo}/issues"
            params = {'per_page': limit, 'state': 'all'}
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            issues = []
            for issue_data in response.json():
                issues.append({
                    'number': issue_data['number'],
                    'title': issue_data['title'],
                    'body': issue_data.get('body', ''),
                    'state': issue_data['state'],
                    'comments': issue_data['comments'],
                    'created_at': issue_data['created_at'],
                    'labels': [label['name'] for label in issue_data.get('labels', [])]
                })
            return issues
        except requests.RequestException as e:
            logger.error(f"Error fetching issues for {username}/{repo}: {e}")
            return []
    
    def get_user(self, username: str) -> Dict[str, Any]:
        """Get user profile information"""
        try:
            url = f"{self.base_url}/users/{username}"
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            return {
                'login': data['login'],
                'name': data.get('name', ''),
                'bio': data.get('bio', ''),
                'company': data.get('company', ''),
                'location': data.get('location', ''),
                'email': data.get('email', ''),
                'public_repos': data['public_repos'],
                'followers': data['followers'],
                'following': data['following'],
                'created_at': data['created_at']
            }
        except requests.RequestException as e:
            logger.error(f"Error fetching user {username}: {e}")
            return {}
    
    def get_repository_data(self, username: str, repo: str) -> Dict[str, Any]:
        """Get comprehensive repository data for analysis"""
        try:
            # Fetch all data in parallel would be ideal, but for simplicity:
            repo_data = self.get_repository(username, repo)
            readme = self.get_readme(username, repo)
            commits = self.get_commits(username, repo)
            issues = self.get_issues(username, repo)
            user = self.get_user(username)
            
            return {
                'repository': repo_data,
                'readme': readme,
                'commits': commits,
                'issues': issues,
                'user': user,
                'fetched_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching comprehensive data for {username}/{repo}: {e}")
            raise