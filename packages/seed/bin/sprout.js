#!/usr/bin/env node
import { sprout } from '../dist/sprout.js';

sprout(process.argv[2] || '.');
