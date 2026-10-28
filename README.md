# Programación para el análisis espacial: Python

Material docente del curso introductorio de programación en Python del **Máster Universitario en Ciencia y Tecnología de la Información Geográfica (CTIG)**.

El repositorio contiene los contenidos teóricos del curso, ejercicios, notebooks de Jupyter y ejemplos de código en Python. La documentación principal está desarrollada como un libro con [Quarto](https://quarto.org/).

## Estructura del repositorio

```text
intro_python/
|-- _quarto.yml           # Configuración del proyecto Quarto
|-- index.qmd             # Página de inicio del libro
|-- references.bib        # Referencias bibliográficas
|-- eisvogel.latex        # Plantilla LaTeX para la versión PDF
|
|-- chapters/             # Capítulos teóricos del curso
|-- notebooks/            # Notebooks de Jupyter
|-- python/               # Ejemplos y scripts de Python
\-- images/               # Imágenes y recursos gráficos
```

## Requisitos

Para generar el libro es necesario tener instalado [Quarto](https://quarto.org/docs/get-started/).

Para comprobar la instalación:

```bash
quarto --version
```

La generación de la versión PDF requiere además una distribución de LaTeX compatible con Quarto.

## Renderizar el libro

Desde el directorio raíz del repositorio:

```bash
quarto render
```

Este comando genera todos los formatos definidos en `_quarto.yml`.

Para generar únicamente la versión HTML:

```bash
quarto render --to html
```

Para generar únicamente la versión PDF:

```bash
quarto render --to pdf
```

Los archivos generados se almacenan en:

```text
_book/
```

## Previsualización

Durante la edición del contenido se puede iniciar una previsualización local con:

```bash
quarto preview
```

Quarto actualizará automáticamente el libro al detectar cambios en los archivos `.qmd`.

## Contenido del curso

El material está organizado en tres tipos principales de recursos:

- **Capítulos:** contenidos teóricos desarrollados en formato Quarto.
- **Notebooks:** ejemplos interactivos para introducir conceptos de programación en Python.
- **Scripts y ejercicios:** ejemplos independientes y actividades prácticas para aplicar los conceptos tratados en el curso.