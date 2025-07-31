# Contributing to xpander.ai Documentation

Thank you for your interest in contributing to xpander.ai documentation! This guide will help you get started quickly.

## 🚀 Quick Start with GitHub Codespaces (Recommended)

The fastest way to contribute is using GitHub Codespaces - no local setup required!

### For New Contributors

1. **Fork the repository**
   - Click the "Fork" button at the top right of this repository

2. **Open in Codespaces**
   - In your forked repository, click the green "Code" button
   - Select the "Codespaces" tab
   - Click "Create codespace on main"

3. **Start developing**
   - Codespaces will automatically set up everything for you
   - Once loaded, run: `npm run dev`
   - Your documentation preview will be available at port 3000

### For Existing Contributors

Simply click: [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/xpander-ai/docs?quickstart=1)

## 📝 Making Changes

### Documentation Structure

- `/docs/` - Main documentation content
- `/tutorials/` - Step-by-step tutorials
- `/workshops/` - Workshop materials
- `/api-reference/` - API documentation
- `/static/images/` - Images and screenshots

### Writing Guidelines

1. **Use MDX format** - Mintlify supports MDX which allows React components in Markdown
2. **Add frontmatter** - Every page needs title, description, and icon
3. **Keep it concise** - Clear, direct communication
4. **Include examples** - Code snippets and real-world use cases
5. **Add screenshots** - Visual aids help understanding

### Testing Your Changes

In your Codespace:
```bash
npm run dev  # Preview changes locally
npm run build  # Build for production
```

## 🔄 Submitting a Pull Request

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Commit your changes**
   ```bash
   git add .
   git commit -m "docs: add documentation for X feature"
   ```

3. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template

## 👀 Review Process

### For Reviewers

All PRs can be reviewed using Codespaces:

1. Navigate to the Pull Request
2. Click the "Code" dropdown
3. Select "Open with Codespaces"
4. Preview the changes live

### What We Look For

- ✅ Clear and accurate content
- ✅ Proper formatting and structure
- ✅ Working links and images
- ✅ Consistent style
- ✅ No build errors

## 🛠️ Development Tips

### Codespaces Shortcuts

- **Preview**: The preview URL appears automatically when you run `npm run dev`
- **Port forwarding**: Codespaces handles this automatically
- **Extensions**: VS Code extensions are pre-configured
- **Terminal**: Use the integrated terminal for all commands

### Common Tasks

**Add a new page:**
1. Create `.mdx` file in appropriate directory
2. Add frontmatter
3. Update navigation in `mint.json`

**Add images:**
1. Place images in `/static/images/`
2. Reference with: `![Alt text](/images/your-image.png)`

**Add code snippets:**
```mdx
```javascript
// Your code here
```