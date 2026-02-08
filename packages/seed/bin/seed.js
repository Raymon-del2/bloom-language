#!/usr/bin/env node
import { createSeed } from '../dist/seed.js';

const name = process.argv[2];
if (!name) {
  console.error('Usage: bloom-seed <name>');
  process.exit(1);
}

createSeed(name);
