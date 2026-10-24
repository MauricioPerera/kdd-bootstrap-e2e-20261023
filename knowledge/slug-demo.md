---
type: 'Concept'
title: 'Proyecto de prueba del bootstrap de main'
description: 'Definicion de una CLI minima para verificar un proyecto nuevo, su tarea Git y la calidad obligatoria en CI.'
tags: ['demo', 'bootstrap', 'quality']
---

# Producto de demostracion

Normalizar un titulo a un slug ASCII: descomponer Unicode mediante NFKD,
retirar caracteres no ASCII, convertir a minusculas y reemplazar cada grupo
que no sea a-z o 0-9 por un guion. Retirar guiones de ambos extremos.
El resultado debe tener de 1 a 64 caracteres; de otro modo, ValueError.
Una entrada que no sea str causa TypeError. No truncar silenciosamente.

La CLI acepta exactamente un titulo posicional, imprime el slug y un salto
de linea en stdout, y termina en 0. Para entrada o argumentos invalidos:
exit 2, stdout vacio, diagnostico en stderr sin traceback.

Contrato y oraculo: [slug](contracts/slug.md).
El [diario Git](git-tasks.md) registra una tarea propia desde backlog hasta
done, con una rama y evidencia de la revision probada.
El [CI generado](bootstrap-product-quality-ci.md) exige la politica propia;
la [aprobacion](quality-approval.md) corresponde al revisor humano.

La prueba usa el main de KDD 7886578b8e4ce9f107851a4d7873ac9ab880dec8.
El bootstrap adapta el workflow antes de cualquier cambio de producto.
Las mutaciones conocidas comprueban fuerza basica del oraculo; no prueban
ausencia de defectos ni generalizacion a mutaciones independientes.
