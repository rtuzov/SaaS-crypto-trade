"use client";

export default function GlobalError({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <html>
      <body>
        <h2>Что-то пошло не так</h2>
        <pre>{error.message}</pre>
        <button onClick={() => reset()}>Попробовать снова</button>
      </body>
    </html>
  );
} 