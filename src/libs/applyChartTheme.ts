export const applyChartTheme = (chart: any, dark: boolean) => {
  chart.applyOptions({
    layout: { background: { color: "transparent" }, textColor: dark ? "#F5F7FA" : "#0F111A" },
    grid: { vertLines: { color: "transparent" }, horzLines: { color: "transparent" } },
    timeScale: { borderColor: "transparent" },
    crosshair: { vertLine: { visible: false }, horzLine: { visible: false } }
  });
}; 