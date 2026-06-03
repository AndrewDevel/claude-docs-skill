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
      navbar: {
        title: '{{PROJECT_NAME}}',
        items: [
          { type: 'docSidebar', sidebarId: 'docs', position: 'left', label: 'Docs' },
          { type: 'localeDropdown', position: 'right' },
          { href: '{{REPO_URL}}', label: 'GitHub', position: 'right' },
        ],
      },
      footer: {
        style: 'dark',
        copyright: `© ${new Date().getFullYear()} {{PROJECT_NAME}}.`,
      },
      prism: {
        theme: themes.github,
        darkTheme: themes.dracula,
      },
    }),
};

module.exports = config;
