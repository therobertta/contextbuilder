// ContextBuilder JavaScript

// Scanning animation and progression
let scanningSteps = [
    "Initializing analysis...",
    "Fetching repository data...",
    "Analyzing README content...",
    "Processing commit messages...",
    "Extracting belief patterns...",
    "Calculating confidence scores...",
    "Generating epistemic profile...",
    "Creating predictions...",
    "Finalizing analysis..."
];

let currentStep = 0;
let scanProgress = 0;

function updateScanningProgress() {
    const progressBar = document.getElementById('scanProgress');
    const statusText = document.getElementById('scanStatus');
    
    if (!progressBar || !statusText) return;
    
    // Update progress bar
    scanProgress += Math.random() * 15 + 5; // Random increment between 5-20%
    if (scanProgress > 100) scanProgress = 100;
    
    progressBar.style.width = scanProgress + '%';
    progressBar.textContent = Math.round(scanProgress) + '%';
    
    // Update status text
    if (currentStep < scanningSteps.length) {
        statusText.textContent = scanningSteps[currentStep];
        currentStep++;
    }
    
    // Check if scanning is complete
    if (scanProgress >= 100) {
        setTimeout(() => {
            statusText.textContent = "Analysis complete! Revealing insights...";
            setTimeout(showResults, 1000);
        }, 500);
        return;
    }
    
    // Continue scanning
    setTimeout(updateScanningProgress, 800 + Math.random() * 400);
}

function showResults() {
    const scanningContainer = document.querySelector('.scanning-container');
    const resultsContainer = document.getElementById('resultsContainer');
    
    if (scanningContainer && resultsContainer) {
        scanningContainer.style.display = 'none';
        resultsContainer.style.display = 'block';
        
        // Fetch real analysis data
        fetchAnalysisData();
    }
}

async function fetchAnalysisData() {
    try {
        const { username, repo } = window.repoData;
        const response = await fetch(`/api/analyze/${username}/${repo}`);
        
        if (!response.ok) {
            throw new Error('Analysis failed');
        }
        
        const data = await response.json();
        
        // Populate results with real data
        populateBeliefs(data.beliefs);
        populateProfile(data.archetype, data.repository, data.user);
        populatePredictions(data.predictions);
        populateScore(data.epistemic_score);
        
        // Store data for sharing
        window.analysisData = data;
        
    } catch (error) {
        console.error('Error fetching analysis:', error);
        // Fall back to mock data
        populateBeliefs();
        populateProfile();
        populatePredictions();
        populateScore();
    }
}

function populateBeliefs(beliefsData = null) {
    const container = document.getElementById('beliefsContainer');
    if (!container) return;
    
    // Use real data if available, otherwise fallback to mock data
    const beliefs = beliefsData || [
        {
            content: "Education through code is more powerful than papers",
            confidence: 0.94
        },
        {
            content: "Simplicity beats complexity in ML implementations",
            confidence: 0.91
        },
        {
            content: "Teaching by building from scratch creates deeper understanding",
            confidence: 0.89
        },
        {
            content: "Open source accelerates collective learning",
            confidence: 0.87
        }
    ];
    
    beliefs.forEach((belief, index) => {
        setTimeout(() => {
            const beliefElement = document.createElement('div');
            beliefElement.className = 'belief-item';
            
            const confidence = Math.round((belief.confidence || 0.8) * 100);
            const content = belief.content || belief.text;
            const evidence = belief.evidence ? belief.evidence.join(', ') : '';
            
            beliefElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div class="flex-grow-1">
                        <h6 class="mb-1">"${content}"</h6>
                        ${evidence ? `<small class="text-muted">Evidence: ${evidence}</small>` : ''}
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: ${confidence}%"></div>
                        </div>
                    </div>
                    <div class="ms-3">
                        <span class="badge bg-success">${confidence}%</span>
                    </div>
                </div>
            `;
            container.appendChild(beliefElement);
        }, index * 600);
    });
}

function populateProfile(archetypeData = null, repositoryData = null, userData = null) {
    const container = document.getElementById('profileContainer');
    if (!container) return;
    
    // Build profile from real data if available
    const archetype = archetypeData || { type: 'pragmatist', description: 'Balanced approach to software development' };
    const repo = repositoryData || {};
    const user = userData || {};
    
    const profile = [
        {
            icon: "fas fa-user-circle",
            label: "Developer Archetype",
            value: `"The ${archetype.type.charAt(0).toUpperCase() + archetype.type.slice(1)}" - ${archetype.description || ''}`
        },
        {
            icon: "fas fa-code",
            label: "Primary Language",
            value: repo.language || "Multi-language developer"
        },
        {
            icon: "fas fa-star",
            label: "Community Impact",
            value: `${repo.stars || 0} stars, ${repo.forks || 0} forks`
        },
        {
            icon: "fas fa-calendar",
            label: "Experience Level",
            value: user.created_at ? `GitHub since ${new Date(user.created_at).getFullYear()}` : "Experienced developer"
        }
    ];
    
    profile.forEach((item, index) => {
        setTimeout(() => {
            const profileElement = document.createElement('div');
            profileElement.className = 'profile-item';
            profileElement.innerHTML = `
                <div class="profile-icon">
                    <i class="${item.icon} text-primary"></i>
                </div>
                <div class="flex-grow-1">
                    <strong>${item.label}:</strong> ${item.value}
                </div>
            `;
            container.appendChild(profileElement);
        }, index * 400);
    });
}

function populatePredictions(predictionsData = null) {
    const container = document.getElementById('predictionsContainer');
    if (!container) return;
    
    // Use real data if available
    const predictions = predictionsData ? predictionsData.likely_actions : [
        {
            text: "Will build educational tool for transformers",
            probability: 78
        },
        {
            text: "Will critique current SOTA complexity",
            probability: 65
        },
        {
            text: "Will open-source next research project",
            probability: 92
        }
    ];
    
    const rejections = predictionsData ? predictionsData.unlikely_actions : [
        "Over-engineered frameworks",
        "Blackbox AI solutions",
        "Non-reproducible research"
    ];
    
    setTimeout(() => {
        container.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <h5 class="text-success"><i class="fas fa-thumbs-up"></i> Likely to Build:</h5>
                    <ul class="list-unstyled">
                        ${predictions.map(p => `
                            <li class="mb-2">
                                <div class="d-flex justify-content-between">
                                    <span>${p.text}</span>
                                    <span class="badge bg-success">${p.probability}%</span>
                                </div>
                            </li>
                        `).join('')}
                    </ul>
                </div>
                <div class="col-md-6">
                    <h5 class="text-danger"><i class="fas fa-thumbs-down"></i> Likely to Reject:</h5>
                    <ul class="list-unstyled">
                        ${rejections.map(r => `
                            <li class="mb-2">
                                <i class="fas fa-times text-danger me-2"></i>${r}
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>
        `;
    }, 500);
}

function populateScore(scoreData = null) {
    const container = document.getElementById('scoreContainer');
    if (!container) return;
    
    // Use real data if available
    const score = scoreData || {
        overall_score: 8.7,
        recommendation: 'Your beliefs are highly consistent but consider exploring adversarial viewpoints to strengthen reasoning.'
    };
    
    setTimeout(() => {
        container.innerHTML = `
            <div class="score-display">${score.overall_score}<span style="font-size: 2rem;">/10</span></div>
            <div class="score-label">Epistemic Consistency Score</div>
            <p class="mt-3 text-muted">
                How well your beliefs align with your actions
            </p>
            ${score.consistency_score ? `
                <div class="row mt-3">
                    <div class="col-md-4">
                        <small>Consistency</small><br>
                        <strong>${score.consistency_score}/10</strong>
                    </div>
                    <div class="col-md-4">
                        <small>Growth</small><br>
                        <strong>${score.growth_score}/10</strong>
                    </div>
                    <div class="col-md-4">
                        <small>Impact</small><br>
                        <strong>${score.impact_score}/10</strong>
                    </div>
                </div>
            ` : ''}
            <div class="mt-4">
                <div class="alert alert-info">
                    <i class="fas fa-lightbulb"></i>
                    <strong>Insight:</strong> ${score.recommendation}
                </div>
            </div>
        `;
    }, 1000);
}

// Social sharing functions
function shareToTwitter() {
    const url = window.location.href;
    const text = `🤯 Just had my GitHub mind read by @EpistemicMe! Check out what it discovered about ${window.repoData.username}/${window.repoData.repo}`;
    window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`, '_blank');
}

function copyLink() {
    navigator.clipboard.writeText(window.location.href).then(() => {
        alert('Link copied to clipboard!');
    }).catch(() => {
        alert('Failed to copy link');
    });
}

// Initialize scanning when page loads
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('scanProgress')) {
        setTimeout(updateScanningProgress, 1000);
    }
});