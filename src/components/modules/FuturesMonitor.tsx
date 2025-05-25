'use client';

import React, { useEffect, useState } from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Switch } from "@/components/ui/switch";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";
import { formatNumber } from "@/libs/utils";

interface Position {
  symbol: string;
  side: string;
  entry_price: number;
  current_price: number;
  size: number;
  leverage: number;
  pnl: number;
  pnl_percentage: number;
  liquidation_price: number;
  timestamp: string;
}

interface UserPositions {
  user_id: string;
  positions: Position[];
  total_pnl: number;
  total_pnl_percentage: number;
  last_update: string;
}

interface MonitorSettings {
  update_interval: number;
  alert_threshold: number;
  enabled: boolean;
}

export function FuturesMonitor() {
  const [mounted, setMounted] = useState(false);
  const [positions, setPositions] = useState<UserPositions | null>(null);
  const [settings, setSettings] = useState<MonitorSettings>({
    update_interval: 5,
    alert_threshold: 0.05,
    enabled: false
  });
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    setMounted(true);
  }, []);

  const fetchPositions = async () => {
    try {
      const response = await fetch('/api/v1/futures-monitor/positions');
      if (response.ok) {
        const data = await response.json();
        setPositions(data);
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch positions",
        variant: "destructive"
      });
    }
  };

  const fetchSettings = async () => {
    try {
      const response = await fetch('/api/v1/futures-monitor/settings');
      if (response.ok) {
        const data = await response.json();
        setSettings(data);
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch settings",
        variant: "destructive"
      });
    }
  };

  const updateSettings = async (newSettings: MonitorSettings) => {
    try {
      const response = await fetch('/api/v1/futures-monitor/settings', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newSettings)
      });
      
      if (response.ok) {
        setSettings(newSettings);
        toast({
          title: "Success",
          description: "Settings updated"
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to update settings",
        variant: "destructive"
      });
    }
  };

  const toggleMonitoring = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `/api/v1/futures-monitor/${settings.enabled ? 'stop' : 'start'}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(settings)
        }
      );
      
      if (response.ok) {
        setSettings(prev => ({ ...prev, enabled: !prev.enabled }));
        toast({
          title: "Success",
          description: `Monitoring ${settings.enabled ? 'stopped' : 'started'}`
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to toggle monitoring",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (mounted) {
      fetchSettings();
      if (settings.enabled) {
        fetchPositions();
        const interval = setInterval(fetchPositions, settings.update_interval * 1000);
        return () => clearInterval(interval);
      }
    }
    return undefined;
  }, [mounted, settings.enabled, settings.update_interval]);

  if (!mounted) {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Futures Monitor</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Switch
                checked={settings.enabled}
                onCheckedChange={toggleMonitoring}
                disabled={loading}
              />
              <Label>Enable Monitoring</Label>
            </div>
            <div className="flex items-center space-x-2">
              <Label>Update Interval (s)</Label>
              <Input
                type="number"
                value={settings.update_interval}
                onChange={(e) => updateSettings({
                  ...settings,
                  update_interval: parseInt(e.target.value)
                })}
                min={1}
                max={60}
                className="w-20"
              />
            </div>
          </div>

          {positions && (
            <>
              <div className="grid grid-cols-2 gap-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Total PnL</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">
                      {formatNumber(positions.total_pnl)} USDT
                    </div>
                    <div className={`text-sm ${
                      positions.total_pnl_percentage >= 0 ? 'text-green-500' : 'text-red-500'
                    }`}>
                      {formatNumber(positions.total_pnl_percentage)}%
                    </div>
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle>Last Update</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="text-sm">
                      {new Date(positions.last_update).toLocaleString()}
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Symbol</TableHead>
                    <TableHead>Side</TableHead>
                    <TableHead>Size</TableHead>
                    <TableHead>Entry Price</TableHead>
                    <TableHead>Current Price</TableHead>
                    <TableHead>PnL</TableHead>
                    <TableHead>PnL %</TableHead>
                    <TableHead>Liquidation</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {positions.positions.map((position) => (
                    <TableRow key={position.symbol}>
                      <TableCell>{position.symbol}</TableCell>
                      <TableCell className={
                        position.side === 'long' ? 'text-green-500' : 'text-red-500'
                      }>
                        {position.side.toUpperCase()}
                      </TableCell>
                      <TableCell>{formatNumber(position.size)}</TableCell>
                      <TableCell>{formatNumber(position.entry_price)}</TableCell>
                      <TableCell>{formatNumber(position.current_price)}</TableCell>
                      <TableCell className={
                        position.pnl >= 0 ? 'text-green-500' : 'text-red-500'
                      }>
                        {formatNumber(position.pnl)}
                      </TableCell>
                      <TableCell className={
                        position.pnl_percentage >= 0 ? 'text-green-500' : 'text-red-500'
                      }>
                        {formatNumber(position.pnl_percentage)}%
                      </TableCell>
                      <TableCell>{formatNumber(position.liquidation_price)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </>
          )}
        </div>
      </CardContent>
    </Card>
  );
} 