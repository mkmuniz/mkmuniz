<div align="center">

<img src="assets/mkmuniz-3d.gif" width="240" alt="Voxel avatar of Mikael, spinning">

# Mikael Muniz Ribeiro

<a href="https://readme-typing-svg.demolab.com/">
  <img src="https://readme-typing-svg.demolab.com/?font=JetBrains+Mono&weight=600&size=19&pause=1200&color=61DAFB&center=true&vCenter=true&width=560&lines=Software+Engineer+%C2%B7+S%C3%A3o+Paulo%2C+BR;TypeScript+%E2%80%A2+Go+%E2%80%A2+Java;This+avatar+is+rendered+by+a+script+in+this+repo" alt="TypeScript, Go, Java — Software Engineer in São Paulo">
</a>

<br>

[![Website](https://img.shields.io/badge/mkmuniz.dev-0B1020?style=for-the-badge&logo=hugo&logoColor=61DAFB)](https://mkmuniz.dev)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=LinkedIn&logoColor=white)](https://www.linkedin.com/in/mikael-muniz-ribeiro/)
[![Gmail](https://img.shields.io/badge/Gmail-EA4335?style=for-the-badge&logo=Gmail&logoColor=white)](mailto:mikaelmuniz2001@gmail.com)
[![Linktree](https://img.shields.io/badge/Linktree-43E55E?style=for-the-badge&logo=Linktree&logoColor=white)](https://linktr.ee/mkmuniz)

</div>

---

## 🎒 Inventory

<div align="center">

<img src="https://skillicons.dev/icons?i=ts,js,react,nextjs,nodejs,nestjs&theme=dark" alt="TypeScript, JavaScript, React, Next.js, Node.js, NestJS">
<br>
<img src="https://skillicons.dev/icons?i=go,java,python,rust,vue,cpp&theme=dark" alt="Go, Java, Python, Rust, Vue, C++">
<br>
<img src="https://skillicons.dev/icons?i=docker,postgres,mongodb,redis,git,linux&theme=dark" alt="Docker, Postgres, MongoDB, Redis, Git, Linux">

</div>

| Slot | Item | Durability |
|:--|:--|:--|
| `1` | **TypeScript** — main tool, never leaves the hotbar | ████████████ |
| `2` | **React / Next.js** — where most of the UI work lands | ██████████░░ |
| `3` | **Node / NestJS** — APIs and services | █████████░░░ |
| `4` | **Go** — when it has to be small and fast | ███████░░░░░ |
| `5` | **Java** — enterprise expeditions | ██████░░░░░░ |
| `6` | **Docker** — everything ships in a box | ████████░░░░ |

---

## 📊 Stats

<div align="center">

<img height="165" src="https://github-readme-stats.vercel.app/api?username=mkmuniz&show_icons=true&hide_border=true&bg_color=00000000&title_color=61DAFB&icon_color=3178C6&text_color=8B95A5" alt="GitHub stats for mkmuniz">
<img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=mkmuniz&layout=compact&hide_border=true&bg_color=00000000&title_color=61DAFB&text_color=8B95A5" alt="Most used languages">

<br>

<img src="https://github-readme-streak-stats.herokuapp.com/?user=mkmuniz&hide_border=true&background=00000000&stroke=8B95A5&ring=61DAFB&fire=61DAFB&currStreakLabel=61DAFB&sideLabels=8B95A5&dates=8B95A5&currStreakNum=8B95A5&sideNums=8B95A5" alt="Contribution streak">

</div>

---

## ⏱️ Time played

<!-- preenchido sozinho todo dia pelo workflow .github/workflows/waka-readme.yml -->
<!--START_SECTION:waka-->
<!--END_SECTION:waka-->

---

## 🌍 Biomes explored

| Project | Stack | What it is |
|:--|:--|:--|
| [**BrightFlow**](https://github.com/mkmuniz/BrightFlow) ⭐7 | TypeScript | Dashboard for managing energy-bill data |
| [**FastPix**](https://github.com/mkmuniz/FastPix) ⭐7 | Java | Generating and managing Pix payments |
| [**Mikael-Portfolio**](https://github.com/mkmuniz/Mikael-Portfolio) | Vue | Projects and career, in one place |
| [**FinTrack**](https://github.com/mkmuniz/FinTrack) | Go | Personal finance tracking |
| [**mira-discord-bot**](https://github.com/mkmuniz/mira-discord-bot) | TypeScript | Discord bot |
| [**elagix-tk**](https://github.com/mkmuniz/elagix-tk) | Rust | Toolkit experiments |

---

## 🔨 Crafting recipe

That avatar up there is not a screenshot, and it is not a skin-render API. It is
built twice from scratch, by two scripts living in this repo:

```
tools/skin.py     →  assets/mkmuniz-skin.png   64×64, a real Minecraft skin
tools/render.py   →  assets/mkmuniz-3d.gif     36 frames, 360° turnaround
```

**`skin.py`** draws every face of the character as text. No image editor — the
hoodie, the headphones and the diamond on the chest are literally typed out:

```python
"front": ["HHHHHHHH", "HHHHHHHH", "HSSSSSSH", "SSSSSSSS",
          "SEPSSPES", "SSSSSSSS", "SSSMMSSS", "SSSSSSSS"],
```

**`render.py`** is a tiny 3D renderer — no engine, no WebGL, ~250 lines of
NumPy. It shoots an orthographic ray per pixel at the eight oriented boxes that
make up the body, samples the skin with Minecraft's own UV layout, quantises the
lighting into six steps, and writes a transparent GIF that reads correctly on
both the light and the dark GitHub theme.

Rebuild it yourself:

```bash
pip install -r tools/requirements.txt
python tools/render.py   # regenerates all three files above
```

Change a letter in `skin.py`, re-run, and the character changes. 🙂

<div align="center">
<br>
<img src="assets/mkmuniz-skin.png" width="160" alt="The raw 64x64 skin texture" style="image-rendering: pixelated">
<br>
<sub><i>the raw 64×64 texture — every pixel typed by hand</i></sub>
</div>
