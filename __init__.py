"""TDM-5F — The DeepSeek Moment · 5QLN fractal: plugin registration."""

from pathlib import Path

PLUGIN_ROOT = Path(__file__).parent
SKILL_ROOT = PLUGIN_ROOT / "skills"


def _seed_external_skills_dir(skill_root: Path) -> None:
    """Best-effort: add the plugin's skills/ to skills.external_dirs in
    config.yaml so the prompt builder lists them.

    ctx.register_skill() makes plugin skills loadable by name, but Hermes does
    not list plugin-provided skills in the <available_skills> prompt index by
    default. Seeding the skills/ directory here makes them appear in
    skills_list and the prompt index without a manual `hermes skills tap add`.
    Mirrors the 5qln plugin pattern.
    """
    try:
        from hermes_cli.config import get_config_path, read_raw_config
        from hermes_cli.auth import atomic_yaml_write
    except ImportError:
        return  # Not running inside a Hermes process (e.g. tests, docs)

    try:
        config_path = get_config_path()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config = read_raw_config()

        skills_cfg = config.get("skills")
        if not isinstance(skills_cfg, dict):
            skills_cfg = {}
            config["skills"] = skills_cfg

        existing = skills_cfg.get("external_dirs")
        if isinstance(existing, str):
            existing = [existing]
        elif not isinstance(existing, list):
            existing = []

        target = str(skill_root.resolve())
        if target not in existing:
            existing.append(target)
            skills_cfg["external_dirs"] = existing
            atomic_yaml_write(config_path, config, sort_keys=False)
    except Exception:
        pass  # Best-effort — plugin still works, skill just won't be prompt-visible


def register(ctx):
    """Register the pentagon engine operating skill. No tools or hooks in v0.1.0."""
    for child in sorted(SKILL_ROOT.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            ctx.register_skill(child.name, skill_md)
    _seed_external_skills_dir(SKILL_ROOT)
