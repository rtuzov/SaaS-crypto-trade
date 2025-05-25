import { Button } from "@/components/ui/button";
type Props = { title: string; price: string; features: string[]; cta: string; highlight?: boolean };
export default function TariffCard({ title, price, features, cta, highlight }: Props) {
  return (
    <div className={`rounded-2xl border p-6 ${highlight ? "ring-2 ring-primary" : ""}`}>
      <h3 className="text-xl font-semibold">{title}</h3>
      <p className="my-4 text-3xl font-bold">{price}</p>
      <ul className="space-y-1 mb-6 text-sm">
        {features.map((f) => <li key={f}>• {f}</li>)}
      </ul>
      <Button asChild className="w-full">
        <a href="/api/checkout">{cta}</a>
      </Button>
    </div>
  );
} 