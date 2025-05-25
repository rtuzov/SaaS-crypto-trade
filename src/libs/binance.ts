import crypto from 'crypto';

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
  stop_loss: number;
  take_profit: number;
  timestamp: string;
}

interface UserPositions {
  user_id: string;
  positions: Position[];
  total_pnl: number;
  total_pnl_percentage: number;
  last_update: string;
}

export class BinanceClient {
  private baseUrl = 'https://fapi.binance.com';
  private apiKey: string;
  private apiSecret: string;

  constructor(apiKey: string, apiSecret: string) {
    this.apiKey = apiKey;
    this.apiSecret = apiSecret;
  }

  private generateSignature(queryString: string): string {
    return crypto
      .createHmac('sha256', this.apiSecret)
      .update(queryString)
      .digest('hex');
  }

  private async request(endpoint: string, method: string = 'GET', params: Record<string, string> = {}) {
    const timestamp = Date.now().toString();
    const queryString = Object.entries({ ...params, timestamp })
      .map(([key, value]) => `${key}=${value}`)
      .join('&');

    const signature = this.generateSignature(queryString);
    const url = `${this.baseUrl}${endpoint}?${queryString}&signature=${signature}`;

    const response = await fetch(url, {
      method,
      headers: {
        'X-MBX-APIKEY': this.apiKey,
      },
    });

    if (!response.ok) {
      throw new Error(`Binance API error: ${response.statusText}`);
    }

    return response.json();
  }

  async getPositions(): Promise<UserPositions> {
    const positions = await this.request('/fapi/v2/positionRisk');
    
    const formattedPositions = positions
      .filter((p: any) => parseFloat(p.positionAmt) !== 0)
      .map((p: any) => ({
        symbol: p.symbol,
        side: parseFloat(p.positionAmt) > 0 ? 'long' : 'short',
        entry_price: parseFloat(p.entryPrice),
        current_price: parseFloat(p.markPrice),
        size: Math.abs(parseFloat(p.positionAmt)),
        leverage: parseFloat(p.leverage),
        pnl: parseFloat(p.unRealizedProfit),
        pnl_percentage: (parseFloat(p.unRealizedProfit) / (parseFloat(p.entryPrice) * Math.abs(parseFloat(p.positionAmt)))) * 100,
        liquidation_price: parseFloat(p.liquidationPrice),
        stop_loss: 0, // TODO: Implement stop loss tracking
        take_profit: 0, // TODO: Implement take profit tracking
        timestamp: new Date().toISOString(),
      }));

    const totalPnl = formattedPositions.reduce((sum: number, p: Position) => sum + p.pnl, 0);
    const totalPnlPercentage = formattedPositions.reduce((sum: number, p: Position) => sum + p.pnl_percentage, 0);

    return {
      user_id: this.apiKey,
      positions: formattedPositions,
      total_pnl: totalPnl,
      total_pnl_percentage: totalPnlPercentage,
      last_update: new Date().toISOString(),
    };
  }

  async closePosition(symbol: string, side: string): Promise<void> {
    const position = await this.request('/fapi/v2/positionRisk', 'GET', { symbol });
    const positionAmt = parseFloat(position[0].positionAmt);
    
    if (positionAmt === 0) {
      throw new Error('Position not found');
    }

    const quantity = Math.abs(positionAmt);
    const orderSide = side === 'long' ? 'SELL' : 'BUY';

    await this.request('/fapi/v1/order', 'POST', {
      symbol,
      side: orderSide,
      type: 'MARKET',
      quantity: quantity.toString(),
    });
  }
} 