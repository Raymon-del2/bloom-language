// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
	site: 'https://bloom-language.vercel.app',
	image: {
		service: {
			entrypoint: 'astro/assets/services/noop',
		},
	},
	integrations: [
		starlight({
			title: 'Bloom',
			description: 'Bloom - The Local-First AI Engine. Plant your code, watch it grow.',
			logo: {
				src: './src/assets/bloom-logo.webp',
				alt: 'Bloom Framework - Local-First AI Engine',
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/bloom' },
			],
			customCss: [
				'./src/styles/custom.css',
			],
			sidebar: [
				{
					label: 'Getting Started',
					items: [
						{ label: 'Quick Start', slug: 'guides/quick-start' },
						{ label: 'Installation', slug: 'guides/installation' },
						{ label: 'Your First Seed', slug: 'guides/first-seed' },
					],
				},
				{
					label: 'Guides',
					items: [
						{ label: 'The Sieve', slug: 'guides/sieve' },
						{ label: 'Crystalize', slug: 'guides/crystalize' },
						{ label: 'Pulse Server', slug: 'guides/pulse' },
					],
				},
				{
					label: 'Reference',
					autogenerate: { directory: 'reference' },
				},
			],
			head: [
				{
					tag: 'meta',
					attrs: {
						property: 'og:image',
						content: '/bloom-og.webp',
					},
				},
				{
					tag: 'meta',
					attrs: {
						property: 'twitter:image',
						content: '/bloom-og.webp',
					},
				},
				{
					tag: 'script',
					attrs: {
						type: 'application/ld+json',
					},
					content: JSON.stringify({
						'@context': 'https://schema.org',
						'@type': 'SoftwareApplication',
						name: 'Bloom',
						applicationCategory: 'DeveloperApplication',
						description: 'The Local-First AI Engine. Plant your code, watch it grow.',
						url: 'https://bloom.dev',
						sameAs: [
							'https://github.com/bloom'
						],
						offers: {
							'@type': 'Offer',
							price: '0',
							priceCurrency: 'USD'
						}
					}),
				},
			],
		}),
		tailwind({
			applyBaseStyles: false,
		}),
	],
});
