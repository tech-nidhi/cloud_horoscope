/**
 * Report Exporter for Cloud Horoscope
 * Generates downloadable Cosmic Architecture PNG Cards and Markdown Reports
 */

/**
 * Wraps text into multiple lines for Canvas drawing
 */
function wrapText(ctx, text, maxWidth) {
  const words = text.split(' ');
  const lines = [];
  let currentLine = words[0];

  for (let i = 1; i < words.length; i++) {
    const word = words[i];
    const width = ctx.measureText(currentLine + " " + word).width;
    if (width < maxWidth) {
      currentLine += " " + word;
    } else {
      lines.push(currentLine);
      currentLine = word;
    }
  }
  lines.push(currentLine);
  return lines;
}

/**
 * Downloads a high-resolution PNG cosmic horoscope report card
 */
export function downloadHoroscopeImage({ name, dobFormatted, horoscopeData }) {
  const canvas = document.createElement('canvas');
  canvas.width = 1200;
  canvas.height = 900;
  const ctx = canvas.getContext('2d');

  // Background Gradient
  const bgGrad = ctx.createRadialGradient(600, 300, 50, 600, 450, 700);
  bgGrad.addColorStop(0, '#2e1065');
  bgGrad.addColorStop(0.4, '#1e1b4b');
  bgGrad.addColorStop(0.8, '#0f172a');
  bgGrad.addColorStop(1, '#020617');
  ctx.fillStyle = bgGrad;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Outer Border & Glow
  ctx.strokeStyle = 'rgba(168, 85, 247, 0.4)';
  ctx.lineWidth = 3;
  ctx.strokeRect(30, 30, canvas.width - 60, canvas.height - 60);

  ctx.strokeStyle = 'rgba(236, 72, 153, 0.2)';
  ctx.lineWidth = 1;
  ctx.strokeRect(40, 40, canvas.width - 80, canvas.height - 80);

  // Subtle star dots
  ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
  const starCoords = [
    [100, 120, 2], [300, 90, 1.5], [950, 140, 2.5], [1100, 220, 1.8],
    [80, 500, 2], [1050, 600, 2.2], [200, 750, 1.5], [1000, 800, 2],
    [600, 80, 2], [450, 820, 1.6], [800, 780, 1.8]
  ];
  for (const [x, y, r] of starCoords) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
  }

  // Header Title
  ctx.fillStyle = '#c084fc';
  ctx.font = 'bold 20px "Plus Jakarta Sans", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('🔮 CLOUD HOROSCOPE • ARCHITECTURAL REPORT', 600, 90);

  // Main Name
  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 44px "Plus Jakarta Sans", sans-serif';
  ctx.fillText(`${name}'s Cosmic Reading`, 600, 150);

  // Subtitle (Date of birth + Sign)
  ctx.fillStyle = '#94a3b8';
  ctx.font = '18px "Plus Jakarta Sans", sans-serif';
  ctx.fillText(`Born: ${dobFormatted}  •  ${horoscopeData.sign} ${horoscopeData.symbol} (${horoscopeData.dates})  •  Element: ${horoscopeData.element}`, 600, 190);

  // Horoscope Content Box
  ctx.fillStyle = 'rgba(255, 255, 255, 0.06)';
  ctx.beginPath();
  ctx.roundRect(80, 230, 1040, 360, 24);
  ctx.fill();
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
  ctx.lineWidth = 1.5;
  ctx.stroke();

  // Forecast Label
  ctx.fillStyle = '#f472b6';
  ctx.font = 'bold 16px "Plus Jakarta Sans", sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('⚡ ARCHITECTURAL FORECAST & CLOUD DESTINY', 120, 275);

  // Horoscope Text
  ctx.fillStyle = '#f8fafc';
  ctx.font = 'italic 24px "Plus Jakarta Sans", sans-serif';
  const lines = wrapText(ctx, `"${horoscopeData.horoscope}"`, 960);
  let startY = 325;
  for (const line of lines) {
    ctx.fillText(line, 120, startY);
    startY += 38;
  }

  // 3 Metric Cards at the bottom
  const metrics = [
    { label: 'LUCKY AWS SERVICE', value: horoscopeData.luckyService, color: '#c084fc' },
    { label: 'OPTIMAL CLOUD REGION', value: horoscopeData.luckyRegion, color: '#60a5fa' },
    { label: 'SERVERLESS RESILIENCE', value: `${horoscopeData.resilienceScore}% Uptime`, color: '#34d399' }
  ];

  const cardWidth = 325;
  const startX = 80;
  const gap = 32;

  metrics.forEach((m, idx) => {
    const x = startX + idx * (cardWidth + gap);
    const y = 620;

    // Card background
    ctx.fillStyle = 'rgba(15, 23, 42, 0.7)';
    ctx.beginPath();
    ctx.roundRect(x, y, cardWidth, 130, 18);
    ctx.fill();
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Card label
    ctx.fillStyle = '#94a3b8';
    ctx.font = 'bold 13px "Plus Jakarta Sans", sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText(m.label, x + 20, y + 40);

    // Card value
    ctx.fillStyle = m.color;
    ctx.font = 'bold 18px "Plus Jakarta Sans", sans-serif';
    ctx.fillText(m.value, x + 20, y + 80);
  });

  // Footer branding
  ctx.fillStyle = '#64748b';
  ctx.font = '14px "Plus Jakarta Sans", sans-serif';
  ctx.textAlign = 'center';
  const dateStr = new Date().toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
  ctx.fillText(`Generated on ${dateStr} • Powered by AWS Bedrock AI & Cloud Horoscope`, 600, 830);

  // Trigger download
  const link = document.createElement('a');
  const safeName = name.toLowerCase().replace(/[^a-z0-9]/g, '-');
  link.download = `cloud-horoscope-${safeName}-${horoscopeData.sign.toLowerCase()}.png`;
  link.href = canvas.toDataURL('image/png');
  link.click();
}

/**
 * Downloads a structured Markdown report
 */
export function downloadHoroscopeMarkdown({ name, dobFormatted, horoscopeData }) {
  const content = `# 🔮 Cloud Horoscope Architectural Report

**Consultant:** ${name}  
**Date of Birth:** ${dobFormatted}  
**Zodiac Sign:** ${horoscopeData.sign} ${horoscopeData.symbol} (${horoscopeData.dates})  
**Cosmic Element:** ${horoscopeData.element}  
**Date of Reading:** ${new Date().toLocaleDateString()}  

---

## ⚡ Architectural Horoscope & Cosmic Reading
> "${horoscopeData.horoscope}"

---

## ☁️ Cloud Destiny Attributes
- **Lucky AWS Service:** ${horoscopeData.luckyService}
- **Optimal Cloud Region:** ${horoscopeData.luckyRegion}
- **Serverless Resilience Rating:** ${horoscopeData.resilienceScore}% Uptime
- **Engine Provider:** ${horoscopeData.author} (${horoscopeData.project})

---
*Generated by Cloud Horoscope powered by Amazon Bedrock AI & AWS Serverless Architecture.*
`;

  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  const safeName = name.toLowerCase().replace(/[^a-z0-9]/g, '-');
  link.download = `cloud-horoscope-${safeName}.md`;
  link.href = url;
  link.click();
  URL.revokeObjectURL(url);
}
