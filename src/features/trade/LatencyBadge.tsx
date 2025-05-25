'use client';

import { useEffect, useState } from 'react';

export function LatencyBadge() {
  const [latency, setLatency] = useState<number | null>(null);
  const [status, setStatus] = useState<'good' | 'warning' | 'error'>('good');

  useEffect(() => {
    const checkLatency = async () => {
      const start = performance.now();
      try {
        const response = await fetch('/api/ping');
        if (!response.ok) {
          throw new Error('Failed to ping server');
        }
        const end = performance.now();
        const newLatency = Math.round(end - start);
        setLatency(newLatency);

        // Update status based on latency
        if (newLatency < 100) {
          setStatus('good');
        } else if (newLatency < 300) {
          setStatus('warning');
        } else {
          setStatus('error');
        }
      } catch (error) {
        setStatus('error');
        setLatency(null);
      }
    };

    // Check latency immediately
    checkLatency();

    // Then check every 5 seconds
    const interval = setInterval(checkLatency, 5000);

    return () => clearInterval(interval);
  }, []);

  const getStatusColor = () => {
    switch (status) {
      case 'good':
        return 'bg-green-100 text-green-800';
      case 'warning':
        return 'bg-yellow-100 text-yellow-800';
      case 'error':
        return 'bg-red-100 text-red-800';
    }
  };

  return (
    <div
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${getStatusColor()}`}
    >
      <span className="mr-1.5 size-2 rounded-full bg-current" />
      {latency ? `${latency}ms` : 'Offline'}
    </div>
  );
}
