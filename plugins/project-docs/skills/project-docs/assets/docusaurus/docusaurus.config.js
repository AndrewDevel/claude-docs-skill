// @ts-check
// Plantilla de configuración de Docusaurus / Docusaurus config template.
// Reemplazar los placeholders {{...}} al hacer scaffolding.
const { themes } = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: '{{PROJECT_NAME}}',
  tagline: 'Documentación técnica, de plataforma y de API / Technical, platform & API docs',
  favicon: 'img/favicon.ico',

  url: 'https://{{GH_USER}}.github.io',
  baseUrl: '/{{GH_REPO}}/',

  organizationName: '{{GH_USER}}',
  projectName: '{{GH_REPO}}',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Diagramas Mermaid (arquitectura, secuencia, ER) embebidos en Markdown.
  markdown: { mermaid: true },
  themes: ['@docusaurus/theme-mermaid'],

  i18n: {
    defaultLocale: 'es',
    locales: ['es', 'en'],
    localeConfigs: {
      es: { label: 'Español' },
      en: { label: 'English' },
    },
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: '{{REPO_URL}}/tree/main/docs/',
          showLastUpdateTime: true,
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/logo.png',
      // Barra superior con aviso (editable o eliminable).
      announcementBar: {
        id: 'docs_wip',
        content:
          '📘 Documentación viva — se actualiza con cada cambio del código. / Living docs — updated on every code change.',
        backgroundColor: '#2d3142',
        textColor: '#ffffff',
        isCloseable: true,
      },
      colorMode: {
        defaultMode: 'light',
        respectPrefersColorScheme: true,
      },
      // Diagramas con tema claro/oscuro coherente.
      mermaid: {
        theme: { light: 'neutral', dark: 'dark' },
      },
      docs: {
        sidebar: { hideable: true, autoCollapseCategories: true },
      },
      navbar: {
        title: '{{PROJECT_NAME}}',
        hideOnScroll: true,
        logo: {
          alt: '{{PROJECT_NAME}} logo',
          src: 'img/logo.png',
        },
        items: [
          { type: 'docSidebar', sidebarId: 'docs', position: 'left', label: 'Docs' },
          { type: 'localeDropdown', position: 'right' },
          {
            href: '{{REPO_URL}}',
            position: 'right',
            className: 'header-github-link',
            'aria-label': 'GitHub repository',
          },
        ],
      },
      footer: {
        style: 'dark',
        copyright: `© ${new Date().getFullYear()} {{PROJECT_NAME}}. Hecho con Docusaurus.`,
      },
      prism: {
        theme: themes.github,
        darkTheme: themes.dracula,
        // Lenguajes extra usados en los ejemplos de las plantillas.
        additionalLanguages: ['bash', 'json', 'typescript', 'swift', 'sql', 'diff'],
      },
    }),
};

module.exports = config;
