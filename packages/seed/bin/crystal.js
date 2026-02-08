#!/usr/bin/env node
import { crystalize } from '../dist/crystal.js';

crystalize(process.argv[2] || '.');
