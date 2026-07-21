import json
from pathlib import Path

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

register = template.Library()


def _load_manifest():
    build_dir = Path(settings.BASE_DIR) / "static" / "react-build"
    for candidate in [
        build_dir / ".vite" / "manifest.json",
        build_dir / "manifest.json",
    ]:
        if candidate.exists():
            with open(candidate) as f:
                return json.load(f)
    return {}


@register.simple_tag
def vite_js():
    manifest = _load_manifest()
    entry = manifest.get("index.html")
    if not entry:
        return ""
    return static(f"react-build/{entry['file']}")


@register.simple_tag
def vite_css_tags():
    manifest = _load_manifest()
    entry = manifest.get("index.html")
    if not entry or "css" not in entry:
        return ""
    links = "".join(
        f'<link rel="stylesheet" href="{static(f"react-build/{css}")}">'
        for css in entry["css"]
    )
    return mark_safe(links)
