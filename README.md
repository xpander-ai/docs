# xpander.ai Documentation

This repository contains the documentation for xpander.ai, built with [Mintlify](https://mintlify.com).

🌐 **Live Documentation**: https://docs.xpander.ai

## 🚀 Getting Started with GitHub Codespaces

GitHub Codespaces provides a complete, ready-to-use development environment in your browser. This is the easiest way to preview documentation changes and review PRs.

### Quick Start

1. **Open in Codespaces**
   - Click the green "Code" button on this repository
   - Select the "Codespaces" tab
   - Click "Create codespace on main" (or your branch)

2. **Start the Documentation Server**
   Once your Codespace is ready, run:
   ```bash
   npm install
   npm run dev
   ```

3. **Preview the Documentation**
   - The documentation will be available at `http://localhost:3000`
   - Codespaces will automatically forward the port and show a notification
   - Click "Open in Browser" when prompted

### Available Commands

| Command | Description |
|---------|-------------|
| `npm install` | Install dependencies (including Mintlify CLI) |
| `npm run dev` | Start the development server with hot reload |
| `npm run build` | Build the documentation for production |
| `npm run preview` | Preview the production build locally |

### Reviewing Pull Requests

1. **Open PR in Codespaces**
   - Navigate to the Pull Request
   - Click the "Code" button within the PR
   - Select "Open with Codespaces"
   - Create a new codespace or use an existing one

2. **Preview Changes**
   ```bash
   npm install
   npm run dev
   ```

3. **Visual Review**
   - Navigate through the documentation at `http://localhost:3000`
   - Check for formatting issues, broken links, and content accuracy
   - Test the search functionality
   - Verify images and code snippets render correctly

## 🖥️ Local Development

If you prefer to work locally:

### Prerequisites
- Node.js 18.x or higher
- npm or yarn

### Setup
```bash
# Clone the repository
git clone https://github.com/xpander-ai/docs.git
cd docs

# Install dependencies
npm install

# Start the development server
npm run dev
```

The documentation will be available at `http://localhost:3000`.

## 📝 Writing Documentation

### File Structure
- `/docs/` - Main documentation content
- `/tutorials/` - Step-by-step tutorials
- `/workshops/` - Workshop materials
- `/templates/` - Reusable templates
- `/api-reference/` - API documentation
- `/connectors/` - Connector documentation
- `/images/` - Images and screenshots
- `/static/` - Static assets

### MDX Format
Documentation is written in MDX format, which allows you to use React components within Markdown. See [Mintlify's documentation](https://mintlify.com/docs/content/components) for available components.

### Adding New Pages
1. Create a new `.mdx` file in the appropriate directory
2. Add frontmatter with title, description, and icon
3. Update `docs.json` to include the new page in navigation

Example frontmatter:
```yaml
---
title: "Page Title"
description: "Brief description of the page"
icon: "rocket"
---
```

## 🔄 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-docs`)
3. Make your changes
4. Test locally or in Codespaces
5. Commit your changes (`git commit -m 'Add amazing documentation'`)
6. Push to your branch (`git push origin feature/amazing-docs`)
7. Open a Pull Request

## 🛠️ Troubleshooting

### Codespaces Issues
- **Port forwarding not working**: Check the "Ports" tab in the Codespaces terminal
- **Mintlify CLI not found**: Run `npm install -g mintlify@latest`
- **Build errors**: Clear cache with `rm -rf .mintlify` and rebuild

### Common Issues
- **Changes not reflecting**: Hard refresh your browser (Ctrl/Cmd + Shift + R)
- **Search not working**: Rebuild the search index with `npm run build`

## 📞 Support

- Join our [Community Slack](https://join.slack.com/t/xpandercommunity/shared_invite/zt-2mt2xkxkz-omM7f~_h2jcuzFudrYtZQQ)
- Visit our [Developer Discord](https://discord.gg/CUcp4WWh5g)
- Open an issue in this repository

## 📄 License

This documentation is licensed under the MIT License. See the LICENSE file for details.