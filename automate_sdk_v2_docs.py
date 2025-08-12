#!/usr/bin/env python3
"""
Automated Documentation Updates for SDK v2.0.0
Automates updates for lifecycle management, schema improvements, 
installation guidance, and API reference enhancements.
"""

import os
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class UpdateConfig:
    """Configuration for documentation updates"""
    version: str = "v2.0.0"
    base_path: Path = Path(".")
    backup_enabled: bool = True
    dry_run: bool = False

class DocumentationUpdater:
    """Main class for automating SDK v2.0.0 documentation updates"""
    
    def __init__(self, config: UpdateConfig):
        self.config = config
        self.updates_applied = []
        self.errors = []
        
    def update_lifecycle_management(self) -> None:
        """Update lifecycle management documentation with v2.0.0 features"""
        logger.info("Updating lifecycle management documentation...")
        
        lifecycle_file = self.config.base_path / "Examples" / "10-lifecycle-management.mdx"
        if not lifecycle_file.exists():
            self.errors.append(f"Lifecycle file not found: {lifecycle_file}")
            return
            
        try:
            content = lifecycle_file.read_text()
            
            # Update SDK version references
            content = re.sub(
                r'pip install "xpander-sdk\[agno\]"',
                'pip install "xpander-sdk[agno]>=2.0.0"',
                content
            )
            
            # Add new v2.0.0 lifecycle features
            new_features = """
@on_boot
async def initialize_agent_versioning():
    \"\"\"Initialize new agent versioning system in v2.0.0.\"\"\"
    global agent_version_manager
    
    print("🔄 Initializing agent versioning...")
    agent_version_manager = {
        "current_version": "2.0.0",
        "draft_enabled": True,
        "deployment_tracking": True
    }
    print("✅ Agent versioning system ready")

@on_boot
async def setup_webhook_system():
    \"\"\"Setup enhanced webhook system with organization-level API keys.\"\"\"
    global webhook_manager
    
    print("🔗 Setting up webhook system...")
    webhook_manager = {
        "org_level_keys": True,
        "enhanced_auth": True,
        "auto_retry": True
    }
    print("✅ Webhook system configured")
"""
            
            # Insert new features before the handle_data_request function
            pattern = r'(@on_task\nasync def handle_data_request)'
            replacement = new_features + "\n" + r'\1'
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            # Update the features section with v2.0.0 improvements
            v2_features = """
## v2.0.0 New Features

<CardGroup cols={2}>
<Card title="Agent Versioning" icon="code-branch">
Complete agent versioning with draft handling and deployment management
</Card>

<Card title="Enhanced Webhooks" icon="webhook">
Organization-level API keys and improved webhook functionality
</Card>

<Card title="Performance Optimizations" icon="gauge-high">
Significant performance improvements across agent workers and API responses
</Card>

<Card title="Memory Management" icon="memory">
Fixed memory leaks and improved garbage collection in long-running sessions
</Card>
</CardGroup>
"""
            
            # Add v2.0.0 features before existing key features
            pattern = r'(## Key Features)'
            replacement = v2_features + "\n" + r'\1'
            content = re.sub(pattern, replacement, content)
            
            if not self.config.dry_run:
                if self.config.backup_enabled:
                    lifecycle_file.rename(f"{lifecycle_file}.backup")
                lifecycle_file.write_text(content)
            
            self.updates_applied.append("Lifecycle management updated with v2.0.0 features")
            logger.info("✅ Lifecycle management documentation updated")
            
        except Exception as e:
            error_msg = f"Failed to update lifecycle management: {str(e)}"
            self.errors.append(error_msg)
            logger.error(error_msg)
    
    def update_schema_improvements(self) -> None:
        """Update API reference with schema improvements"""
        logger.info("Updating schema improvements...")
        
        api_files = [
            "API reference/agents/api-reference/index.mdx",
            "API reference/tools/api-reference/index.mdx", 
            "API reference/events/api-reference/index.mdx"
        ]
        
        for api_file_path in api_files:
            api_file = self.config.base_path / api_file_path
            if not api_file.exists():
                self.errors.append(f"API file not found: {api_file}")
                continue
                
            try:
                content = api_file.read_text()
                
                # Add v2.0.0 schema improvements notice
                schema_notice = """
<Note>
**SDK v2.0.0 Schema Improvements**

This API reference has been updated for SDK v2.0.0 with:
- Enhanced validation for custom tool schemas
- Improved cross-provider compatibility
- New agent versioning system support
- Performance optimizations for large context windows
</Note>
"""
                
                # Insert after the frontmatter
                pattern = r'(---\n.*?---\n)'
                replacement = r'\1\n' + schema_notice
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                
                if not self.config.dry_run:
                    if self.config.backup_enabled:
                        api_file.rename(f"{api_file}.backup")
                    api_file.write_text(content)
                
                self.updates_applied.append(f"Schema improvements added to {api_file_path}")
                
            except Exception as e:
                error_msg = f"Failed to update {api_file_path}: {str(e)}"
                self.errors.append(error_msg)
                logger.error(error_msg)
        
        logger.info("✅ Schema improvements documentation updated")
    
    def update_installation_guidance(self) -> None:
        """Update installation guidance across documentation"""
        logger.info("Updating installation guidance...")
        
        installation_files = [
            "user-guide/quick-start.mdx",
            "Examples/00-setup-deployment.mdx",
            "Examples/01-simple-hello-world.mdx"
        ]
        
        for install_file_path in installation_files:
            install_file = self.config.base_path / install_file_path
            if not install_file.exists():
                self.errors.append(f"Installation file not found: {install_file}")
                continue
                
            try:
                content = install_file.read_text()
                
                # Update pip install commands to v2.0.0
                content = re.sub(
                    r'pip install[^\n]*xpander-sdk[^\n]*',
                    'pip install "xpander-sdk[agno]>=2.0.0"',
                    content
                )
                
                # Add v2.0.0 installation notes
                v2_install_note = """
<Warning>
**SDK v2.0.0 Breaking Changes**

SDK v2.0.0 includes significant architectural changes. Please review the [migration guide](#migration-from-v1x) before upgrading existing projects.

Key changes:
- New agent versioning system
- Enhanced webhook authentication
- Improved memory management
- Performance optimizations
</Warning>
"""
                
                # Add after any existing installation command
                pattern = r'(pip install[^\n]*\n)'
                replacement = r'\1\n' + v2_install_note + '\n'
                content = re.sub(pattern, replacement, content)
                
                if not self.config.dry_run:
                    if self.config.backup_enabled:
                        install_file.rename(f"{install_file}.backup")
                    install_file.write_text(content)
                
                self.updates_applied.append(f"Installation guidance updated in {install_file_path}")
                
            except Exception as e:
                error_msg = f"Failed to update installation in {install_file_path}: {str(e)}"
                self.errors.append(error_msg)
                logger.error(error_msg)
        
        logger.info("✅ Installation guidance updated")
    
    def update_api_reference_enhancements(self) -> None:
        """Update API reference with enhancements and new endpoints"""
        logger.info("Updating API reference enhancements...")
        
        # Update main API reference index
        api_index = self.config.base_path / "API reference" / "index.mdx"
        if api_index.exists():
            try:
                content = api_index.read_text()
                
                # Add v2.0.0 API enhancements section
                api_enhancements = """
## SDK v2.0.0 API Enhancements

<CardGroup cols={3}>
<Card title="Agent Versioning API" icon="code-branch" href="/API reference/agents/api-reference/versioning">
New endpoints for managing agent versions, drafts, and deployments
</Card>

<Card title="Enhanced Webhooks" icon="webhook" href="/API reference/events/api-reference/webhooks">
Organization-level API keys and improved webhook management
</Card>

<Card title="Performance Metrics" icon="chart-line" href="/API reference/backend/metrics">
New endpoints for monitoring agent performance and resource usage
</Card>

<Card title="Knowledge Base CRUD" icon="database" href="/API reference/knowledge/api-reference/crud">
Advanced CRUD operations with OCR support and improved document processing
</Card>

<Card title="Custom Workers" icon="server" href="/API reference/backend/workers">
Kubernetes cluster support for custom workers with advanced logging
</Card>

<Card title="Authentication v2" icon="shield-check" href="/API reference/auth/v2">
New authentication system with improved security and performance
</Card>
</CardGroup>
"""
                
                # Add enhancements after the main title
                pattern = r'(# API Reference\n)'
                replacement = r'\1\n' + api_enhancements + '\n'
                content = re.sub(pattern, replacement, content)
                
                if not self.config.dry_run:
                    if self.config.backup_enabled:
                        api_index.rename(f"{api_index}.backup")
                    api_index.write_text(content)
                
                self.updates_applied.append("API reference index updated with v2.0.0 enhancements")
                
            except Exception as e:
                error_msg = f"Failed to update API reference index: {str(e)}"
                self.errors.append(error_msg)
                logger.error(error_msg)
        
        logger.info("✅ API reference enhancements updated")
    
    def update_changelog(self) -> None:
        """Ensure changelog is up to date with v2.0.0 features"""
        logger.info("Validating changelog for v2.0.0...")
        
        changelog_file = self.config.base_path / "changelog" / "product-updates.mdx"
        if changelog_file.exists():
            content = changelog_file.read_text()
            
            if "SDK v2.0.0" in content:
                logger.info("✅ Changelog already contains v2.0.0 updates")
                self.updates_applied.append("Changelog validation passed")
            else:
                self.errors.append("Changelog missing SDK v2.0.0 entry")
        else:
            self.errors.append("Changelog file not found")
    
    def run_all_updates(self) -> Dict[str, Any]:
        """Run all documentation updates"""
        logger.info(f"Starting SDK v2.0.0 documentation updates (dry_run: {self.config.dry_run})")
        
        # Run all update methods
        self.update_lifecycle_management()
        self.update_schema_improvements()
        self.update_installation_guidance()
        self.update_api_reference_enhancements()
        self.update_changelog()
        
        # Generate summary report
        summary = {
            "version": self.config.version,
            "updates_applied": len(self.updates_applied),
            "errors": len(self.errors),
            "dry_run": self.config.dry_run,
            "details": {
                "updates": self.updates_applied,
                "errors": self.errors
            }
        }
        
        return summary
    
    def generate_report(self, summary: Dict[str, Any]) -> None:
        """Generate a detailed report of the updates"""
        report_file = self.config.base_path / f"sdk_v2_update_report.json"
        
        if not self.config.dry_run:
            with open(report_file, 'w') as f:
                json.dump(summary, f, indent=2)
        
        # Print summary
        print("\n" + "="*60)
        print(f"SDK v2.0.0 Documentation Update Summary")
        print("="*60)
        print(f"Version: {summary['version']}")
        print(f"Updates Applied: {summary['updates_applied']}")
        print(f"Errors: {summary['errors']}")
        print(f"Dry Run: {summary['dry_run']}")
        
        if summary['details']['updates']:
            print(f"\n✅ Successfully Applied Updates:")
            for update in summary['details']['updates']:
                print(f"  • {update}")
        
        if summary['details']['errors']:
            print(f"\n❌ Errors Encountered:")
            for error in summary['details']['errors']:
                print(f"  • {error}")
        
        print(f"\nReport saved to: {report_file}")
        print("="*60)

def main():
    """Main function to run the documentation automation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automate SDK v2.0.0 documentation updates")
    parser.add_argument("--dry-run", action="store_true", help="Run without making changes")
    parser.add_argument("--no-backup", action="store_true", help="Disable backup creation")
    parser.add_argument("--base-path", type=str, default=".", help="Base path for documentation")
    
    args = parser.parse_args()
    
    config = UpdateConfig(
        dry_run=args.dry_run,
        backup_enabled=not args.no_backup,
        base_path=Path(args.base_path)
    )
    
    updater = DocumentationUpdater(config)
    summary = updater.run_all_updates()
    updater.generate_report(summary)
    
    # Exit with error code if there were errors
    exit_code = 1 if summary['errors'] > 0 else 0
    return exit_code

if __name__ == "__main__":
    exit(main())