import re
import logging
from typing import Dict, List, Any, Tuple
from collections import Counter
import json

logger = logging.getLogger(__name__)

class BeliefExtractor:
    """Extract developer beliefs from GitHub repository data"""
    
    def __init__(self):
        # Pattern-based belief extraction rules
        self.belief_patterns = {
            'educational': {
                'keywords': ['learn', 'teach', 'tutorial', 'example', 'simple', 'beginner', 'guide', 'demo'],
                'phrases': ['step by step', 'easy to understand', 'from scratch', 'learn by doing'],
                'belief_template': 'Education and teaching are important for knowledge sharing',
                'confidence_boost': 0.1
            },
            'minimalist': {
                'keywords': ['simple', 'clean', 'minimal', 'basic', 'vanilla', 'lightweight', 'tiny'],
                'phrases': ['keep it simple', 'less is more', 'minimal dependencies', 'no bloat'],
                'belief_template': 'Simplicity and minimalism lead to better software',
                'confidence_boost': 0.15
            },
            'practical': {
                'keywords': ['working', 'practical', 'useful', 'production', 'real-world', 'hands-on'],
                'phrases': ['it works', 'production ready', 'battle tested', 'real use case'],
                'belief_template': 'Practical solutions are more valuable than theoretical ones',
                'confidence_boost': 0.1
            },
            'open_source': {
                'keywords': ['open', 'free', 'community', 'contribute', 'collaborative', 'share'],
                'phrases': ['open source', 'free software', 'community driven', 'contributions welcome'],
                'belief_template': 'Open source collaboration accelerates innovation',
                'confidence_boost': 0.2
            },
            'quality': {
                'keywords': ['quality', 'robust', 'reliable', 'tested', 'stable', 'maintainable'],
                'phrases': ['code quality', 'well tested', 'maintainable code', 'best practices'],
                'belief_template': 'Code quality and maintainability are essential',
                'confidence_boost': 0.1
            },
            'performance': {
                'keywords': ['fast', 'efficient', 'optimized', 'performance', 'speed', 'scalable'],
                'phrases': ['high performance', 'optimized for speed', 'scalable solution'],
                'belief_template': 'Performance and efficiency are critical considerations',
                'confidence_boost': 0.1
            }
        }
        
        # Developer archetype patterns
        self.archetype_patterns = {
            'educator': ['tutorial', 'learn', 'teach', 'example', 'guide', 'course'],
            'minimalist': ['simple', 'clean', 'minimal', 'basic', 'tiny'],
            'innovator': ['new', 'novel', 'cutting-edge', 'experimental', 'research'],
            'pragmatist': ['practical', 'useful', 'working', 'production', 'real-world'],
            'perfectionist': ['perfect', 'precise', 'exact', 'correct', 'proper']
        }
    
    def extract_beliefs(self, github_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract beliefs from GitHub repository data"""
        try:
            beliefs = []
            
            # Extract from README
            readme_beliefs = self._extract_from_readme(github_data.get('readme', ''))
            beliefs.extend(readme_beliefs)
            
            # Extract from commits
            commit_beliefs = self._extract_from_commits(github_data.get('commits', []))
            beliefs.extend(commit_beliefs)
            
            # Extract from repository metadata
            meta_beliefs = self._extract_from_metadata(github_data.get('repository', {}))
            beliefs.extend(meta_beliefs)
            
            # Extract from issues
            issue_beliefs = self._extract_from_issues(github_data.get('issues', []))
            beliefs.extend(issue_beliefs)
            
            # Deduplicate and score
            beliefs = self._deduplicate_beliefs(beliefs)
            beliefs = self._calculate_confidence(beliefs, github_data)
            
            # Sort by confidence and return top beliefs
            beliefs.sort(key=lambda x: x['confidence'], reverse=True)
            return beliefs[:5]  # Return top 5 beliefs
            
        except Exception as e:
            logger.error(f"Error extracting beliefs: {e}")
            return self._get_fallback_beliefs()
    
    def _extract_from_readme(self, readme: str) -> List[Dict[str, Any]]:
        """Extract beliefs from README content"""
        beliefs = []
        if not readme:
            return beliefs
        
        readme_lower = readme.lower()
        
        for category, patterns in self.belief_patterns.items():
            score = 0
            evidence = []
            
            # Check keywords
            for keyword in patterns['keywords']:
                count = readme_lower.count(keyword)
                if count > 0:
                    score += count * 0.5
                    evidence.append(f"'{keyword}' mentioned {count} times")
            
            # Check phrases
            for phrase in patterns['phrases']:
                if phrase in readme_lower:
                    score += 2
                    evidence.append(f"Contains phrase: '{phrase}'")
            
            if score > 0:
                beliefs.append({
                    'category': category,
                    'content': patterns['belief_template'],
                    'confidence': min(score * 0.1, 0.95),  # Cap at 95%
                    'evidence': evidence,
                    'source': 'readme'
                })
        
        return beliefs
    
    def _extract_from_commits(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract beliefs from commit messages"""
        beliefs = []
        if not commits:
            return beliefs
        
        # Analyze commit message patterns
        commit_text = ' '.join([commit.get('message', '') for commit in commits]).lower()
        
        # Look for specific patterns in commit messages
        patterns = {
            'refactoring': ['refactor', 'cleanup', 'improve', 'optimize', 'simplify'],
            'testing': ['test', 'spec', 'coverage', 'fix test'],
            'documentation': ['doc', 'readme', 'comment', 'document'],
            'breaking_changes': ['breaking', 'major', 'rewrite', 'restructure']
        }
        
        for pattern_name, keywords in patterns.items():
            score = sum(commit_text.count(keyword) for keyword in keywords)
            if score > 0:
                belief_map = {
                    'refactoring': 'Code quality improvement is an ongoing process',
                    'testing': 'Testing and verification are essential for reliability',
                    'documentation': 'Clear documentation improves code accessibility',
                    'breaking_changes': 'Bold changes are necessary for progress'
                }
                
                beliefs.append({
                    'category': pattern_name,
                    'content': belief_map[pattern_name],
                    'confidence': min(score * 0.05, 0.8),
                    'evidence': [f"Commit patterns suggest focus on {pattern_name}"],
                    'source': 'commits'
                })
        
        return beliefs
    
    def _extract_from_metadata(self, repo_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract beliefs from repository metadata"""
        beliefs = []
        
        # Analyze repository description
        description = repo_data.get('description', '').lower()
        if description:
            for category, patterns in self.belief_patterns.items():
                if any(keyword in description for keyword in patterns['keywords']):
                    beliefs.append({
                        'category': category,
                        'content': patterns['belief_template'],
                        'confidence': 0.7,
                        'evidence': [f"Repository description indicates {category} focus"],
                        'source': 'metadata'
                    })
        
        # Analyze topics
        topics = repo_data.get('topics', [])
        if topics:
            topic_text = ' '.join(topics).lower()
            for category, patterns in self.belief_patterns.items():
                if any(keyword in topic_text for keyword in patterns['keywords']):
                    beliefs.append({
                        'category': category,
                        'content': patterns['belief_template'],
                        'confidence': 0.6,
                        'evidence': [f"Repository topics suggest {category} focus"],
                        'source': 'topics'
                    })
        
        return beliefs
    
    def _extract_from_issues(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract beliefs from issue discussions"""
        beliefs = []
        if not issues:
            return beliefs
        
        # Analyze issue titles and bodies
        issue_text = ' '.join([
            issue.get('title', '') + ' ' + issue.get('body', '')
            for issue in issues
        ]).lower()
        
        # Look for community engagement patterns
        if 'help wanted' in issue_text or 'good first issue' in issue_text:
            beliefs.append({
                'category': 'community',
                'content': 'Community contribution and mentorship are valuable',
                'confidence': 0.8,
                'evidence': ['Issues show welcoming attitude to new contributors'],
                'source': 'issues'
            })
        
        return beliefs
    
    def _deduplicate_beliefs(self, beliefs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate beliefs and merge similar ones"""
        # Group by category
        categories = {}
        for belief in beliefs:
            category = belief['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(belief)
        
        # Keep the highest confidence belief per category
        deduplicated = []
        for category, category_beliefs in categories.items():
            if category_beliefs:
                best_belief = max(category_beliefs, key=lambda x: x['confidence'])
                # Merge evidence from all beliefs in this category
                all_evidence = []
                for belief in category_beliefs:
                    all_evidence.extend(belief.get('evidence', []))
                best_belief['evidence'] = list(set(all_evidence))
                deduplicated.append(best_belief)
        
        return deduplicated
    
    def _calculate_confidence(self, beliefs: List[Dict[str, Any]], 
                            github_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate final confidence scores based on multiple factors"""
        repo_data = github_data.get('repository', {})
        
        # Boost confidence based on repository metrics
        stars = repo_data.get('stars', 0)
        forks = repo_data.get('forks', 0)
        
        star_boost = min(stars / 1000, 0.1)  # Up to 10% boost for popular repos
        fork_boost = min(forks / 500, 0.05)  # Up to 5% boost for frequently forked repos
        
        for belief in beliefs:
            belief['confidence'] = min(belief['confidence'] + star_boost + fork_boost, 0.95)
        
        return beliefs
    
    def _get_fallback_beliefs(self) -> List[Dict[str, Any]]:
        """Return fallback beliefs if extraction fails"""
        return [
            {
                'category': 'general',
                'content': 'Code should be functional and maintainable',
                'confidence': 0.7,
                'evidence': ['General software development principle'],
                'source': 'fallback'
            }
        ]
    
    def extract_archetype(self, github_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract developer archetype from GitHub data"""
        try:
            # Analyze all text content
            all_text = (
                github_data.get('readme', '') + ' ' +
                github_data.get('repository', {}).get('description', '') + ' ' +
                ' '.join([commit.get('message', '') for commit in github_data.get('commits', [])])
            ).lower()
            
            # Score each archetype
            archetype_scores = {}
            for archetype, keywords in self.archetype_patterns.items():
                score = sum(all_text.count(keyword) for keyword in keywords)
                if score > 0:
                    archetype_scores[archetype] = score
            
            if not archetype_scores:
                return {'type': 'pragmatist', 'confidence': 0.5}
            
            # Get the highest scoring archetype
            best_archetype = max(archetype_scores, key=archetype_scores.get)
            confidence = min(archetype_scores[best_archetype] * 0.1, 0.95)
            
            return {
                'type': best_archetype,
                'confidence': confidence,
                'description': self._get_archetype_description(best_archetype)
            }
            
        except Exception as e:
            logger.error(f"Error extracting archetype: {e}")
            return {'type': 'pragmatist', 'confidence': 0.5}
    
    def _get_archetype_description(self, archetype: str) -> str:
        """Get description for developer archetype"""
        descriptions = {
            'educator': 'Focuses on teaching and sharing knowledge through code',
            'minimalist': 'Believes in simple, clean solutions with minimal complexity',
            'innovator': 'Pushes boundaries and explores cutting-edge technologies',
            'pragmatist': 'Prioritizes practical, working solutions over theoretical perfection',
            'perfectionist': 'Strives for precise, correct, and well-crafted code'
        }
        return descriptions.get(archetype, 'Balanced approach to software development')