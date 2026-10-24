"""Frozen functional, adversarial mutation and real CLI oracles."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.slug import slugify


class FunctionalSlugTests(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(slugify("Hola Mundo"), "hola-mundo")

    def test_separators(self):
        self.assertEqual(slugify("uno___dos... tres"), "uno-dos-tres")

    def test_accents(self):
        self.assertEqual(slugify("\u00c1rbol y ping\u00fcino"), "arbol-y-pinguino")

    def test_edges(self):
        self.assertEqual(slugify("  --Hola--  "), "hola")

    def test_numbers(self):
        self.assertEqual(slugify("Versi\u00f3n 2026"), "version-2026")

    def test_limit(self):
        self.assertEqual(slugify("A" * 64), "a" * 64)

    def test_blank(self):
        for text in ("", "   ", "!?___"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                slugify(text)

    def test_too_long(self):
        with self.assertRaises(ValueError):
            slugify("a" * 65)

    def test_no_ascii(self):
        with self.assertRaises(ValueError):
            slugify("\u4f60\u597d")


class AdversarialSlugTests(unittest.TestCase):
    def test_wrong_types(self):
        for value in (None, 42, False, [], {}, b"hola"):
            with self.subTest(value=value), self.assertRaises(TypeError):
                slugify(value)

    def test_path_input(self):
        self.assertEqual(slugify("../../Admin\\root"), "admin-root")

    def test_combining_unicode(self):
        self.assertEqual(slugify("cafe\u0301"), "cafe")

    def test_repeatable(self):
        text = "Prueba 24"
        self.assertEqual(slugify(text), "prueba-24")
        self.assertEqual(slugify(text), slugify(text))
        self.assertEqual(text, "Prueba 24")

    def test_utf8_diagnostics_under_legacy_locale(self):
        script = (
            "import locale, runpy, sys\n"
            "locale.getencoding = lambda: 'cp1252'\n"
            "sys.argv = ['unittest', "
            "'tests.test_slug.AdversarialSlugTests.test_identity_mutant_rejected', "
            "'tests.test_slug.AdversarialSlugTests.test_constant_mutant_rejected', "
            "'tests.test_slug.AdversarialSlugTests.test_no_normalization_mutant_rejected']\n"
            "runpy.run_module('unittest', run_name='__main__')\n"
        )
        result = subprocess.run(
            [sys.executable, "-X", "utf8=0", "-c", script], cwd=ROOT,
            capture_output=True, text=True, encoding="utf-8", errors="strict",
            timeout=30,
            env={**os.environ, "PYTHONUTF8": "0", "PYTHONIOENCODING": "utf-8"},
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Ran 3 tests", result.stderr)
        self.assertIn("OK", result.stderr)
        self.assertNotIn("UnicodeDecodeError", result.stderr)

    def _assert_mutant_rejected(self, source):
        with tempfile.TemporaryDirectory(prefix="kdd-slug-mutant-") as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "tests").mkdir()
            (root / "src/__init__.py").write_text("", encoding="utf-8")
            (root / "tests/__init__.py").write_text("", encoding="utf-8")
            (root / "src/slug.py").write_text(source, encoding="utf-8")
            (root / "tests/test_slug.py").write_bytes(Path(__file__).read_bytes())
            result = subprocess.run(
                [sys.executable, "-m", "unittest", "tests.test_slug.FunctionalSlugTests"],
                cwd=root, capture_output=True, text=True, timeout=20,
                encoding="utf-8", errors="strict",
                env={**os.environ, "PYTHONUTF8": "1"},
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("Ran 9 tests", result.stderr)
            self.assertIn("FAILED (", result.stderr)
            self.assertIn("AssertionError", result.stderr)
            for environmental in ("ImportError", "ModuleNotFoundError", "SyntaxError"):
                self.assertNotIn(environmental, result.stderr)

    def test_identity_mutant_rejected(self):
        self._assert_mutant_rejected("def slugify(text):\n    return text\n")

    def test_constant_mutant_rejected(self):
        self._assert_mutant_rejected("def slugify(text):\n    return 'hola-mundo'\n")

    def test_no_normalization_mutant_rejected(self):
        self._assert_mutant_rejected(
            "import re\ndef slugify(text):\n"
            "    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')\n"
        )


class SlugCliTests(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, "src/slug.py", *args], cwd=ROOT,
            capture_output=True, text=True, timeout=10,
            encoding="utf-8", errors="strict",
            env={**os.environ, "PYTHONUTF8": "1"},
        )

    def test_success(self):
        result = self._run("Hola Mundo")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "hola-mundo\n")
        self.assertEqual(result.stderr, "")

    def test_unicode(self):
        result = self._run("\u00c1rbol 2026")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "arbol-2026\n")

    def test_blank_error(self):
        result = self._run("   ")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_argument(self):
        result = self._run()
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_extra_argument(self):
        result = self._run("uno", "dos")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
