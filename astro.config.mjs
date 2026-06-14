import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const isVercel = process.env.VERCEL === '1' || process.env.VERCEL === 'true';
const base = isVercel ? '/' : '/DevOps-Projects';
const site = isVercel
  ? `https://${process.env.VERCEL_URL ?? 'devops-projects.vercel.app'}`
  : 'https://devcloudninjas.github.io';

export default defineConfig({
  site,
  base,
  integrations: [
    starlight({
      title: 'DevOps Projects',
      description:
        'A student-first DevOps learning portal with 54 hands-on projects, guided paths, safety runbooks, and portfolio-ready proof.',
      customCss: ['./src/styles/portal.css'],
      favicon: '/favicon.svg',
      lastUpdated: true,
      pagefind: true,
      head: [
        {
          tag: 'script',
          attrs: { type: 'module' },
          content: `(() => {
            const STORAGE_KEY = 'devops-sidebar-collapsed';
            const root = document.documentElement;

            const readStoredState = () => {
              try {
                return localStorage.getItem(STORAGE_KEY) === '1';
              } catch {
                return false;
              }
            };

            const writeState = (collapsed) => {
              root.dataset.sidebarCollapsed = collapsed ? 'true' : 'false';
              try {
                localStorage.setItem(STORAGE_KEY, collapsed ? '1' : '0');
              } catch {}

              const button = document.querySelector('[data-sidebar-toggle]');
              if (button) {
                button.setAttribute('aria-pressed', String(collapsed));
                button.setAttribute('aria-label', collapsed ? 'Expand sidebar' : 'Collapse sidebar');
                button.title = collapsed ? 'Expand sidebar' : 'Collapse sidebar';
              }
            };

            const mount = () => {
              const titleWrapper = document.querySelector('.title-wrapper');
              if (!titleWrapper || titleWrapper.querySelector('[data-sidebar-toggle]')) return;

              const button = document.createElement('button');
              button.type = 'button';
              button.className = 'sidebar-toggle print:hidden';
              button.dataset.sidebarToggle = 'true';
              button.innerHTML =
                '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="m15 18-6-6 6-6"></path></svg>';
              titleWrapper.prepend(button);
              button.addEventListener('click', () => writeState(root.dataset.sidebarCollapsed !== 'true'));
              writeState(root.dataset.sidebarCollapsed === 'true');
            };

            root.dataset.sidebarCollapsed = readStoredState() ? 'true' : 'false';
            document.addEventListener('DOMContentLoaded', mount, { once: true });
            if (document.readyState !== 'loading') mount();
            window.addEventListener('pageshow', mount);
          })();`,
        },
      ],
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 3,
      },
      sidebar: [
        { label: 'Home', link: '/' },
        {
          label: 'Start Here',
          items: [
            { label: 'Start Here', link: '/catalog/start-here/' },
            { label: 'Catalog Overview', link: '/catalog/' },
            { label: 'Project Picker', link: '/catalog/project-picker/' },
            { label: 'Beginner Route', link: '/learning-paths/beginner/' },
            { label: 'Docker/Kubernetes Route', link: '/learning-paths/docker-kubernetes/' },
            { label: 'AWS/Terraform Route', link: '/learning-paths/terraform-iac/' },
            { label: 'DevSecOps Route', link: '/learning-paths/devsecops/' },
            { label: 'Portfolio Route', link: '/flagship/' },
            { label: 'Run Safely', link: '/runbooks/' },
          ],
        },
        {
          label: 'Projects',
          collapsed: true,
          items: [
            { label: 'All Projects', link: '/projects/' },
            { label: 'Project Picker', link: '/catalog/project-picker/' },
            { label: 'ArgoCD GitOps Home Lab', link: '/projects/50-argocd-gitops-home-lab/' },
            { label: 'OpenTelemetry Home Lab', link: '/projects/51-opentelemetry-observability-home-lab/' },
            { label: 'OpenTofu Free-Tier Lab', link: '/projects/52-opentofu-aws-free-tier-lab/' },
            { label: 'Supply Chain Security Lab', link: '/projects/53-supply-chain-security-lab/' },
            { label: 'Progressive Delivery Lab', link: '/projects/54-progressive-delivery-home-lab/' },
          ],
        },
        {
          label: 'Learning Paths',
          items: [{ autogenerate: { directory: 'learning-paths' } }],
        },
        {
          label: 'Runbooks',
          collapsed: true,
          items: [
            { label: 'Student Guide', link: '/runbooks/student-implementation-guide/' },
            { label: 'Credentials & Cost Safety', link: '/runbooks/credentials-and-cost-safety/' },
            { label: 'IaC and Kubernetes', link: '/iac-kubernetes-solid-runbook/' },
          ],
        },
        {
          label: 'Reference',
          collapsed: true,
          items: [
            { label: 'Security Baselines', link: '/security-baselines/' },
            { label: 'Project README Template', link: '/project-readme-template/' },
            { label: 'Tags', link: '/tags/' },
            { label: 'Flagship Docs', link: '/flagship/' },
            { label: 'Community', link: '/community/' },
            { label: 'Marketing', link: '/marketing/' },
          ],
        },
        {
          label: 'Support',
          collapsed: true,
          items: [
            { label: 'Support The Project', link: '/support/' },
            { label: 'Premium Kit', link: '/premium-kit/' },
            { label: 'Accelerator', link: '/accelerator/' },
            { label: 'For Schools And Teams', link: '/for-schools/' },
          ],
        },
      ],
    }),
  ],
});
