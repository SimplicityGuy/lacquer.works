# lacquer.works

Single-page holding site for **Lacquer Works Studio** — an independent engineering
studio building at the intersection of **music, data, and AI**.

> _4AD records meets Teenage Engineering._ Dark, precise, restrained, a little
> mysterious. It should feel like a tool, not a portfolio. When in doubt, remove
> rather than add.

Live at **[lacquer.works](https://lacquer.works)**.

---

## Contents

- [Overview](#overview)
- [Quick start](#quick-start)
- [Design language](#design-language)
  - [Palette](#palette)
  - [Typography](#typography)
  - [Spacing, borders & surfaces](#spacing-borders--surfaces)
  - [Motion](#motion)
- [The mark](#the-mark)
- [The vinyl-grooves background](#the-vinyl-grooves-background)
- [Page structure](#page-structure)
- [Projects](#projects)
- [Accessibility & performance](#accessibility--performance)
- [Development](#development)
- [Deployment](#deployment)
- [Repository layout](#repository-layout)
- [Editing guidelines](#editing-guidelines)
- [License](#license)

---

## Overview

`index.html` is the entire site: one static file, no build step. Plain HTML, one
`<style>` block, one `<script>` block of vanilla JS. It works over `file://` and
deploys as flat static HTML with nothing to compile.

Two things are drawn at runtime with the Canvas API rather than shipped as image
assets:

1. **The logo mark** — a stylised record/turntable glyph, rendered by a single
   `drawMark(canvasId, opts)` function and reused at four sizes (nav, hero static
   layer, hero rotating layer, favicon).
2. **The hero background** — a field of animated vinyl grooves.

There are no third-party JS libraries and no framework. The only external
dependency is Google Fonts.

---

## Quick start

```bash
# clone
git clone git@github.com:SimplicityGuy/lacquer.works.git
cd lacquer.works

# open it — no build, no server required
open index.html                 # macOS

# …or serve it, if you want the fonts to load exactly as in production
python3 -m http.server 8000     # then visit http://localhost:8000
```

That's the whole toolchain. There is no `package.json`, no bundler, no CSS
pipeline — by design.

---

## Design language

The look is defined entirely by a small set of tokens declared as CSS custom
properties at the top of `index.html`. Everything on the page is composed from
these; nothing is off-palette.

### Palette

Ink-dark violet base, three accent violets, two structural mids. No gradients,
ever — colour comes from the palette and from canvas alpha, not from blends.

| Token           | Value      | Role                                              |
| --------------- | ---------- | ------------------------------------------------- |
| `--bg`          | `#04030a`  | Page background, card fill, mark interior         |
| `--bg2`         | `#09071a`  | About strip surface                               |
| `--bg3`         | `#0d0b20`  | Reserved deep surface                             |
| `--violet`      | `#9d5cff`  | Primary accent — outer ring, arrows, button border|
| `--purple`      | `#c084fc`  | Secondary accent — project names, glyph arc       |
| `--magenta`     | `#f472b6`  | Signal accent — waveform bar, tonearm dot         |
| `--mid`         | `#2d1b6e`  | Groove ring, tag borders, hover borders           |
| `--faint`       | `#1c1040`  | Hairline dividers and section borders             |
| `--near-white`  | `#f0eaff`  | Primary text                                      |
| `--dimmed`      | `#c4b0e8`  | Body copy                                          |
| `--url-color`   | `#c084fc`  | URLs and section labels                           |

Two literal off-palette values exist by intent: `#4a3880` (footer / project
kicker — a muted violet-grey) and the canvas RGBA tints, which are the palette
hexes expressed with per-frame alpha.

### Typography

Two families, and only two.

- **JetBrains Mono** (300 / 400 / 500) — the entire interface: nav, labels, body
  copy, buttons, footer, and the mark's arc text. Uppercased labels ride wide
  tracking (`letter-spacing` `0.12em`–`0.22em`).
- **Anybody** (200, _italic_) — the display face, used only for the wordmark and
  project names. Thin, italic, slightly compressed — the one expressive gesture
  against an otherwise monospace grid.

| Element          | Family        | Size   | Weight / style      |
| ---------------- | ------------- | ------ | ------------------- |
| Wordmark         | Anybody       | 64px   | 200 italic          |
| Project name     | Anybody       | 22px   | 200 italic          |
| Hero copy        | JetBrains Mono| 13px   | 300                 |
| About body       | JetBrains Mono| 12px   | 300                 |
| Project desc     | JetBrains Mono| 11px   | 300                 |
| Section labels   | JetBrains Mono| 9px    | 400, uppercase      |
| Button           | JetBrains Mono| 10px   | 400, uppercase      |
| Tags / kicker    | JetBrains Mono| 8px    | 400, uppercase      |

Labels lead with `//` (`// projects`, `// building at the intersection…`) — a
code-comment cadence that sets the tool-not-brochure tone. The year is Roman:
**MMXXV**.

### Spacing, borders & surfaces

- **8px spacing grid** — paddings and gaps are multiples of 8 (`16 / 24 / 40 / 64
  / 96`).
- **All borders are hairlines** — `0.5px` (the button is the sole exception at
  `0.8px`). This is deliberate and load-bearing; keep it.
- **No `border-radius` anywhere** — the global reset sets `border-radius: 0` and
  every corner is square.
- **No box-shadows. No gradients.** Depth comes from surface tone (`--bg` →
  `--bg2`) and hairline dividers, nothing else.

### Motion

Restrained and slow. Three animations, all honouring reduced-motion:

- **Hero fade-in** — `800ms ease-out`, opacity + 16px upward drift, once on load.
- **Mark rotation** — the mark's asymmetric elements orbit at **60s / turn**,
  linear, infinite (see [The mark](#the-mark)).
- **Grooves background** — a continuous `requestAnimationFrame` loop (see
  [The vinyl-grooves background](#the-vinyl-grooves-background)).

Hover transitions are `0.2s` on `background`, `color`, and `border-color` only.

---

## The mark

The logo is drawn, not embedded. `drawMark(canvasId, opts)` paints, onto a 2D
canvas of any size, a record-like glyph composed of:

- an **outer ring** (`--violet`) and an inner **groove ring** (`--mid`);
- a dark **interior fill**;
- two **asymmetric glyph arcs** (`--purple` outer ≈310°, `--mid` inner ≈280°)
  with **terminal dots** (`--magenta`, `--violet`);
- three offset **waveform bars** (`--purple` / `--magenta` / `--purple`);
- **arc text** — `LACQUER` curving over the top, `WORKS` under the bottom, laid
  out letter-by-letter from live font metrics.

Every element's colour is an `opts` field, which is how one function serves four
roles. Setting an element's colour to transparent simply omits it:

| Instance             | Size    | How it's drawn                                             |
| -------------------- | ------- | ---------------------------------------------------------- |
| Nav mark             | 48×48   | `showText:false`                                           |
| Hero — static layer  | 320×340 | Full mark **minus** glyph arcs & dots (those set transparent) |
| Hero — rotating layer| 320×340 | **Only** glyph arcs & dots, on a transparent background    |
| Favicon              | 64×64   | Full mark → `toDataURL()` → injected `<link rel="icon">`   |

**Why two hero layers?** The outer ring is a perfect circle, so rotating it is
visually invisible. Instead, the mark is split across two stacked canvases: the
symmetric parts and the arc text sit still on the bottom layer, while only the
_asymmetric_ arcs and dots live on the top layer, whose wrapper is rotated in CSS
(`#hero-mark-rotor`, `spin 60s linear infinite`). The result is a clearly visible
turntable rotation while the `LACQUER / WORKS` text stays upright — with no
duplicated drawing logic.

Everything mark- and text-dependent runs inside `document.fonts.ready.then(...)`,
because the arc text depends on `ctx.measureText` and would mis-lay-out before the
fonts load.

The favicon is generated the same way, from an offscreen 64×64 canvas — there are
no image files to keep in sync.

---

## The vinyl-grooves background

A single `<canvas>` fills the hero (`inset:0`, `z-index:0`; hero content sits at
`z-index:1`). It renders concentric record grooves centred behind the mark (left
third of the hero), so the field reads as a turntable halo around the logo.
About / Projects / Footer stay flat — no canvas.

Concentric rings can't show rotation, so perceptible motion comes from three
sources, all palette-only:

1. **An outward-travelling brightness wave** — per-ring alpha modulated by
   `sin(r·0.045 − t·waveSpeed)`, crest-only, over a low base alpha.
2. **An orbiting magenta "tonearm" dot** with a faint line to centre — echoes the
   mark's terminal dots and makes the rotation unmistakable.
3. **A slowly breathing spindle ring** near the centre.

The tuning is the approved **"Present"** intensity (`1.7`), chosen after a live
comparison of four candidates (grooves / dust / lattice / waveform):

| Parameter        | Value               |
| ---------------- | ------------------- |
| Intensity (`I`)  | `1.7`               |
| Ring gap         | `15px`              |
| Wave speed       | `0.0011 · I`        |
| Base alpha       | `0.045`             |
| Crest swing      | `0.16 · I`          |
| Orbit radius     | `min(W,H) · 0.20`   |
| Orbit angular vel| `−t · 0.00026 · I`  |

The canvas is sized to its element rect × `devicePixelRatio` (capped at 2),
re-initialised on resize, and fully redrawn each frame.

---

## Page structure

Five sections, top to bottom:

1. **Nav** — fixed, `rgba(4,3,10,0.92)` + `backdrop-filter: blur(12px)`, `0.5px`
   bottom hairline. Left: 48×48 mark + `LACQUER WORKS`. Right: `lacquer.works`.
   No nav links.
2. **Hero** — `min-height:100vh`. Two columns on desktop (mark left ≈320×340,
   wordmark lockup right); stacked and centred on mobile. Wordmark = _Lacquer /
   Works_ **STUDIO** / `lacquer.works`, then `// building at the intersection of
   music, data, and AI`, then one outline button → `mailto:hello@lacquer.works`.
3. **About strip** — full-width `--bg2`, three hairline-divided columns: _Founder
   & Principal Engineer_, _Music + Data + AI_, _Est. MMXXV_.
4. **Projects** — `// projects` label + three cards (see below).
5. **Footer** — full-width `--bg`, top hairline. _Lacquer Works Studio · MMXXV_ /
   `lacquer.works`.

Responsive breakpoint is **768px**: below it, hero / about / projects each
collapse to a single column, the mark shrinks to 220px, and the nav drops its URL
label.

---

## Projects

The three project cards link to their GitHub repositories:

| Card             | Blurb                                                          | Tags                    | Repo                                                                            |
| ---------------- | -------------------------------------------------------------- | ----------------------- | ------------------------------------------------------------------------------ |
| `discogsography` | Vinyl collection graph. Neo4j + PostgreSQL + Discogs API.      | python · docker · graph | [SimplicityGuy/discogsography](https://github.com/SimplicityGuy/discogsography) |
| `phaze`          | Align your music.                                              | python · music · audio  | [SimplicityGuy/phaze](https://github.com/SimplicityGuy/phaze)                   |
| `GRUVAX`         | AI music file organiser. Anthropic Batch API + prompt caching. | python · AI · music     | [SimplicityGuy/GRUVAX](https://github.com/SimplicityGuy/GRUVAX)                 |

To change the roster, edit the three `.project-card` anchors in `index.html`:
name (`.project-name`), one-line blurb (`.project-desc`), tags
(`.project-tags span`), and the `href`. Keep to **three tags** and one sentence of
description per card — the grid and the tone both depend on that restraint.

---

## Accessibility & performance

- **`prefers-reduced-motion: reduce`** is honoured: the background rAF loop never
  starts (a single static grooves frame is drawn instead) and the mark rotation is
  disabled. The static frame is composed to still look intentional.
- **Battery / CPU** — the background loop pauses on `visibilitychange` when the
  tab is hidden and resumes when visible.
- **Semantics** — the wordmark is a real `<h1>`; every decorative canvas is
  `aria-hidden="true"`.
- **DPR** is capped at 2 to avoid over-rendering the background on high-density
  displays.

---

## Development

There is nothing to install and nothing to run. Edit `index.html`, reload the
browser.

**Verifying a change:**

- Open the console — it should be clean (the runtime-generated favicon means
  there's no missing-`favicon.ico` request).
- Confirm the mark's arc text lays out correctly (proves the `document.fonts.ready`
  path).
- Confirm the background is perceptibly animating and the glyph arcs + dots orbit
  while the arc text and rings stay upright.
- Toggle reduced-motion (DevTools → Rendering → *Emulate CSS
  prefers-reduced-motion*) and confirm all motion stops on a clean static frame.
- Check the collapse at ≤768px (spot-check ~375px and ~1440px).

Reference screenshots from build/verification live at the repo root
(`desktop-*.png`, `mobile-*.png`, `hero-*.png`, `*-verification.png`).

---

## Deployment

Static hosting — copy `index.html` to any static host or CDN; there is no build
artifact. The site is served at [lacquer.works](https://lacquer.works). Ensure the
Google Fonts request is reachable in your hosting environment (the mark's arc text
waits on `document.fonts.ready`).

---

## Repository layout

```
.
├── index.html                     # the entire site — HTML + CSS + JS in one file
├── README.md                      # this document
├── LICENSE
├── design/                        # design exploration & source assets
│   ├── lacquer-works-assets.html  # design system + drawMark reference
│   ├── bg-prototypes.html         # the four background candidates
│   ├── lw-1-grooves.png … lw-4-waveform.png   # background candidate renders
│   └── lw-fix-*.png               # tuning iterations
├── docs/
│   └── superpowers/
│       ├── specs/   2026-06-30-lacquer-works-landing-design.md   # the design contract
│       └── plans/   2026-06-30-lacquer-works-landing.md          # the build plan
├── lacquer-works-claude-code-prompt.md   # original source prompt
└── *.png                          # build / verification screenshots
```

The canonical description of the design system and every locked decision is the
spec: [`docs/superpowers/specs/2026-06-30-lacquer-works-landing-design.md`](docs/superpowers/specs/2026-06-30-lacquer-works-landing-design.md).
Read it before making structural changes.

---

## Editing guidelines

The aesthetic is a set of constraints, not suggestions. Before adding anything,
check it against these:

- **Two fonts only** — JetBrains Mono for everything, Anybody 200 italic for the
  wordmark and project names.
- **Stay on-palette** — use the tokens; no new colours, no gradients, no shadows.
- **Hairlines and square corners** — `0.5px` borders, `border-radius: 0`
  everywhere.
- **8px grid** — spacing in multiples of 8.
- **Motion stays slow and honours reduced-motion** — nothing fast, nothing
  gratuitous; every animation needs a reduced-motion off-ramp.
- **`drawMark` is shared** — resize or recolour via `opts`; don't fork the drawing
  logic. Mark/text work stays inside `document.fonts.ready`.
- **When in doubt, remove rather than add.**

---

## License

See [`LICENSE`](LICENSE).
