"use client";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

type Props = {
  series: { timestamp: string; value: number }[];
};

export default function PnlChart({ series }: Props) {
  const data = {
    labels: series.map((s) => new Date(s.timestamp).toLocaleDateString()),
    datasets: [
      {
        label: "PnL",
        data: series.map((s) => s.value),
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      },
    ],
  };

  return <Line data={data} />;
} 