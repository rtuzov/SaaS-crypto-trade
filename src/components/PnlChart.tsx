'use client';

import type { IChartApi } from 'lightweight-charts';
import { ColorType, createChart } from 'lightweight-charts';
import { useEffect, useRef } from 'react';
import { useSubscription } from 'urql';

const LIVE_PNL_SUBSCRIPTION = `
  subscription LivePnl($traderId: ID!) {
    live_pnl(trader_id: $traderId) {
      timestamp
      value
    }
  }
`;

type PnlData = {
  timestamp: number;
  value: number;
};

export function PnlChart({ traderId }: { traderId: string }) {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<any>(null);

  const [result] = useSubscription({
    query: LIVE_PNL_SUBSCRIPTION,
    variables: { traderId },
  });

  useEffect(() => {
    if (chartContainerRef.current) {
      const chart = createChart(chartContainerRef.current, {
        layout: {
          background: { type: ColorType.Solid, color: 'transparent' },
          textColor: '#d1d4dc',
        },
        grid: {
          vertLines: { color: 'rgba(42, 46, 57, 0.5)' },
          horzLines: { color: 'rgba(42, 46, 57, 0.5)' },
        },
        width: chartContainerRef.current.clientWidth,
        height: 300,
      });

      const series = chart.addLineSeries({
        color: '#2962FF',
        lineWidth: 2,
      });

      chartRef.current = chart;
      seriesRef.current = series;

      const handleResize = () => {
        if (chartContainerRef.current) {
          chart.applyOptions({
            width: chartContainerRef.current.clientWidth,
          });
        }
      };

      window.addEventListener('resize', handleResize);

      return () => {
        window.removeEventListener('resize', handleResize);
        chart.remove();
      };
    }
  }, []);

  useEffect(() => {
    if (result.data?.live_pnl && seriesRef.current) {
      const pnlData: PnlData = result.data.live_pnl;
      seriesRef.current.update({
        time: pnlData.timestamp,
        value: pnlData.value,
      });
    }
  }, [result.data]);

  return (
    <div className="h-[300px] w-full rounded-lg bg-background p-4">
      <div ref={chartContainerRef} className="size-full" />
    </div>
  );
}
