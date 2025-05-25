import sharp from 'sharp';
import { promises as fs } from 'fs';
import path from 'path';

const sizes = [192, 512];

async function generateIcons() {
  const svgBuffer = await fs.readFile(path.join(process.cwd(), 'public', 'icons', 'icon.svg'));
  
  for (const size of sizes) {
    await sharp(svgBuffer)
      .resize(size, size)
      .png()
      .toFile(path.join(process.cwd(), 'public', 'icons', `icon-${size}x${size}.png`));
  }
}

generateIcons().catch(console.error); 