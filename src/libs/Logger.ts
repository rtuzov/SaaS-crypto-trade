import logtail from '@logtail/pino';
import pino, { type DestinationStream } from 'pino';
import pretty from 'pino-pretty';

import { Env } from './Env';

export async function initLogger() {
  let stream: DestinationStream;

  if (Env.LOGTAIL_SOURCE_TOKEN) {
    stream = pino.multistream([
      await logtail({
        sourceToken: Env.LOGTAIL_SOURCE_TOKEN,
        options: {
          sendLogsToBetterStack: true,
        },
      }),
      {
        stream: pretty(), // Prints logs to the console
      },
    ]);
  } else {
    stream = pretty({
      colorize: true,
    });
  }

  return pino({ base: undefined }, stream);
}

export const logger = initLogger();
