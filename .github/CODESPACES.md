# GitHub Codespaces Configuration

This repository is fully configured for GitHub Codespaces, providing instant development environments for all contributors and reviewers.

## 🎯 Key Features

### Automatic Availability
- ✅ Available on all pull requests automatically
- ✅ Works with all branches and forks
- ✅ No repository settings changes needed
- ✅ Free tier supports up to 60 hours/month

### Pre-configured Environment
- Node.js 20.x with npm
- Mintlify CLI pre-installed
- VS Code extensions for Markdown/MDX
- Automatic port forwarding for preview
- Git and GitHub CLI included

## 🚀 Usage

### For Pull Request Reviews
1. Navigate to any PR
2. Click "Code" → "Open with Codespaces"
3. Wait for environment to load (~30 seconds)
4. Run `npm run dev` to preview changes
5. Browse to forwarded port 3000

### For Development
1. Fork the repository
2. Click the Codespaces badge in README
3. Start coding immediately
4. All changes are automatically saved

### Quick Commands
```bash
npm run dev      # Start development server
npm run build    # Build documentation
npm run preview  # Preview production build
```

## ⚙️ Configuration Details

### Resource Allocation
- **CPU**: 2 cores (minimum)
- **Memory**: 4GB RAM
- **Storage**: 32GB
- **Idle timeout**: 30 minutes (default)

### Automatic Setup
The following happens automatically when a Codespace is created:

1. **Install Dependencies**: `npm install` runs automatically
2. **Install Mintlify**: Global installation of latest version
3. **Configure Editor**: VS Code settings and extensions
4. **Open README**: Automatically opens for orientation
5. **Port Forwarding**: Port 3000 is forwarded for preview

### VS Code Extensions
- ESLint
- Prettier
- Markdown All in One
- markdownlint
- MDX

## 🔧 Customization

### Personal Dotfiles
You can use your personal dotfiles by:
1. Creating a dotfiles repository
2. Enabling in GitHub settings
3. Codespaces will automatically apply them

### Environment Variables
Set in your Codespace:
```bash
export VARIABLE_NAME="value"
```

Or add to `.devcontainer/devcontainer.json`:
```json
"remoteEnv": {
  "VARIABLE_NAME": "value"
}
```

## 📊 Usage Limits

### Free Tier (Default)
- 120 core hours/month for free accounts
- 180 core hours/month for Pro accounts
- 2-core machines = 60-90 hours of usage

### Best Practices
- Stop Codespaces when not in use
- Use timeouts (Settings → Codespaces → Default idle timeout)
- Delete old Codespaces regularly

## 🆘 Troubleshooting

### Common Issues

**Codespace won't start**
- Check GitHub status page
- Try a different browser
- Clear browser cache

**Port forwarding not working**
- Check "Ports" tab in terminal
- Ensure server is running
- Try manual port forward

**Extensions not loading**
- Reload window: Cmd/Ctrl + R
- Rebuild container
- Check devcontainer.json syntax

**Performance issues**
- Upgrade to 4-core machine
- Close unnecessary tabs
- Check network connection

### Getting Help
- Check [GitHub Codespaces docs](https://docs.github.com/codespaces)
- Open an issue in this repository
- Contact repository maintainers

## 🔐 Security

- Codespaces are isolated environments
- Access controlled by GitHub permissions
- Secrets can be added via repository/organization settings
- All data is encrypted at rest and in transit

---

*This configuration ensures that every contributor and reviewer can instantly access a fully-configured development environment without any local setup.*