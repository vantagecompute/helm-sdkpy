// Copyright 2025 Vantage Compute
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import * as fs from 'fs';
import * as path from 'path';

// Function to read version from pyproject.toml
function getVersionFromPyproject(): string {
  try {
    const pyprojectPath = path.join(__dirname, '../pyproject.toml');
    const content = fs.readFileSync(pyprojectPath, 'utf8');
    
    // Extract version using regex
    const versionMatch = content.match(/^version\s*=\s*["']([^"']+)["']/m);
    
    if (versionMatch) {
      return versionMatch[1];
    }
    
    throw new Error('Version not found in pyproject.toml');
  } catch (error) {
    console.error('Error reading version from pyproject.toml:', error);
    return '0.0.0'; // fallback version
  }
}

const projectVersion = getVersionFromPyproject();

const config: Config = {
  title: 'helm-sdkpy',
  tagline: `Python bindings for Helm - v${projectVersion}`,
  favicon: 'img/favicon.ico',

  url: 'https://vantagecompute.github.io',
  baseUrl: '/helm-sdkpy/',

  organizationName: 'vantagecompute',
  projectName: 'helm-sdkpy',
  deploymentBranch: 'main',
  trailingSlash: false,

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  markdown: {
    format: 'detect',
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn'
    }
  },
  themes: ['@docusaurus/theme-mermaid'],
  presets: [
    [
      'classic',
      {
        docs: {
          path: './docs',
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/vantagecompute/helm-sdkpy/tree/main/docusaurus/docs/',
          sidebarCollapsible: true,
          sidebarCollapsed: false,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],
  plugins: [
    [ 
      'docusaurus-plugin-llms',
      {
        // Options here
        generateLLMsTxt: true,
        generateLLMsFullTxt: true,
        docsDir: 'docs',
        ignoreFiles: ['advanced/*', 'private/*'],
        title: 'helm-sdkpy Documentation',
        description: 'Python bindings for Helm - Kubernetes package manager',
        includeBlog: false,
        // Content cleaning options
        excludeImports: true,
          removeDuplicateHeadings: true,
          // Generate individual markdown files following llmstxt.org specification
          generateMarkdownFiles: true,
          // Control documentation order
          includeOrder: [],
          includeUnmatchedLast: true,
          // Path transformation options
          pathTransformation: {
            // Paths to ignore when constructing URLs (will be removed if found)
            ignorePaths: ['docs'],
            // Paths to add when constructing URLs (will be prepended if not already present)
            // addPaths: ['api'],
          },
          // Custom LLM files for specific documentation sections
          customLLMFiles: [
            {
              filename: 'llms-index.txt',
              includePatterns: ['docs/index.md'],
              fullContent: true,
              title: 'helm-sdkpy Documentation Index',
              description: 'Index reference for helm-sdkpy'
            },
            {
              filename: 'llms-installation.txt',
              includePatterns: ['docs/installation.md'],
              fullContent: true,
              title: 'helm-sdkpy Installation Guide',
              description: 'Installation documentation for helm-sdkpy'
            },
            {
              filename: 'llms-quickstart.txt',
              includePatterns: ['docs/quickstart.md'],
              fullContent: true,
              title: 'helm-sdkpy Quick Start Guide',
              description: 'Quick start guide to get up and running with helm-sdkpy'
            },
            {
              filename: 'llms-usage.txt',
              includePatterns: ['docs/usage.md'],
              fullContent: true,
              title: 'helm-sdkpy Usage Documentation',
              description: 'Usage documentation and examples for helm-sdkpy'
            },
            {
              filename: 'llms-architecture.txt',
              includePatterns: ['docs/architecture/**/*.md'],
              fullContent: true,
              title: 'helm-sdkpy Architecture Documentation',
              description: 'Complete architecture documentation for helm-sdkpy including core architecture and build/packaging'
            },
            {
              filename: 'llms-examples.txt',
              includePatterns: ['docs/examples/**/*.md'],
              fullContent: true,
              title: 'helm-sdkpy Examples',
              description: 'Practical examples for helm-sdkpy including chart installation, upgrades, release management, repository management, concurrent operations, and error handling'
            },
            {
              filename: 'llms-api-reference.txt',
              includePatterns: ['docs/api/**/*.md'],
              fullContent: true,
              title: 'helm-sdkpy API Reference',
              description: 'Complete API reference for helm-sdkpy actions, chart, repo, and exceptions'
            },
            {
              filename: 'llms-troubleshooting.txt',
              includePatterns: ['docs/troubleshooting.md'],
              fullContent: true,
              title: 'helm-sdkpy Troubleshooting',
              description: 'Troubleshooting documentation for helm-sdkpy'
            },
          ],
        },
    ],
  ],

  customFields: {
    projectVersion: projectVersion,
  },

  themeConfig: {
    navbar: {
      title: `helm-sdkpy Documentation v${projectVersion}`,
      logo: {
        alt: 'Vantage Compute Logo',
        src: 'https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-white-horz.png',
        srcDark: 'https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-white-horz.png',
        href: 'https://vantagecompute.github.io/helm-sdkpy/',
        target: '_self',
      },
      items: [
        {
          href: 'https://pypi.org/project/helm-sdkpy/',
          label: 'PyPI',
          position: 'right',
          className: 'pypi-button',
        },
        {
          href: 'https://github.com/vantagecompute/helm-sdkpy',
          label: 'GitHub',
          position: 'right',
          className: 'github-button',
        },
      ],
    },
    footer: {
      style: 'dark',
      logo: {
        alt: 'Vantage Compute Logo',
        src: 'https://vantage-compute-public-assets.s3.us-east-1.amazonaws.com/branding/vantage-logo-text-white-horz.png',
        href: 'https://vantagecompute.ai',
      },
      links: [
        {
          title: 'Documentation',
          items: [
            {
              label: 'Installation',
              to: '/installation',
            },
            {
              label: 'Usage Examples',
              to: '/usage',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub Discussions',
              href: 'https://github.com/vantagecompute/helm-sdkpy/discussions',
            },
            {
              label: 'Issues',
              href: 'https://github.com/vantagecompute/helm-sdkpy/issues',
            },
            {
              label: 'Support',
              href: 'https://vantagecompute.ai/support',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/vantagecompute/helm-sdkpy',
            },
            {
              label: 'Vantage Compute',
              href: 'https://vantagecompute.ai',
            },
            {
              label: 'PyPI',
              href: 'https://pypi.org/project/helm-sdkpy/',
            },
          ],
        },
      ],
      copyright: 'Copyright &copy; ' + new Date().getFullYear() + ' Vantage Compute.',
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['shell-session', 'python', 'bash'],
    },
    tableOfContents: {
      minHeadingLevel: 2,
      maxHeadingLevel: 5,
    },
  },
};

export default config;
