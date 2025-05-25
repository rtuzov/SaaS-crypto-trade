"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function Trade() {
  const [cmd, setCmd] = useState("");
  const [log, setLog] = useState<string[]>([]);
  const send = async () => {
    if (!cmd) return;
    setLog((prev) => [...prev, `> ${cmd}`]);
    await fetch("/api/execute_trade", { method: "POST", body: JSON.stringify({ cmd }) });
    setCmd("");
  };
  return (
    <section className="container py-10 grid gap-6 md:grid-cols-[2fr_1fr]">
      <div className="border rounded-lg p-4 flex flex-col">
        <div className="flex-1 overflow-y-auto text-sm mb-4">
          {log.map((m, i) => (<p key={i}>{m}</p>))}
        </div>
        <div className="flex gap-2">
          <Input value={cmd} onChange={(e) => setCmd(e.target.value)} placeholder="btc long 0.05 5x tp 70000 sl 64000" />
          <Button onClick={send}>Send</Button>
        </div>
      </div>
      <aside className="border rounded-lg p-4"> {/* History drawer placeholder */}</aside>
    </section>
  );
} 