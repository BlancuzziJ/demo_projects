# JavaScript Calculator

A fully functional calculator built with **vanilla HTML, CSS, and JavaScript** – no libraries or build tools required.

## What it demonstrates

- DOM manipulation with `querySelector` and event listeners
- Keyboard support (number keys, operators, Enter, Backspace, Escape)
- CSS Grid layout for the button grid
- Clean separation of display state and calculation logic
- Edge-case handling: division by zero, chained operations, decimal input

## How to run

Open `index.html` in any modern browser.

```bash
# macOS
open index.html

# Linux
xdg-open index.html

# Windows (PowerShell)
Start-Process index.html
```

## Features

| Feature | Details |
|---------|---------|
| Basic arithmetic | `+`, `-`, `×`, `÷` |
| Decimal support | Single decimal point enforced |
| Keyboard input | Digits, operators, Enter (=), Backspace, Escape (C) |
| Error handling | Displays `Error` on division by zero |
| Responsive | Scales from mobile to desktop |
