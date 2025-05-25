"use client";
import { Button } from "@/components/ui/button";
import { useTranslations } from "next-intl";

export function Hero() {
  const t = useTranslations("landing.hero");
  return (
    <section className="relative py-24 text-center">
      <video
        src="/assets/bg-hero.mp4"
        autoPlay muted loop
        className="absolute inset-0 h-full w-full object-cover opacity-25 -z-10"
      />
      <h1 className="text-4xl md:text-6xl font-extrabold">{t("title")}</h1>
      <p className="mt-4 text-lg md:text-2xl text-muted-foreground">
        {t("subtitle")}
      </p>
      <div className="mt-8 flex justify-center gap-4">
        <Button asChild size="lg">
          <a href="/auth/register">{t("ctaStart")}</a>
        </Button>
        <Button variant="outline" asChild size="lg">
          <a href="/pricing">{t("ctaPricing")}</a>
        </Button>
      </div>
    </section>
  );
} 