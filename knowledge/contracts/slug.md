---
type: 'Task Contract'
title: 'Normalizar titulos mediante una CLI'
description: 'Crear slugs ASCII deterministas con errores claros y oraculos funcionales, adversariales y de CLI.'
tags: ['product', 'slug', 'cli']
task: slug
intent: 'Normalizar un titulo y exponer el comportamiento mediante CLI.'
target: src/slug.py
language: python
signature: 'def slugify(text: str) -> str:'
test_command: 'python -m unittest tests/test_slug.py'
budget:
  cyclomatic_max: 6
  nesting_max: 2
  lines_max: 80
  params_max: 1
tests: tests/test_slug.py
tests_sha256: '0d11f171d0f610a0d96be736b88bedddc107e6e383c1c5ae3200a8913fc4836e'
touch_only: ['src/slug.py']
deps_allowed: ['stdlib']
forbids: ['network', 'subprocess', 'llm']
---

## Intent
Implementar el [producto de demostracion](../slug-demo.md) para verificar
el bootstrap real, la tarea del tablero y la calidad obligatoria en CI.

## Interface
`slugify(text: str) -> str` y `python src/slug.py "Titulo"`.
Comportamiento y errores definidos en el [nodo de producto](../slug-demo.md).

## Invariants
- Funcion pura, resultado ASCII determinista, sin truncamiento.
- CLI con codigos y canales de salida definidos por el producto.
- El oraculo y este contrato permanecen iguales al baseline aprobado.
- El implementador cambia solo src/slug.py; el coordinador registra la tarea.

## Examples
- "Hola Mundo" -> "hola-mundo".
- "Arbol 2026" -> "arbol-2026".
- Entrada vacia o slug de 65 caracteres -> ValueError.

## Do / Don't
- DO ejecutar las pruebas reales y las mutaciones aisladas.
- DON'T editar el oraculo para hacer pasar la implementacion.

## Tests
21 pruebas: nueve funcionales, siete adversariales (tres mutantes conocidos
ejecutados en copias aisladas) y cinco de CLI mediante procesos reales.
El stub falla antes de implementar. Las pruebas CLI son evidencia de la
interfaz de consola; el tablero se verificara ademas en navegador real.

## Constraints
Stdlib; sin red, subprocess ni LLM en produccion. Los procesos pertenecen
solo al oraculo del PM. PARAR y reportar si falta la referencia revisada.
