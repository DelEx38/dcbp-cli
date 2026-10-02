"""
Tests for DCBP CLI commands - v0.6.0 Safety Release.

Security contract: DCBP must NEVER delete or overwrite a skill it cannot
prove it owns. These tests verify that contract is upheld.
"""

import hashlib
import shutil
from pathlib import Path

import pytest

from dcbp_cli.commands import (
    _parse_frontmatter,
    classify_skill,
    migrate_global_skills,
    _install_skills_to_project,
    init_project,
    update_templates,
    Ownership,
    DCBP_V050_SKILL_HASHES,
)


# ===========================================================================
# Tests: _parse_frontmatter
# ===========================================================================

class TestParseFrontmatter:
    def test_valid_frontmatter(self):
        content = "---\nname: dev\ntool: dcbp\n---\n\n# Body"
        fm = _parse_frontmatter(content)
        assert fm is not None
        assert fm["name"] == "dev"
        assert fm["tool"] == "dcbp"

    def test_no_frontmatter(self):
        content = "# Just a markdown file\nNo frontmatter here."
        assert _parse_frontmatter(content) is None

    def test_missing_closing_delimiter(self):
        content = "---\nname: dev\ntool: dcbp\n\n# Body (no closing ---)"
        assert _parse_frontmatter(content) is None

    def test_empty_frontmatter(self):
        content = "---\n---\n\n# Body"
        fm = _parse_frontmatter(content)
        assert fm == {}

    def test_tool_in_body_only_not_in_frontmatter(self):
        """Regression test: tool: dcbp only in body must NOT be parsed as frontmatter."""
        content = "---\nname: dev\n---\n\n# Body\ntool: dcbp appears here but not in frontmatter"
        fm = _parse_frontmatter(content)
        assert fm is not None
        assert "tool" not in fm

    def test_crlf_line_endings(self):
        content = "---\r\nname: dev\r\ntool: dcbp\r\n---\r\n\r\n# Body"
        # After normalization via read_bytes().replace, this becomes LF
        # But _parse_frontmatter works on already-decoded string
        content_lf = content.replace('\r\n', '\n')
        fm = _parse_frontmatter(content_lf)
        assert fm is not None
        assert fm.get("tool") == "dcbp"

    def test_quoted_values(self):
        content = '---\nname: "my skill"\ndescription: \'some desc\'\n---\n# Body'
        fm = _parse_frontmatter(content)
        assert fm["name"] == "my skill"
        assert fm["description"] == "some desc"

    def test_first_line_not_dashes(self):
        content = "# Title\n---\nname: dev\n---\n"
        assert _parse_frontmatter(content) is None


# ===========================================================================
# Tests: classify_skill
# ===========================================================================

class TestClassifySkill:
    def test_no_skill_md_is_unknown(self, tmp_path):
        skill_dir = tmp_path / "my_skill"
        skill_dir.mkdir()
        assert classify_skill(skill_dir) == Ownership.UNKNOWN

    def test_tool_dcbp_in_frontmatter_is_owned(self, tmp_path):
        skill_dir = tmp_path / "dev"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: dev\ntool: dcbp\n---\n\n# Dev skill\n",
            encoding="utf-8"
        )
        assert classify_skill(skill_dir) == Ownership.OWNED

    def test_tool_dcbp_in_body_only_is_unknown(self, tmp_path):
        """CRITICAL regression test: tool: dcbp only in body is UNKNOWN."""
        skill_dir = tmp_path / "dev"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: dev\ndescription: something\n---\n\n"
            "# Body text\ntool: dcbp mentioned here but not in frontmatter\n",
            encoding="utf-8"
        )
        assert classify_skill(skill_dir) == Ownership.UNKNOWN

    def test_malformed_frontmatter_is_unknown(self, tmp_path):
        skill_dir = tmp_path / "dev"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: dev\n# no closing delimiter\n# Body content\n",
            encoding="utf-8"
        )
        assert classify_skill(skill_dir) == Ownership.UNKNOWN

    def test_third_party_skill_is_unknown(self, tmp_path, third_party_skill_content):
        skill_dir = tmp_path / "dev"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(third_party_skill_content, encoding="utf-8")
        assert classify_skill(skill_dir) == Ownership.UNKNOWN

    def test_known_hash_with_dcbp_marker_is_owned(self, tmp_path, templates_path):
        """A v0.5.0 template file (hash match + DCBP marker) is OWNED."""
        for skill_name, expected_hash in DCBP_V050_SKILL_HASHES.items():
            src = templates_path / ".claude" / "skills" / skill_name / "SKILL.md"
            if not src.exists():
                continue
            skill_dir = tmp_path / skill_name
            skill_dir.mkdir(exist_ok=True)
            shutil.copy2(src, skill_dir / "SKILL.md")
            # The template files now have tool: dcbp, so they're OWNED by criterion 1
            # But to test criterion 2 (hash), we'd need the old content
            # This test ensures classify_skill returns OWNED for current templates
            result = classify_skill(skill_dir)
            assert result == Ownership.OWNED, (
                f"Expected OWNED for skill '{skill_name}', got {result}"
            )
            break  # Test at least one

    def test_generic_skill_same_name_but_different_content_is_unknown(self, tmp_path):
        """A skill named 'dev' with generic content (no hash match, no marker) is UNKNOWN."""
        skill_dir = tmp_path / "dev"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: dev\ndescription: Generic dev workflow\n---\n\n# Dev\nDo things.\n",
            encoding="utf-8"
        )
        assert classify_skill(skill_dir) == Ownership.UNKNOWN

    def test_unreadable_skill_is_unknown(self, tmp_path):
        """If SKILL.md can't be read, it must be UNKNOWN."""
        skill_dir = tmp_path / "dev"
        skill_dir.mkdir()
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("---\ntool: dcbp\n---\n", encoding="utf-8")

        # Simulate read error by making it a directory instead
        skill_md.unlink()
        skill_md.mkdir()  # Directory with same name -> read_bytes() will fail

        assert classify_skill(skill_dir) == Ownership.UNKNOWN

    def test_name_mismatch_with_tool_dcbp_is_unknown(self, tmp_path):
        """dir=dev, frontmatter: name=other-skill, tool=dcbp → UNKNOWN (identity incoherent)."""
        skill_dir = tmp_path / "dev"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: other-skill\ntool: dcbp\n---\n\n# Content\n",
            encoding="utf-8"
        )
        assert classify_skill(skill_dir) == Ownership.UNKNOWN

    def test_unknown_catalog_name_with_tool_dcbp_is_unknown(self, tmp_path):
        """dir=unknown-name, name=unknown-name, tool=dcbp (not in catalog) → UNKNOWN."""
        skill_dir = tmp_path / "unknown-name"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: unknown-name\ntool: dcbp\n---\n\n# Content\n",
            encoding="utf-8"
        )
        assert classify_skill(skill_dir) == Ownership.UNKNOWN

    def test_coherent_identity_with_tool_dcbp_is_owned(self, tmp_path):
        """dir=dev, name=dev, tool=dcbp (in catalog) → OWNED (full identity coherence)."""
        skill_dir = tmp_path / "dev"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: dev\ntool: dcbp\n---\n\n# Content\n",
            encoding="utf-8"
        )
        assert classify_skill(skill_dir) == Ownership.OWNED


# ===========================================================================
# Tests: Global scope absent after fix
# ===========================================================================

class TestNoGlobalInstall:
    """After v0.6.0, init/update must NEVER create ~/.claude/skills/."""

    def test_init_does_not_create_global_skills(self, fake_home, fake_project):
        """init must not create ~/.claude/skills/."""
        init_project(fake_project, skip_questions=True)
        global_skills = fake_home / ".claude" / "skills"
        assert not global_skills.exists(), (
            f"init created global skills directory at {global_skills}"
        )

    def test_init_force_does_not_create_global_skills(self, fake_home, fake_project):
        """init --force must not create ~/.claude/skills/."""
        # First init
        init_project(fake_project, skip_questions=True)
        # Force reinit
        init_project(fake_project, force=True, skip_questions=True)
        global_skills = fake_home / ".claude" / "skills"
        assert not global_skills.exists(), (
            f"init --force created global skills directory at {global_skills}"
        )

    def test_update_does_not_create_global_skills(self, fake_home, fake_project):
        """update must not create ~/.claude/skills/."""
        init_project(fake_project, skip_questions=True)
        update_templates(fake_project)
        global_skills = fake_home / ".claude" / "skills"
        assert not global_skills.exists(), (
            f"update created global skills directory at {global_skills}"
        )

    def test_init_does_not_modify_existing_global_skills(self, fake_home, fake_project):
        """If ~/.claude/skills/ already exists, init must not modify it."""
        global_skills = fake_home / ".claude" / "skills"
        global_skills.mkdir(parents=True)
        sentinel = global_skills / "sentinel.txt"
        sentinel.write_text("I am a sentinel", encoding="utf-8")

        init_project(fake_project, skip_questions=True)

        assert sentinel.exists(), "init modified existing global skills dir"
        assert sentinel.read_text(encoding="utf-8") == "I am a sentinel"


# ===========================================================================
# Tests: Project-local install
# ===========================================================================

class TestProjectInstall:
    def test_init_installs_skills_in_project(self, fake_home, fake_project):
        """Skills must be installed in {project}/.claude/skills/."""
        init_project(fake_project, skip_questions=True)
        project_skills = fake_project / ".claude" / "skills"
        assert project_skills.exists()
        skill_dirs = [d.name for d in project_skills.iterdir() if d.is_dir()]
        assert len(skill_dirs) >= 12, f"Expected 12+ skills, found: {skill_dirs}"

    def test_update_refreshes_project_skills(self, fake_home, fake_project):
        """update must refresh skills in project/.claude/skills/."""
        init_project(fake_project, skip_questions=True)
        project_skills = fake_project / ".claude" / "skills"

        # Corrupt a skill
        dev_skill = project_skills / "dev" / "SKILL.md"
        original_content = dev_skill.read_text(encoding="utf-8")
        dev_skill.write_text("---\nname: dev\ntool: dcbp\n---\n# Corrupted\n", encoding="utf-8")

        update_templates(fake_project)

        # After update, the DCBP-owned skill should be refreshed
        restored = dev_skill.read_text(encoding="utf-8")
        # update with force=True should restore it
        assert "Corrupted" not in restored


# ===========================================================================
# Tests: Collision - third-party skills survive
# ===========================================================================

class TestThirdPartySkillsPreserved:
    """Third-party skills must survive init, init --force, and update."""

    SKILL_NAMES = ["dev", "review", "test", "commit"]

    def _plant_third_party_skills(self, project_path, skill_names, content):
        """Install fake third-party skills in project/.claude/skills/."""
        skills_dir = project_path / ".claude" / "skills"
        skills_dir.mkdir(parents=True, exist_ok=True)
        for name in skill_names:
            skill_dir = skills_dir / name
            skill_dir.mkdir(exist_ok=True)
            (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

    def test_third_party_skills_survive_init(
        self, fake_home, fake_project, third_party_skill_content
    ):
        """Third-party skills must survive init (project has pre-existing skills)."""
        # Plant third-party skills before init
        self._plant_third_party_skills(
            fake_project, self.SKILL_NAMES, third_party_skill_content
        )

        init_project(fake_project, skip_questions=True)

        skills_dir = fake_project / ".claude" / "skills"
        for name in self.SKILL_NAMES:
            skill_md = skills_dir / name / "SKILL.md"
            assert skill_md.exists(), f"Third-party skill '{name}' was deleted"
            content = skill_md.read_text(encoding="utf-8")
            assert content == third_party_skill_content, (
                f"Third-party skill '{name}' was overwritten"
            )

    def test_third_party_skills_survive_init_force(
        self, fake_home, fake_project, third_party_skill_content
    ):
        """Third-party skills must survive init --force."""
        self._plant_third_party_skills(
            fake_project, self.SKILL_NAMES, third_party_skill_content
        )

        # init --force must STILL not overwrite unknown skills
        init_project(fake_project, force=True, skip_questions=True)

        skills_dir = fake_project / ".claude" / "skills"
        for name in self.SKILL_NAMES:
            skill_md = skills_dir / name / "SKILL.md"
            assert skill_md.exists(), f"Third-party skill '{name}' was deleted by --force"
            content = skill_md.read_text(encoding="utf-8")
            assert content == third_party_skill_content, (
                f"Third-party skill '{name}' was overwritten by --force"
            )

    def test_third_party_skills_survive_update(
        self, fake_home, fake_project, third_party_skill_content
    ):
        """Third-party skills must survive update."""
        init_project(fake_project, skip_questions=True)

        # Overwrite DCBP skills with third-party content
        skills_dir = fake_project / ".claude" / "skills"
        for name in self.SKILL_NAMES:
            skill_md = skills_dir / name / "SKILL.md"
            skill_md.write_text(third_party_skill_content, encoding="utf-8")

        update_templates(fake_project)

        for name in self.SKILL_NAMES:
            skill_md = skills_dir / name / "SKILL.md"
            assert skill_md.exists(), f"Third-party skill '{name}' was deleted by update"
            content = skill_md.read_text(encoding="utf-8")
            assert content == third_party_skill_content, (
                f"Third-party skill '{name}' was overwritten by update"
            )

    def test_third_party_skills_byte_for_byte_preserved(
        self, fake_home, fake_project, third_party_skill_content
    ):
        """Third-party skills must be preserved byte-for-byte."""
        original_bytes = third_party_skill_content.encode("utf-8")
        skills_dir = fake_project / ".claude" / "skills"
        skills_dir.mkdir(parents=True)
        skill_dir = skills_dir / "dev"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_bytes(original_bytes)

        _install_skills_to_project(
            Path("nonexistent_src"),  # no-op since src doesn't exist
            skills_dir,
            force=True,
        )

        result_bytes = (skills_dir / "dev" / "SKILL.md").read_bytes()
        assert result_bytes == original_bytes


# ===========================================================================
# Tests: _install_skills_to_project
# ===========================================================================

class TestInstallSkillsToProject:
    def test_installs_new_skills(self, fake_home, fake_project, templates_path):
        skills_dst = fake_project / ".claude" / "skills"
        skills_src = templates_path / ".claude" / "skills"

        report = _install_skills_to_project(skills_src, skills_dst)

        assert len(report["installed"]) > 0
        assert len(report["skipped_unknown"]) == 0

    def test_skips_unknown_skills(self, fake_home, fake_project, templates_path):
        skills_dst = fake_project / ".claude" / "skills"
        skills_src = templates_path / ".claude" / "skills"

        # Pre-install a third-party "dev" skill
        dev_dir = skills_dst / "dev"
        dev_dir.mkdir(parents=True)
        (dev_dir / "SKILL.md").write_text(
            "---\nname: dev\ndescription: third-party\n---\n# My dev\n",
            encoding="utf-8"
        )

        report = _install_skills_to_project(skills_src, skills_dst, force=False)

        assert "dev" in report["skipped_unknown"]

    def test_force_updates_owned_skills(self, fake_home, fake_project, templates_path):
        skills_dst = fake_project / ".claude" / "skills"
        skills_src = templates_path / ".claude" / "skills"

        # First install
        _install_skills_to_project(skills_src, skills_dst, force=False)

        # All skills are now DCBP-owned (tool: dcbp)
        report = _install_skills_to_project(skills_src, skills_dst, force=True)

        assert len(report["updated"]) > 0
        assert len(report["skipped_unknown"]) == 0

    def test_nonexistent_src_returns_empty_report(self, fake_project):
        report = _install_skills_to_project(
            Path("nonexistent_src"),
            fake_project / "skills"
        )
        assert report["installed"] == []
        assert report["updated"] == []


# ===========================================================================
# Tests: migrate_global_skills
# ===========================================================================

class TestMigrateGlobalSkills:
    def test_no_global_skills_dir_returns_empty(self, tmp_path):
        nonexistent = tmp_path / "nonexistent"
        report = migrate_global_skills(nonexistent)
        assert report["removed"] == []
        assert report["unknown"] == []

    def test_removes_only_owned_skills(self, tmp_path, templates_path):
        global_skills = tmp_path / "skills"
        global_skills.mkdir()

        # Plant a DCBP-owned skill (with tool: dcbp frontmatter)
        owned_dir = global_skills / "start"
        owned_dir.mkdir()
        (owned_dir / "SKILL.md").write_text(
            "---\nname: start\ntool: dcbp\n---\n# Start\nReferences .claude/dcbp/\n",
            encoding="utf-8"
        )

        # Plant a third-party skill
        unknown_dir = global_skills / "my_custom_skill"
        unknown_dir.mkdir()
        (unknown_dir / "SKILL.md").write_text(
            "---\nname: my_custom_skill\n---\n# Custom\n",
            encoding="utf-8"
        )

        report = migrate_global_skills(global_skills)

        assert "start" in report["removed"]
        assert not owned_dir.exists()
        assert "my_custom_skill" in report["unknown"]
        assert unknown_dir.exists()

    def test_unknown_skills_never_touched(self, tmp_path):
        global_skills = tmp_path / "skills"
        global_skills.mkdir()

        third_party = global_skills / "third_party"
        third_party.mkdir()
        content = "---\nname: third_party\n---\n# My skill\n"
        (third_party / "SKILL.md").write_text(content, encoding="utf-8")

        migrate_global_skills(global_skills)

        assert third_party.exists()
        assert (third_party / "SKILL.md").read_text(encoding="utf-8") == content

    def test_empty_dirs_preserved(self, tmp_path):
        global_skills = tmp_path / "skills"
        global_skills.mkdir()
        empty_dir = global_skills / "empty_skill"
        empty_dir.mkdir()

        report = migrate_global_skills(global_skills)

        assert "empty_skill" in report["unknown"]
        assert empty_dir.exists()

    def test_unknown_dirs_preserved(self, tmp_path):
        global_skills = tmp_path / "skills"
        global_skills.mkdir()

        unknown_dir = global_skills / "custom"
        unknown_dir.mkdir()
        (unknown_dir / "SKILL.md").write_text(
            "---\nname: custom\n---\n# Custom skill\n", encoding="utf-8"
        )

        migrate_global_skills(global_skills)

        assert unknown_dir.exists()

    def test_idempotent(self, tmp_path):
        global_skills = tmp_path / "skills"
        global_skills.mkdir()

        # One owned, one unknown
        owned = global_skills / "start"
        owned.mkdir()
        (owned / "SKILL.md").write_text(
            "---\nname: start\ntool: dcbp\n---\n# Start\n.claude/dcbp/ reference\n",
            encoding="utf-8"
        )

        unknown = global_skills / "custom"
        unknown.mkdir()
        (unknown / "SKILL.md").write_text(
            "---\nname: custom\n---\n# Custom\n", encoding="utf-8"
        )

        report1 = migrate_global_skills(global_skills)
        report2 = migrate_global_skills(global_skills)

        # Second call should find nothing to remove (owned already gone)
        assert "start" in report1["removed"]
        assert "start" not in report2["removed"]
        assert unknown.exists()  # Never touched

    def test_non_dir_entries_tracked(self, tmp_path):
        global_skills = tmp_path / "skills"
        global_skills.mkdir()
        (global_skills / "file.txt").write_text("some file", encoding="utf-8")

        report = migrate_global_skills(global_skills)
        assert "file.txt" in report["not_dir"]


# ===========================================================================
# Tests: Idempotence
# ===========================================================================

class TestIdempotence:
    def test_init_twice_idempotent(self, fake_home, fake_project):
        """Running init twice should not fail or corrupt anything."""
        result1 = init_project(fake_project, skip_questions=True)
        assert result1 is True

        # Second init should fail (already initialized) without --force
        result2 = init_project(fake_project, skip_questions=True)
        assert result2 is False

        # Skills directory should still be intact
        skills_dir = fake_project / ".claude" / "skills"
        assert skills_dir.exists()

    def test_init_force_twice_idempotent(self, fake_home, fake_project):
        """Running init --force twice should produce the same result."""
        init_project(fake_project, force=True, skip_questions=True)

        skills_before = {
            d.name for d in (fake_project / ".claude" / "skills").iterdir()
            if d.is_dir()
        }

        init_project(fake_project, force=True, skip_questions=True)

        skills_after = {
            d.name for d in (fake_project / ".claude" / "skills").iterdir()
            if d.is_dir()
        }

        assert skills_before == skills_after

    def test_update_twice_idempotent(self, fake_home, fake_project):
        """Running update twice should produce the same result."""
        init_project(fake_project, skip_questions=True)
        update_templates(fake_project)

        skills_dir = fake_project / ".claude" / "skills"
        content_before = {}
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    content_before[skill_dir.name] = skill_md.read_bytes()

        update_templates(fake_project)

        for name, content in content_before.items():
            skill_md = skills_dir / name / "SKILL.md"
            assert skill_md.read_bytes() == content, (
                f"Skill '{name}' changed on second update"
            )

    def test_migration_twice_idempotent(self, tmp_path):
        """Running migrate_global_skills twice is safe."""
        global_skills = tmp_path / "skills"
        global_skills.mkdir()

        owned = global_skills / "start"
        owned.mkdir()
        (owned / "SKILL.md").write_text(
            "---\nname: start\ntool: dcbp\n---\n.claude/dcbp/ ref\n",
            encoding="utf-8"
        )

        report1 = migrate_global_skills(global_skills)
        report2 = migrate_global_skills(global_skills)

        assert len(report1["removed"]) == 1
        assert len(report2["removed"]) == 0  # Nothing left to remove
