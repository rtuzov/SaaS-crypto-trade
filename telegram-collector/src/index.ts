import dotenv from 'dotenv';
import { Kafka } from 'kafkajs';
import { TelegramClient } from 'telegram';
import { NewMessage } from 'telegram/events';
import { StringSession } from 'telegram/sessions';

import { parseSignal } from './signalParser';

dotenv.config();

// Telegram configuration
const apiId = Number.parseInt(process.env.TELEGRAM_API_ID!);
const apiHash = process.env.TELEGRAM_API_HASH!;
const session = new StringSession(process.env.TELEGRAM_SESSION || '');

// Kafka configuration
const kafka = new Kafka({
  clientId: 'telegram-collector',
  brokers: [process.env.KAFKA_BROKER || 'redpanda:9092'],
  retry: {
    initialRetryTime: 100,
    retries: 8
  },
  connectionTimeout: 3000,
});

const producer = kafka.producer({
  allowAutoTopicCreation: true,
  transactionTimeout: 30000
});

// Channel IDs to monitor
const CHANNELS = [
  'cryptosignals',
  'binance_signals',
  'crypto_alerts',
].map(id => Number.parseInt(id));

async function start() {
  let retryCount = 0;
  const maxRetries = 5;

  while (retryCount < maxRetries) {
    try {
      // Initialize Telegram client
      const client = new TelegramClient(session, apiId, apiHash, {
        connectionRetries: 5,
      });

      await client.start({
        phoneNumber: process.env.TELEGRAM_PHONE || '',
        password: async () => process.env.TELEGRAM_PASSWORD!,
        phoneCode: async () => process.env.TELEGRAM_CODE!,
        onError: err => console.error(err),
      });

      console.log('Telegram client started');

      // Connect to Kafka with retry
      try {
        await producer.connect();
        console.log('Kafka producer connected');
      } catch (error) {
        console.error('Failed to connect to Kafka:', error);
        throw error;
      }

      // Subscribe to channel messages
      for (const channelId of CHANNELS) {
        client.addEventHandler(async (event) => {
          const message = event.message;

          if ('channelId' in message.peerId && message.peerId.channelId.toString() === channelId.toString()) {
            try {
              const signal = parseSignal(message.text);
              if (signal) {
                await producer.send({
                  topic: 'trading-signals',
                  messages: [
                    {
                      key: channelId.toString(),
                      value: JSON.stringify({
                        ...signal,
                        source: 'telegram',
                        channel_id: channelId,
                        timestamp: Date.now(),
                      }),
                    },
                  ],
                });
                console.log('Signal sent to Kafka:', signal);
              }
            } catch (error) {
              console.error('Error processing message:', error);
            }
          }
        }, new NewMessage({}));
      }

      // Keep the process running
      process.on('SIGINT', async () => {
        await client.disconnect();
        await producer.disconnect();
        process.exit(0);
      });

      break;
    } catch (error) {
      retryCount++;
      console.error(`Attempt ${retryCount} failed:`, error);
      if (retryCount === maxRetries) {
        console.error('Max retries reached. Exiting...');
        process.exit(1);
      }
      await new Promise(resolve => setTimeout(resolve, 5000 * retryCount));
    }
  }
}

start().catch(console.error);
