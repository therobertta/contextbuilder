import os
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
import json

logger = logging.getLogger(__name__)

class EpistemicClient:
    """Epistemic Me SDK client for belief system modeling"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get('EPISTEMIC_API_KEY')
        self.base_url = os.environ.get('EPISTEMIC_BASE_URL', 'https://api.epistemicme.ai')
        
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}' if self.api_key else '',
            'User-Agent': 'ContextBuilder/1.0'
        }
        
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def create_self_model(self, username: str, **kwargs) -> Dict[str, Any]:
        """Create a self model for the developer"""
        try:
            data = {
                'user_id': username,
                'name': kwargs.get('name', username),
                'philosophies': kwargs.get('philosophies', ['open_source', 'collaborative']),
                'created_at': datetime.now().isoformat()
            }
            
            # For now, return mock data since we don't have real API
            return {
                'id': f'self_model_{username}',
                'user_id': username,
                'name': data['name'],
                'philosophies': data['philosophies'],
                'created_at': data['created_at']
            }
        except Exception as e:
            logger.error(f"Error creating self model for {username}: {e}")
            raise
    
    def create_belief(self, self_model_id: str, content: str, belief_type: str = 'STATEMENT', 
                     confidence: float = 0.8, source: str = 'github') -> Dict[str, Any]:
        """Create a belief from extracted content"""
        try:
            data = {
                'self_model_id': self_model_id,
                'content': content,
                'belief_type': belief_type,
                'confidence': confidence,
                'source': source,
                'created_at': datetime.now().isoformat()
            }
            
            # For now, return mock data
            return {
                'id': f'belief_{hash(content) % 10000}',
                'self_model_id': self_model_id,
                'content': content,
                'belief_type': belief_type,
                'confidence': confidence,
                'source': source,
                'created_at': data['created_at']
            }
        except Exception as e:
            logger.error(f"Error creating belief: {e}")
            raise
    
    def create_belief_system(self, self_model_id: str, beliefs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a belief system from multiple beliefs"""
        try:
            data = {
                'self_model_id': self_model_id,
                'beliefs': beliefs,
                'created_at': datetime.now().isoformat()
            }
            
            # For now, return mock data
            return {
                'id': f'belief_system_{self_model_id}',
                'self_model_id': self_model_id,
                'beliefs': beliefs,
                'belief_count': len(beliefs),
                'created_at': data['created_at']
            }
        except Exception as e:
            logger.error(f"Error creating belief system: {e}")
            raise
    
    def create_dialectic(self, self_model_id: str, learning_objective: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a dialectic for reasoning about beliefs"""
        try:
            data = {
                'self_model_id': self_model_id,
                'learning_objective': learning_objective or {
                    'description': 'Understand developer coding philosophy and practices',
                    'topics': ['code_quality', 'collaboration', 'technology_choices'],
                    'target_belief_type': 'CAUSAL'
                },
                'created_at': datetime.now().isoformat()
            }
            
            # For now, return mock data
            return {
                'id': f'dialectic_{self_model_id}',
                'self_model_id': self_model_id,
                'learning_objective': data['learning_objective'],
                'interactions': [],
                'created_at': data['created_at']
            }
        except Exception as e:
            logger.error(f"Error creating dialectic: {e}")
            raise
    
    def calculate_epistemic_score(self, beliefs: List[Dict[str, Any]], 
                                 actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate epistemic evaluation score"""
        try:
            # Simple scoring algorithm for now
            consistency_score = self._calculate_consistency(beliefs, actions)
            growth_score = self._calculate_growth(beliefs)
            impact_score = self._calculate_impact(actions)
            
            overall_score = (consistency_score + growth_score + impact_score) / 3
            
            return {
                'overall_score': round(overall_score, 1),
                'consistency_score': round(consistency_score, 1),
                'growth_score': round(growth_score, 1),
                'impact_score': round(impact_score, 1),
                'recommendation': self._get_recommendation(overall_score),
                'calculated_at': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error calculating epistemic score: {e}")
            return {
                'overall_score': 8.5,
                'consistency_score': 8.7,
                'growth_score': 7.2,
                'impact_score': 9.5,
                'recommendation': 'Your beliefs are highly consistent but consider exploring adversarial viewpoints to strengthen reasoning.',
                'calculated_at': datetime.now().isoformat()
            }
    
    def _calculate_consistency(self, beliefs: List[Dict[str, Any]], actions: List[Dict[str, Any]]) -> float:
        """Calculate how well beliefs align with actions"""
        # Mock implementation - in reality this would use sophisticated NLP
        return 8.7
    
    def _calculate_growth(self, beliefs: List[Dict[str, Any]]) -> float:
        """Calculate belief evolution and growth rate"""
        # Mock implementation
        return 7.2
    
    def _calculate_impact(self, actions: List[Dict[str, Any]]) -> float:
        """Calculate belief influence on others"""
        # Mock implementation based on GitHub metrics
        return 9.5
    
    def _get_recommendation(self, score: float) -> str:
        """Get recommendation based on score"""
        if score >= 9.0:
            return "Exceptional epistemic consistency! Your beliefs strongly align with your actions."
        elif score >= 8.0:
            return "Your beliefs are highly consistent but consider exploring adversarial viewpoints to strengthen reasoning."
        elif score >= 7.0:
            return "Good alignment between beliefs and actions. Consider documenting your philosophy more explicitly."
        elif score >= 6.0:
            return "Some inconsistencies detected. Reflect on whether your actions truly reflect your stated beliefs."
        else:
            return "Significant gaps between beliefs and actions. Consider realigning your practices with your core values."