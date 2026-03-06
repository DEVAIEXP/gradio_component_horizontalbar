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
       
        html_template = """
        <button class="toggle-btn" type="button" aria-label="Toggle Bar">
            <div class="chevron"></div>
        </button>
        @children
        """
        
        css_template = """        
        position: fixed !important;
        left: 50% !important;
        width: ${bar_width} !important;
        height: ${bar_height} !important;
        z-index: ${on_top ? 2000 : 1000} !important;
        overflow: visible !important;
        background-color: var(--background-fill-secondary) !important;
        display: flex !important;
        flex-direction: column !important;
        box-sizing: border-box !important;
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        transform: translateX(-50%) ${is_open ? "translateY(0)" : (pos === 'top' ? "translateY(-100%)" : "translateY(100%)")} !important;
        
        ${pos === 'top' ? 'top: 0; border-bottom: 1px solid var(--border-color-primary);' : 'bottom: 0; border-top: 1px solid var(--border-color-primary);'}
        ${rounded ? (pos === 'top' ? 'border-radius: 0 0 20px 20px !important;' : 'border-radius: 20px 20px 0 0 !important;') : ''}

        &.is-open {
            transform: translateX(-50%) translateY(0) !important;
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }

        &.is-closed {
            transform: translateX(-50%) ${pos === 'top' ? "translateY(-100%)" : "translateY(100%)"} !important;
            box-shadow: none;
        }

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
            scrollbar-width: thin !important;
            scrollbar-color: var(--border-color-primary) transparent !important;
        }

        .vs-content-scroll::-webkit-scrollbar { width: 6px; }
        .vs-content-scroll::-webkit-scrollbar-thumb { background: var(--border-color-primary); border-radius: 10px; }
        .vs-content-scroll::-webkit-scrollbar-thumb:hover { background: var(--color-accent); }

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
            ${pos === 'top' ? 'bottom: -32px; border-top: none; border-radius: 0 0 14px 14px;' : 'top: -32px; border-bottom: none; border-radius: 14px 14px 0 0;'}
            box-shadow: ${pos === 'top' ? '0 4px 6px rgba(0,0,0,0.1)' : '0 -4px 6px rgba(0,0,0,0.1)'};
        }

        .chevron {
            width: 10px;
            height: 10px;
            border-bottom: 3px solid var(--body-text-color);
            border-right: 3px solid var(--body-text-color);
            transition: transform 0.4s ease;
            margin-top: ${pos === 'top' ? '-4px' : '4px'};
            transform: ${pos === 'top' ? 'rotate(45deg)' : 'rotate(-135deg)'};
        }
        
        &.is-open .chevron {
            transform: ${pos === 'top' ? 'rotate(-135deg)' : 'rotate(45deg)'};
            margin-top: ${pos === 'top' ? '4px' : '-4px'};
        }
        """

        js_on_load = """
        const root = element;
        const btn = root.querySelector('.toggle-btn');
        if (!btn) return;

        const childrenTextNode = Array.from(root.childNodes).find(n => n.nodeType === 3 && n.textContent.trim() === '@children');
        
        if (childrenTextNode) {
            const mock = document.createElement('div');
            mock.className = 'vs-content-scroll';
            mock.innerHTML = `<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;opacity:0.4;gap:10px;"><div style="font-size:24px">↕️</div><div>Horizontal Bar Preview</div></div>`;
            root.replaceChild(mock, childrenTextNode);
        } else {
            if (!root.querySelector('.vs-content-scroll')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'vs-content-scroll';
                Array.from(root.childNodes).forEach(node => {
                    if (node !== btn && node.nodeType === 1) {
                        wrapper.appendChild(node);
                    }
                });
                root.appendChild(wrapper);
            }
        }

        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const currentlyOpen = root.classList.contains('is-open') || (!root.classList.contains('is-closed') && props.is_open);
            const newState = !currentlyOpen;

            if (newState) {
                root.classList.remove('is-closed');
                root.classList.add('is-open');
            } else {
                root.classList.remove('is-open');
                root.classList.add('is-closed');
            }

            if (typeof props !== 'undefined') props.is_open = newState;
            trigger(newState ? 'expand' : 'collapse');
        });
        """
        
        super().__init__(
            pos=position,
            is_open=open,
            bar_height=h_val,
            bar_width=w_val,
            on_top=bring_to_front,
            rounded=rounded_borders,
            html_template=html_template,
            css_template=css_template,
            js_on_load=js_on_load,
            **kwargs
        )
    
    def api_info(self): return {"type": "string"}