# THALOS PRIME V3.0 - SETUP GUIDE

## Step-by-Step Setup Instructions

### 1. Get Your Google Gemini API Key (FREE)

1. Open your browser and go to: https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click the "Create API Key" button
4. Select "Create API key in new project" (or use existing project)
5. Copy the API key that appears (it looks like: AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXX)

### 2. Add the API Key to Your File

1. Open the file: `thalos_prime.html`
2. Find line 102 which says:
   ```javascript
   const apiKey = "";
   ```
3. Paste your API key between the quotes:
   ```javascript
   const apiKey = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXX";
   ```
4. Save the file (Ctrl+S)

### 3. Deploy the Interface

#### METHOD A: Using the Deploy Script (Easiest)
- Double-click `deploy.bat`
- The server will start and open your browser automatically

#### METHOD B: Using Python Command
- Open PowerShell or Command Prompt
- Navigate to the project folder
- Run: `python deploy_server.py`

#### METHOD C: Direct Browser Opening
- Right-click `thalos_prime.html`
- Select "Open with" → Your browser (Chrome, Firefox, Edge)

### 4. Start Using Thalos

Once the page loads:
- You'll see a green terminal interface with particle effects
- Type any command or question in the input field at the bottom
- Press Enter to send your query to Thalos Prime
- The AI will respond in the terminal

### Example Commands to Try:

```
> What are you?
> Explain quantum computing
> Write a Python function to sort a list
> Tell me about the Fermi paradox
> System diagnostics
> Who created you?
```

## Deployment Options

### Local Deployment (What we've set up)
✅ Works immediately
✅ No internet hosting needed
✅ Private and secure
✅ Free
❌ Only accessible on your computer

### Web Hosting (For public access)

#### GitHub Pages (Free)
1. Create a GitHub repository
2. Upload `thalos_prime.html`
3. Go to Settings → Pages
4. Enable GitHub Pages
5. Your site will be at: `https://yourusername.github.io/repo-name/thalos_prime.html`

#### Netlify (Free)
1. Go to https://netlify.com
2. Drag and drop `thalos_prime.html`
3. Get instant deployment URL

#### Vercel (Free)
1. Go to https://vercel.com
2. Import your project
3. Deploy instantly

## Troubleshooting

### Problem: "API Key not working"
**Solution:**
- Verify the key is copied correctly (no extra spaces)
- Check you've saved the HTML file after adding the key
- Ensure you have internet connection
- Verify the API key is enabled at https://aistudio.google.com

### Problem: "Page not loading"
**Solution:**
- If using deploy_server.py, ensure Python is installed
- Check port 8000 is not in use by another program
- Try changing PORT in deploy_server.py to 8080 or 3000
- Try opening the HTML file directly in browser

### Problem: "3D effects not showing"
**Solution:**
- Clear browser cache (Ctrl+F5)
- Try a different browser (Chrome recommended)
- Check internet connection (Three.js loads from CDN)
- Ensure WebGL is enabled in browser settings

### Problem: "Terminal not responding"
**Solution:**
- Open browser console (F12) to check for errors
- Verify API key is correctly added
- Check Google AI Studio for quota limits
- Try refreshing the page

## Security Best Practices

⚠️ **IMPORTANT:** Your API key is visible in the HTML file

For personal use: This is fine
For public deployment: Consider these options:
1. Use a backend server to hide the API key
2. Set up API key restrictions in Google Cloud Console
3. Monitor your API usage regularly
4. Never commit files with API keys to public repositories

## Customization Tips

### Change Colors
Search for `#0f0` (green) in the HTML and replace with:
- `#00f` for blue
- `#f00` for red  
- `#0ff` for cyan
- `#f0f` for magenta

### Increase Particles
Line 118: Change `5000` to higher number (may impact performance)

### Speed Up Animation
Lines 132-133: Increase the rotation values (0.001 → 0.005)

### Change Terminal Size
Line 42: Modify `height: 200px` to larger value

## Support

For issues with:
- **Google Gemini API**: https://ai.google.dev/docs
- **Three.js**: https://threejs.org/docs/
- **General web hosting**: Check your hosting provider's documentation

## Next Steps

1. ✅ Get API key from Google
2. ✅ Add it to thalos_prime.html
3. ✅ Run deploy_server.py or deploy.bat
4. ✅ Start chatting with Thalos Prime!

---

**SYSTEM INITIALIZATION COMPLETE**
**READY FOR DEPLOYMENT**
