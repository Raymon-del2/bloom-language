# @bloom/seed

CLI for Bloom seed creation and management.

## Installation

```bash
npm install @bloom/seed
```

## Usage

```bash
# Create a new seed
bloom-seed my-app

# Initialize a project
bloom-init

# Crystalize for production
bloom-crystal

# Sprout a preview
bloom-sprout
```

## API

### `createSeed(name: string, options?: SeedOptions): Promise<Seed>`

Creates a new Bloom seed.

### `initProject(path?: string): Promise<void>`

Initializes a Bloom project in the specified directory.

## License

MIT
