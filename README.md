# `gradio-horizontal-bar`
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.2%20-%20blue">  
<a href="https://huggingface.co/spaces/elismasilva/gradio_horizontal_bar"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Demo-blue"></a>  
<span>💻 <a href='https://github.com/DEVAIEXP/gradio_component_horizontalbar'>Component GitHub Code</a></span>

A versatile, collapsible layout component for Gradio 6 apps using `gr.HTML`. It allows you to create fixed panels at the **top** or **bottom** of the screen that can contain any other Gradio component.

Perfect for floating toolbars, real-time log consoles, settings panels, or secondary navigation bars that stay out of the way until needed.

## Features and Key Characteristics

- **Dual-Positioning:** Easily switch between `top` and `bottom` placement with a single property.
- **Native Container Support:** Works as a standard Gradio context manager (`with HorizontalBar():`), allowing you to nest any Gradio component inside.
- **Gradio 6 Theme Integration:** Uses native CSS variables (`--background-fill`, `--color-accent`) to match any theme perfectly in Light or Dark mode.


## Installation

```bash
pip install gradio-horizontal-bar
```

## Usage

### Mode 1: Top Floating Toolbar
```py
import gradio as gr
from gradio_horizontal_bar import HorizontalBar

with gr.Blocks() as demo:
    with HorizontalBar(position="top", height=85, open=False):
        with gr.Row():
            gr.Button("▶️ Start Process", variant="primary")
            gr.Button("⏹️ Stop All")
            
    gr.Image("https://picsum.photos/1200/600")
    
demo.launch()
```

### Mode 2: Bottom Log Console (Pre-opened)
```py
import gradio as gr
from gradio_horizontal_bar import HorizontalBar

with gr.Blocks() as demo:
    gr.Markdown("# Main Content Area")
    
    with HorizontalBar(position="bottom", height=250, open=True):
        gr.Markdown("### 📝 System Logs")
        gr.Textbox(lines=8, interactive=False, placeholder="Waiting for logs...")
        
demo.launch()
```

| Property | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `position` | `Literal["top", "bottom"]` | `"bottom"` | Where the bar is anchored (top or bottom of the screen). |
| `open` | `bool` | `True` | Whether the bar starts expanded (`True`) or collapsed (`False`). |
| `height` | `int \| str` | `320` | Height of the bar (pixels if int, or any CSS unit if str). |
| `width` | `int \| str` | `"100%"` | Width of the bar (horizontally centered). |
| `bring_to_front` | `bool` | `False` | If `True`, gives the bar a higher z-index to overlap other sidebars. |
| `rounded_borders` | `bool` | `True` | Whether to apply rounded corners to the floating edges. |
| `label` | `str \| None` | `None` | Optional label for the component context. |
| `visible` | `bool` | `True` | Whether the component is visible on the screen. |



### License
Apache 2.0

---