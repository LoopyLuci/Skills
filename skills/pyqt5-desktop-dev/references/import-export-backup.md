# Import/Export & Backup

## Project Import/Export

```python
# import_export.py - Bulk project operations

class ProjectImporter:
    """Handles importing projects from various formats."""
    
    def import_from_json(self, data: dict, new_id: Optional[str] = None) -> Project:
        """Import a project from JSON data."""
        errors = validate_project(data)
        if errors:
            raise ValidationError("import", "; ".join(errors))
        project = Project.from_dict(data)
        self.project_manager.save(project)
        return project
    
    def import_from_file(self, path: Path, new_id: Optional[str] = None) -> Project:
        """Import a project from a JSON file."""
    
    def import_from_zip(self, path: Path, extract_dir: Optional[Path] = None) -> list[Project]:
        """Import projects from a ZIP archive."""

class ProjectExporter:
    """Handles exporting projects to various formats."""
    
    def export_to_json(self, project_id: str, output_path: Optional[Path] = None) -> Path:
        """Export a project to JSON file."""
    
    def export_to_zip(self, project_ids: list[str], output_path: Optional[Path] = None) -> Path:
        """Export multiple projects to a ZIP archive."""
    
    def export_all(self, output_path: Optional[Path] = None) -> Path:
        """Export all projects to a ZIP archive."""
```

## Backup Manager

```python
class BackupManager:
    """Manages automated backups with scheduling."""
    
    def create_backup(self, project_manager: ProjectManager, name: Optional[str] = None) -> Path:
        """Create a full backup of all projects."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = name or f"backup_{timestamp}"
        backup_path = self.backup_dir / name
        # Copy all project JSON files
    
    def restore_backup(self, backup_path: Path, project_manager: ProjectManager) -> int:
        """Restore projects from a backup."""
    
    def list_backups(self) -> list[dict]:
        """List all available backups."""
    
    def delete_backup(self, name: str) -> bool:
        """Delete a backup."""
    
    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        """Remove old backups, keeping only the most recent ones."""
```

## Storage Structure

```
~/.webbuilder/
  projects/           # Active projects
    project-xxx.json
  backups/
    backup_20260901_120000/
      project-xxx.json
      project-yyy.json
  exports/
    project-xxx.json
    projects_20260901.zip
  feedback/
    fb-xxxxxxxx.json
  session_id          # Anonymous session identifier
```

## Import/Export Checklist

- [ ] Import from JSON (single project)
- [ ] Import from ZIP (bulk)
- [ ] Export to JSON (single project)
- [ ] Export to ZIP (bulk)
- [ ] Export all projects
- [ ] Create backup
- [ ] Restore from backup
- [ ] List backups
- [ ] Cleanup old backups
- [ ] Validate before import
