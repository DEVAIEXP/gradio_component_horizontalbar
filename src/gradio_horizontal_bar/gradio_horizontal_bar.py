from __future__ import annotations
import gradio as gr
from typing import Literal

class HorizontalBar(gr.HTML):
    
    def __init__(
        self,
        position: Literal["top", "bottom"] = "bottom",
        open: bool = True,
        height: int | str = 320,
        width: int | str = "100%",
        bring_to_front: bool = False,
        rounded_borders: bool = True,
        **kwargs,
    ):
        h_val = f"{height}px" if isinstance(height, int) else height
        w_val = f"{width}px" if isinstance(width, int) else width

        super().__init__(
            pos=position,
            is_open=open,
            bar_height=h_val,
            bar_width=w_val,
            on_top=bring_to_front,
            rounded=rounded_borders,
            html_template=self._get_html_template(),
            css_template=self._get_css_template(),
            js_on_load=self._get_js_on_load(),
            **kwargs
        )

    def _get_html_template(self):
        return """
        <button class="toggle-btn" aria-label="Toggle Bar">
            <div class="chevron"></div>
        </button>
        @children
        """

    def _get_css_template(self):
        return """     
            position: fixed !important;
            left: 50% !important;
            width: ${bar_width} !important;
            height: ${bar_height} !important;
            background-color: var(--background-fill-secondary) !important;
            z-index: ${on_top ? 2000 : 1000} !important;
            overflow: visible !important;
        
            ${pos === 'top' ? 'top: 0; border-bottom: 1px solid var(--border-color-primary); box-shadow: 0 8px 20px rgba(0,0,0,0.15);' : 'bottom: 0; border-top: 1px solid var(--border-color-primary); box-shadow: 0 -8px 20px rgba(0,0,0,0.15);'}
            ${rounded ? (pos === 'top' ? 'border-radius: 0 0 20px 20px !important;' : 'border-radius: 20px 20px 0 0 !important;') : ''}

            animation: ${pos === 'top' ? 'slideTop' : 'slideBottom'} 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards !important;
            @keyframes slideTop { from { transform: translateX(-50%) translateY(-100%); } to { transform: translateX(-50%) translateY(${is_open ? '0' : '-100%'}); } }
            @keyframes slideBottom { from { transform: translateX(-50%) translateY(100%); } to { transform: translateX(-50%) translateY(${is_open ? '0' : '100%'}); } }

            transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
            ${is_open ? 'transform: translateX(-50%) translateY(0) !important;' : (pos === 'top' ? 'transform: translateX(-50%) translateY(-100%) !important;' : 'transform: translateX(-50%) translateY(100%) !important;')}

            .vs-content-scroll {
                width: 100%;
                height: 100%;
                overflow-y: auto !important;
                overflow-x: hidden !important;
                padding: 10px !important;
                box-sizing: border-box !important;
                display: flex;
                flex-direction: column;
                gap: 10px;

                scrollbar-width: thin;
                scrollbar-color: var(--border-color-primary) transparent;
            }

            .vs-content-scroll::-webkit-scrollbar {
                width: 6px;
            }

            .vs-content-scroll::-webkit-scrollbar-thumb {
                background: var(--border-color-primary);
                border-radius: 10px;
            }

            .vs-content-scroll::-webkit-scrollbar-thumb:hover {
                background: var(--color-accent);
            }

            .toggle-btn {
                position: absolute;
                left: 50%;
                transform: translateX(-50%);
                background: var(--background-fill-secondary);
                border: 1.5px solid var(--border-color-primary);
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 65px;
                height: 32px;
                z-index: 2001;
                padding: 0;
                ${pos === 'top' ? 'bottom: -32px; border-top: none; border-radius: 0 0 14px 14px;' : 'top: -32px; border-bottom: none; border-radius: 14px 14px 0 0;'}
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }

            .chevron {
                width: 10px;
                height: 10px;
                border-bottom: 3px solid var(--body-text-color);
                border-right: 3px solid var(--body-text-color);
                transition: transform 0.4s ease;
                margin-top: ${pos === 'top' ? '-4px' : '4px'};
                ${pos === 'top' ? 'transform: rotate(45deg);' : 'transform: rotate(-135deg);'}
        }
        ${is_open ? (pos === 'top' ? '.chevron { transform: rotate(-135deg); margin-top: 5px; }' : '.chevron { transform: rotate(45deg); margin-top: -5px; }') : ''}
        """

    def _get_js_on_load(self):
    
        return f"""
        const root = element;
        const btn = root.querySelector('.toggle-btn');

        function wrapChildren() {{
            if (root.querySelector('.vs-content-scroll')) return;
            
            const wrapper = document.createElement('div');
            wrapper.className = 'vs-content-scroll';

            Array.from(root.childNodes).forEach(node => {{
                if (node !== btn && node.nodeType === 1) {{
                    wrapper.appendChild(node);
                }}
            }});
            root.appendChild(wrapper);
        }}

        wrapChildren();

        btn.addEventListener('click', (e) => {{
            e.stopPropagation();
            props.is_open = !props.is_open;
            trigger(props.is_open ? 'expand' : 'collapse');
        }});

        """

    def api_info(self): return {"type": "string"}