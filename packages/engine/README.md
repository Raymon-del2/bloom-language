# @bloom/engine

Core Bloom engine and runtime.

## Installation

```bash
npm install @bloom/engine
```

## Features

- **Sieve** - Cryptographic verification system
- **Pulse** - Live development server with HMR
- **Crystalize** - Build system for multiple targets

## Usage

```typescript
import { Sieve, Pulse, Crystalize } from '@bloom/engine';

// Initialize the Sieve
const sieve = new Sieve({ level: 'strict' });

// Start Pulse server
const pulse = new Pulse({ port: 8080 });
await pulse.start();

// Crystalize for production
const crystal = new Crystalize({ target: 'web' });
await crystal.build();
```

## License

MIT
