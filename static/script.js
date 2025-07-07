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
        
        // Populate results with mock data
        populateBeliefs();
        populateProfile();
        populatePredictions();
        populateScore();
    }
}

function populateBeliefs() {
    const container = document.getElementById('beliefsContainer');
    if (!container) return;
    
    const beliefs = [
        {
            text: "Education through code is more powerful than papers",
            confidence: 94
        },
        {
            text: "Simplicity beats complexity in ML implementations",
            confidence: 91
        },
        {
            text: "Teaching by building from scratch creates deeper understanding",
            confidence: 89
        },
        {
            text: "Open source accelerates collective learning",
            confidence: 87
        }
    ];
    
    beliefs.forEach((belief, index) => {
        setTimeout(() => {
            const beliefElement = document.createElement('div');
            beliefElement.className = 'belief-item';
            beliefElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div class="flex-grow-1">
                        <h6 class="mb-1">"${belief.text}"</h6>
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: ${belief.confidence}%"></div>
                        </div>
                    </div>
                    <div class="ms-3">
                        <span class="badge bg-success">${belief.confidence}%</span>
                    </div>
                </div>
            `;
            container.appendChild(beliefElement);
        }, index * 600);
    });
}

function populateProfile() {
    const container = document.getElementById('profileContainer');
    if (!container) return;
    
    const profile = [
        {
            icon: "fas fa-graduation-cap",
            label: "Learning Style",
            value: "\"Show, don't tell\" educator"
        },
        {
            icon: "fas fa-chart-line",
            label: "Risk Profile",
            value: "High technical risk, low conceptual risk"
        },
        {
            icon: "fas fa-bullseye",
            label: "Alignment",
            value: "Democratizing AI knowledge"
        },
        {
            icon: "fas fa-heart",
            label: "Core Values",
            value: "Transparency, Education, Simplicity"
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

function populatePredictions() {
    const container = document.getElementById('predictionsContainer');
    if (!container) return;
    
    const predictions = [
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
    
    const rejections = [
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

function populateScore() {
    const container = document.getElementById('scoreContainer');
    if (!container) return;
    
    setTimeout(() => {
        container.innerHTML = `
            <div class="score-display">8.7<span style="font-size: 2rem;">/10</span></div>
            <div class="score-label">Epistemic Consistency Score</div>
            <p class="mt-3 text-muted">
                How well your beliefs align with your actions
            </p>
            <div class="mt-4">
                <div class="alert alert-info">
                    <i class="fas fa-lightbulb"></i>
                    <strong>Insight:</strong> Your beliefs are highly consistent but consider 
                    exploring adversarial viewpoints to strengthen reasoning.
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