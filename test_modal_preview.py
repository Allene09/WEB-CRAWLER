from playwright.sync_api import sync_playwright

TEST_SCRIPT = """
(() => {
    let modal = document.getElementById('__spider_scan_modal__');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = '__spider_scan_modal__';
        modal.style.cssText = `
            position: fixed !important;
            bottom: 24px !important;
            left: 24px !important;
            width: 360px !important;
            background: rgba(15, 23, 42, 0.96) !important;
            backdrop-filter: blur(12px) !important;
            color: #f8fafc !important;
            padding: 16px 20px !important;
            border-radius: 14px !important;
            border: 2px solid #0284c7 !important;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.75), 0 0 20px rgba(56, 189, 248, 0.25) !important;
            z-index: 2147483646 !important;
            font-family: system-ui, -apple-system, sans-serif !important;
            line-height: 1.4 !important;
            pointer-events: none !important;
        `;
        document.body.appendChild(modal);
    }

    const data = {
        scanNum: 1,
        tag: '<button>',
        elementName: 'Student Registration',
        action: 'Triggered Click Event',
        status: 'PASSED ✓',
        statusColor: '#22c55e',
        details: [
            { label: 'Click Action', value: 'Responsive ✓', color: '#22c55e' },
            { label: 'JS Exceptions', value: '0 Clean ✓', color: '#22c55e' },
            { label: 'Network', value: '200 OK', color: '#38bdf8' },
            { label: 'DOM State', value: 'Modal Rendered', color: '#94a3b8' }
        ]
    };

    const detailsHtml = (data.details || []).map(d => `
        <div style="background:rgba(2, 6, 23, 0.6);padding:6px 10px;border-radius:8px;border:1px solid rgba(56, 189, 248, 0.15);">
            <div style="color:#94a3b8;font-size:10px;text-transform:uppercase;font-weight:700;">${d.label}</div>
            <div style="color:${d.color || '#f8fafc'};font-size:12px;font-weight:700;margin-top:1px;">${d.value}</div>
        </div>
    `).join('');

    modal.innerHTML = `
        <div style="display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(56,189,248,0.25);padding-bottom:10px;margin-bottom:12px;">
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="font-size:20px;">🕷️</span>
                <div>
                    <div style="font-size:13px;font-weight:800;color:#38bdf8;letter-spacing:0.5px;">SPIDEY LIVE SCANNER</div>
                    <div style="font-size:10px;color:#94a3b8;">Inspecting DOM & React State</div>
                </div>
            </div>
            <span style="background:#0284c7;color:#fff;font-size:11px;font-weight:800;padding:3px 9px;border-radius:12px;box-shadow:0 0 8px #38bdf8;">
                #${data.scanNum || 1}
            </span>
        </div>

        <div style="margin-bottom:10px;">
            <div style="color:#94a3b8;font-size:10px;text-transform:uppercase;font-weight:700;letter-spacing:0.5px;">Element Targeted:</div>
            <div style="background:rgba(2, 6, 23, 0.75);color:#38bdf8;font-family:monospace;font-size:13px;font-weight:700;padding:6px 10px;border-radius:8px;border:1px solid rgba(56, 189, 248, 0.25);margin-top:3px;word-break:break-all;">
                <span style="color:#f43f5e;">${data.tag || '<el>'}</span> ${data.elementName || ''}
            </div>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px;">
            ${detailsHtml}
        </div>

        <div style="background:rgba(34, 197, 94, 0.15);border:1.5px solid ${data.statusColor || '#22c55e'};color:${data.statusColor || '#86efac'};padding:7px 12px;border-radius:8px;font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:space-between;">
            <span>STATUS</span>
            <span>${data.status || 'PASSED ✓'}</span>
        </div>
    `;
})();
"""

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page()
    page.goto("https://ojtrack.bscs4b.com")
    page.evaluate(TEST_SCRIPT)
    page.screenshot(path="scan_modal_preview.png")
    b.close()
    print("Preview saved to scan_modal_preview.png")
