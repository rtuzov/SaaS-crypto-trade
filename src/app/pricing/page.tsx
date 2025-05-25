import TariffCard from "@/components/pricing/TariffCard";

export const metadata = { title: "Pricing – Trading SaaS" };

export default async function PricingPage() {
  const plans = [
    { title: "Starter", price: "$0 / mo", features: ["Demo data"], cta: "Sign up" },
    { title: "Pro", price: "$29 / mo", features: ["Live trading", "CSV analytics"], cta: "Subscribe", highlight: true },
    { title: "Enterprise", price: "Custom", features: ["Unlimited"], cta: "Contact us" }
  ];
  return (
    <section className="py-24 container grid md:grid-cols-3 gap-8">
      {plans.map((p) => <TariffCard key={p.title} {...p} />)}
    </section>
  );
} 