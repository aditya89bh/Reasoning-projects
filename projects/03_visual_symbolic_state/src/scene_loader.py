"""Scene loading utilities for the visual-to-symbolic state prototype.

The first prototype uses structured JSON scenes instead of raw vision. This
keeps the focus on symbolic state construction before adding perception models.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from .symbolic_state import SceneObject


class SceneLoader:
    """Load structured scene files into scene objects."""

    def load_json(self, path: str | Path) -> Dict:
        """Load a raw scene dictionary from JSON."""

        scene_path = Path(path)
        with scene_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def load_objects(self, path: str | Path) -> List[SceneObject]:
        """Load scene objects from a structured JSON file."""

        raw_scene = self.load_json(path)
        return self.objects_from_scene(raw_scene)

    def objects_from_scene(self, raw_scene: Dict) -> List[SceneObject]:
        """Convert raw scene dictionary into SceneObject instances."""

        objects = []
        for raw_object in raw_scene.get("objects", []):
            objects.append(
                SceneObject(
                    object_id=raw_object["object_id"],
                    object_type=raw_object.get("object_type", "unknown"),
                    attributes=dict(raw_object.get("attributes", {})),
                    position=dict(raw_object.get("position", {})),
                    confidence=float(raw_object.get("confidence", 1.0)),
                )
            )
        return objects

    def episode_id_from_scene(self, raw_scene: Dict, fallback: str = "episode_001") -> str:
        """Return episode id from scene metadata."""

        return raw_scene.get("episode_id", fallback)

    def state_id_from_scene(self, raw_scene: Dict, fallback: str = "state_001") -> str:
        """Return state id from scene metadata."""

        return raw_scene.get("state_id", fallback)
