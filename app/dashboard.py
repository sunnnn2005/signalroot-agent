def render_dashboard() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>SignalRoot Agent</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; background: #0f1115; color: #f5f7fb; }
    main { max-width: 1120px; margin: 0 auto; padding: 36px 20px; }
    header { display: flex; justify-content: space-between; gap: 20px; align-items: end; margin-bottom: 24px; }
    h1 { margin: 0; font-size: 42px; }
    p { color: #aab1c2; }
    button, select { border-radius: 8px; border: 1px solid #343a46; background: #191d26; color: white; padding: 10px 12px; }
    button { background: #ff4d6d; border-color: #ff4d6d; font-weight: 800; cursor: pointer; }
    .grid { display: grid; grid-template-columns: 0.85fr 1.15fr; gap: 16px; }
    .panel { border: 1px solid #2a303b; border-radius: 8px; background: #151922; padding: 18px; }
    .alert { padding: 12px; border-bottom: 1px solid #2a303b; cursor: pointer; }
    .alert:hover { background: #1e2430; }
    .muted { color: #aab1c2; font-size: 13px; }
    .pill { display: inline-block; background: #2a303b; padding: 4px 8px; border-radius: 999px; margin-top: 8px; }
    pre { white-space: pre-wrap; color: #dce3f3; line-height: 1.45; }
    @media (max-width: 820px) { header, .grid { display: block; } .panel { margin-top: 14px; } }
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>SignalRoot Agent</h1>
        <p>Agentic incident triage with metrics, logs, deploy history, and prior incident matching.</p>
      </div>
      <button id="triage">Run Triage</button>
    </header>
    <section class="grid">
      <div class="panel">
        <h2>Active Alerts</h2>
        <div id="alerts"></div>
      </div>
      <div class="panel">
        <h2>Triage Report</h2>
        <pre id="report">Select an alert, then run triage.</pre>
      </div>
    </section>
  </main>
  <script>
    let selected = null;
    async function loadAlerts() {
      const response = await fetch('/alerts');
      const alerts = await response.json();
      selected = alerts[0]?.id;
      document.querySelector('#alerts').innerHTML = alerts.map(alert => `
        <div class="alert" onclick="selected='${alert.id}'">
          <strong>${alert.title}</strong>
          <div class="muted">${alert.service}</div>
          <span class="pill">${alert.severity}</span>
        </div>
      `).join('');
    }
    async function triage() {
      const response = await fetch(`/alerts/${selected}/triage`, { method: 'POST' });
      const report = await response.json();
      document.querySelector('#report').textContent =
        `Root cause: ${report.likely_root_cause.cause}\\n` +
        `Confidence: ${Math.round(report.likely_root_cause.confidence * 100)}%\\n\\n` +
        `Impact: ${report.impact}\\n\\n` +
        `Evidence:\\n${report.evidence.slice(0, 6).map(item => '- ' + item.summary).join('\\n')}\\n\\n` +
        `Next steps:\\n${report.recommended_next_steps.map(step => '- ' + step).join('\\n')}`;
    }
    document.querySelector('#triage').addEventListener('click', triage);
    loadAlerts();
  </script>
</body>
</html>"""
