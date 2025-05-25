import { FuturesMonitor } from "@/components/modules/FuturesMonitor";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex flex-col space-y-4">
      {children}
      <FuturesMonitor />
    </div>
  );
} 