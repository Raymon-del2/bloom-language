#!/usr/bin/env node
import { initProject } from '../dist/init.js';

initProject(process.argv[2] || '.');
