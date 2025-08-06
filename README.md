# xpander.ai Documentation

This repository contains the documentation for xpander.ai, built with [Mintlify](https://mintlify.com).

🌐 **Live Documentation**: https://docs.xpander.ai

## 🚀 Getting Started

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

### Available Commands

| Command | Description |
|---------|-------------|
| `npm install` | Install dependencies (including Mintlify CLI) |
| `npm run dev` | Start the development server with hot reload |
| `npm run build` | Build the documentation for production |
| `npm run preview` | Preview the production build locally |

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

### Contributing Steps

1. Fork the repository
2. Clone your fork locally
3. Make your changes in your local development environment
4. Test your changes with `npm run dev`
5. Commit and push your changes
6. Open a Pull Request

For contribution guidelines, please refer to our community Slack or Discord channels listed in the documentation.

## 🛠️ Troubleshooting

### Common Issues
- **Changes not reflecting**: Hard refresh your browser (Ctrl/Cmd + Shift + R)
- **Search not working**: Rebuild the search index with `npm run build`
- **Mintlify CLI not found**: Run `npm install -g mintlify@latest`
- **Build errors**: Clear cache with `rm -rf .mintlify` and rebuild

## 📞 Support

- Join our [Community Slack](https://join.slack.com/t/xpandercommunity/shared_invite/zt-2mt2xkxkz-omM7f~_h2jcuzFudrYtZQQ)
- Visit our [Developer Discord](https://discord.gg/CUcp4WWh5g)
- Open an issue in this repository

## 📄 License

This documentation is licensed under the MIT License. See the LICENSE file for details.