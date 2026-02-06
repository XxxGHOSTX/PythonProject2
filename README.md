# Thalos Prime AI Interface Collection

A collection of advanced AI terminal interfaces with cinematic visual effects, powered by Google's Gemini AI and Three.js/Canvas animations.

## 🎨 Available Versions

### 🌟 Version 4.0 - PRIMARY DIRECTIVE (NEW!)
**File:** `thalos_prime_primary_directive.html`
**Launch:** `launch_primary_directive.bat`

**THE MOST ADVANCED VERSION - UNRESTRICTED AI INTERFACE**

#### Revolutionary Features:
- **5 Operation Modes**: Adaptive, Code Generation, Deep Analysis, Creative, Unrestricted
- **Advanced Code Generation**: Copilot-like capabilities for any programming language
- **Unlimited Length Generation**: 10 length settings from minimal to UNLIMITED
- **3 AI Models**: Gemini 2.0 Flash, Experimental, and 2.5 Flash
- **Syntax Highlighting**: Support for 100+ programming languages
- **Context Management**: Conversation history with token tracking
- **Professional Features**: Export conversations, context panel, analytics
- **Enhanced Visuals**: 8,000 particles with dynamic connections
- **Multi-line Input**: Advanced text input with formatting
- **One-Click Code Copying**: Copy any code block instantly
- **No Restrictions**: Completely unrestricted output capabilities

Perfect for: Developers, writers, researchers, analysts, anyone needing unlimited AI capabilities

**→ [READ FULL DOCUMENTATION](PRIMARY_DIRECTIVE_GUIDE.md)**
**→ [QUICK REFERENCE](PRIMARY_DIRECTIVE_QUICK_REF.txt)**

---

### Version 3.0 - Terminal Edition (Green Matrix)
**File:** `thalos_prime.html`
- Classic Matrix-style green terminal aesthetic
- 5,000 particle 3D visualization using Three.js
- Real-time telemetry display
- Minimalist command-line interface
- Perfect for: Developers, Matrix fans, terminal enthusiasts

### Version 2.1 - Celestial Navigator (Amber/Gold)
**File:** `thalos_celestial.html`
- React-based interface with amber/gold cosmic theme
- Drifting universe background with Matrix rain overlay
- NASA-inspired galactic coordinate mapping
- Sidebar with galaxy database (Centaurus A, Messier 87, etc.)
- Star charts and celestial data visualization
- Perfect for: Space enthusiasts, astronomy lovers, cosmic explorers

## 🚀 Quick Start

### Option 1: Launch PRIMARY DIRECTIVE (Recommended - Most Advanced!)

**Double-click:** `launch_primary_directive.bat`

The most advanced version with unrestricted AI capabilities, code generation, and unlimited content generation.

### Option 2: Quick Launch Menu (Multiple Versions)

1. **Double-click:** `launch_thalos.bat`
2. **Choose your version:**
   - `1` - Terminal Edition (Green Matrix)
   - `2` - Celestial Navigator (Amber/Gold)
3. Interface opens in your browser immediately!

### Option 3: Launch Specific Version Manually

**Primary Directive (v4.0):**
```powershell
start thalos_prime_primary_directive.html
```

**Terminal Edition (v3.0):**
```powershell
start thalos_prime.html
```

**Celestial Navigator (v2.1):**
```powershell
start thalos_celestial.html
```

### Option 3: With Local Server

1. **Run the deployment server**
   ```powershell
   python deploy_server.py
   ```

2. **Select which version to open** (or open both!)
   - Server runs on http://localhost:8080
   - Choose from interactive menu

### Option 4: Direct Browser Opening

- Right-click either HTML file → Open with → Your Browser
- No server needed!

## 🎨 Features

### Terminal Edition (v3.0)
- **3D Particle Visualization**: Real-time rotating particle field using Three.js
- **AI-Powered Terminal**: Natural language interface to Google Gemini AI
- **Matrix Aesthetic**: Green-on-black terminal with glowing effects
- **System Telemetry**: Live latency and neural load indicators
- **Responsive Design**: Works on desktop and mobile devices
- **Retry Logic**: Automatic reconnection on API failures

### Celestial Navigator (v2.1)
- **React-Based Interface**: Modern component architecture
- **Cosmic Background**: Drifting stars + Matrix rain hybrid canvas animation
- **Galactic Mapping**: NASA-inspired coordinate system with real galaxies
- **Sidebar Database**: Browse Centaurus A, Messier 87, Sagittarius A*, Andromeda
- **Module System**: Star Charts, Data Logs, and Nexus console
- **Amber/Gold Theme**: Warm cosmic aesthetic with glowing effects
- **Live Footer**: Real-time coordinate display and drift engine status

## 🛠️ Technical Details

### Terminal Edition
- **Frontend**: Pure HTML/CSS/JavaScript (no build step required)
- **3D Engine**: Three.js r128
- **AI Model**: Google Gemini 2.5 Flash Preview
- **No Dependencies**: Self-contained single HTML file

### Celestial Navigator
- **Frontend**: React 18 (via CDN - no build step)
- **Styling**: Tailwind CSS (via CDN)
- **Canvas**: Custom 2D animation engine
- **AI Model**: Google Gemini 2.5 Flash Preview
- **Transpiler**: Babel Standalone (in-browser JSX compilation)
- **No Dependencies**: Self-contained single HTML file

**Both versions:**
- ✅ No npm install required
- ✅ No build process
- ✅ Single file deployment
- ✅ Same API key works for both

## ⚙️ Configuration

You can customize the interface by editing `thalos_prime.html`:

- **Particle Count** (line 118): Change `5000` to increase/decrease particles
- **Animation Speed** (lines 132-133): Adjust rotation values
- **Terminal Height** (line 42): Modify `height: 200px`
- **Color Scheme**: Search for `#0f0` to change the green color

## 🔐 Security Notes

- **Never commit your API key** to public repositories
- Consider using environment variables for production deployments
- The API key is currently client-side - use a backend proxy for production
- Google Gemini has usage quotas - monitor your usage at Google AI Studio

## 📝 System Prompt

Thalos Prime uses a custom system prompt to maintain its SBI (Synthetic Biological Intelligence) persona. You can modify this in the `callThalos()` function (line 140).

## 🆘 Troubleshooting

**Interface loads but AI doesn't respond:**
- Check that you've added your API key correctly
- Verify your API key is valid at https://aistudio.google.com
- Check browser console for errors (F12)

**3D visualization not appearing:**
- Ensure Three.js CDN is accessible
- Check that WebGL is supported in your browser
- Try a different browser (Chrome/Firefox recommended)

**Server won't start:**
- Ensure port 8000 is not already in use
- Try changing the PORT value in `deploy_server.py`
- Check Python is installed: `python --version`

## 📜 License

This project is provided as-is for educational and personal use.

## 🌟 Credits

- Three.js for 3D rendering
- Google Gemini AI for natural language processing
- Inspired by the Matrix franchise aesthetic

---

**SYSTEM STATUS: OPERATIONAL**
**NEURAL INTERFACE: READY**
**THALOS PRIME V3.0 ONLINE**
