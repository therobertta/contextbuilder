# ContextBuilder 🧠

AI-powered developer belief system analyzer - Extract and visualize developer philosophies from GitHub repositories using Epistemic Me SDK.

## 🚀 Quick Start

Visit `epistemicme.ai/username/repo` to analyze any GitHub repository and discover the developer's core beliefs and philosophies.

### Example URLs
- `epistemicme.ai/karpathy/nanogpt` - Analyze Karpathy's NanoGPT
- `epistemicme.ai/microsoft/vscode` - Analyze VSCode development philosophy
- `epistemicme.ai/yourusername/yourrepo` - Analyze your own repository

## 🎯 What It Does

ContextBuilder scans GitHub repositories and uses AI to extract:

- **Core Beliefs** - Fundamental philosophies behind the code
- **Epistemic Profile** - Learning style, risk profile, and values
- **Belief Predictions** - What the developer is likely to build or reject
- **Epistemic Eval Score** - How well beliefs align with actions

## 💻 Local Development

### Prerequisites
- Python 3.8+
- Git

### Setup
```bash
# Clone the repository
git clone https://github.com/therobertta/contextbuilder.git
cd contextbuilder

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Start the application
python app.py
```

Visit `http://localhost:5001` to see the application.

### Testing Routes
- `http://localhost:5001/` - Home page
- `http://localhost:5001/karpathy/nanogpt` - Example analysis
- `http://localhost:5001/health` - Health check

## 🏗️ Project Structure

```
contextbuilder/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── analysis.html     # Repository analysis page
│   └── error.html        # Error page
├── static/               # Static assets
│   ├── style.css         # CSS styles
│   └── script.js         # JavaScript functionality
└── README.md            # This file
```

## 🚀 Deployment

### 1-Hour AWS EC2 Deployment

```bash
# On EC2 instance
sudo yum update -y
sudo yum install -y python3 python3-pip git

# Clone and setup
git clone https://github.com/therobertta/contextbuilder.git
cd contextbuilder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY="your-production-secret-key"
export GITHUB_TOKEN="your-github-token"
export PORT=80

# Start with gunicorn
gunicorn --bind 0.0.0.0:80 app:app
```

## 📊 Current Status

- ✅ Flask app with dynamic routing
- ✅ Dramatic reveal UI with animations
- ✅ Mock belief extraction and display
- ⏳ Real GitHub API integration (Next)
- ⏳ Actual belief extraction engine (Next)
- ⏳ Epistemic Me SDK integration (Next)

## 🎯 Roadmap

### Week 1 (MVP)
- [x] Basic Flask app structure
- [ ] GitHub API integration
- [ ] Pattern-based belief extraction
- [ ] Deployment to production

### Week 2 (Enhanced Features)
- [ ] Developer personality classification
- [ ] Belief evolution tracking
- [ ] Social comparison features
- [ ] Epistemic Eval integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Links

- [Epistemic Me SDK](https://github.com/Epistemic-Me/Python-SDK)
- [Self Management Agent](https://github.com/Epistemic-Me/Self-Management-Agent)
- [Project Issues](https://github.com/therobertta/contextbuilder/issues)
- [Project Board](https://github.com/users/therobertta/projects/2)

---

*Built with ❤️ using the Epistemic Me SDK for belief-centric AI evaluation.*