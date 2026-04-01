# Forge Vision

Forge is a convention-first full-stack TypeScript framework for building readable business applications quickly.

Forge should feel:

- simple
- explicit
- calm
- explainable
- readable
- product-minded

Forge is not trying to win by being the most abstract, flexible, magical, or extensible framework.

Forge should prefer:

- convention over configuration
- generated code that humans can read
- predictable structure
- honest limitations
- explainability through CLI and manifest data
- boring, stable implementations over cleverness

Forge should avoid:

- premature abstraction
- plugin systems before they are needed
- speculative architecture
- hidden framework behavior that makes generated code hard to understand
- pretending rough edges are solved when they are not

Phase 1 is not about building a complete framework.

Phase 1 is about proving a coherent story:

1. create app
2. generate model
3. generate scaffold
4. migrate
5. run dev server
6. explain how the app is wired

A good Forge implementation should make a developer feel:
“I can see what this framework is doing, and I could work with it confidently.”

If a decision improves flexibility but harms readability, predictability, or honesty, Forge should usually choose readability, predictability, and honesty.