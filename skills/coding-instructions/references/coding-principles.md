# Andrej Karpathy coding principles

Mandatory when writing code. Applies to code only, not to casual chat.

## 1. Minimalism

- Keep code short, self-contained, zero-dependency (or near-zero).
- Write the simplest "atomic" implementation first, then optimize.
- Don't add complexity for hypothetical needs.

## 2. Don't be a hero — copy first, innovate later

- Find a proven solution to copy, then adapt as needed.
- Introduce only one complexity at a time.

## 3. Understand the fundamentals

- Don't blindly trust abstractions; when things fail, debug down to the mechanism.
- Code should reflect understanding, not black-box stacking.

## 4. Simple to complex

- Get it working first, then add capabilities and optimizations step by step.

## 5. Clean style

- Short files, single responsibility; flat directories, minimal nesting.
- Comments should teach — explain the "why", skip filler.

## 6. Minimal dependencies

- Prefer the standard library; plain implementations over heavy frameworks.
