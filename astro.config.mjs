import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://devcloudninjas.github.io',
  base: '/DevOps-Projects',
  integrations: [
    starlight({
      title: 'DevOps Projects',
      description:
        'A student-first DevOps learning portal with 54 hands-on projects, guided paths, safety runbooks, and portfolio-ready proof.',
      customCss: ['./src/styles/portal.css'],
      favicon: '/favicon.svg',
      lastUpdated: true,
      pagefind: true,
      social: [
        {
          icon: 'github',
          label: 'GitHub repository',
          href: 'https://github.com/DevCloudNinjas/DevOps-Projects',
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
            { label: 'Catalog Overview', link: '/catalog/' },
            { label: 'Project Picker', link: '/catalog/project-picker/' },
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
            { label: 'Flagship Docs', link: '/flagship/' },
            { label: 'Community', link: '/community/' },
            { label: 'Marketing', link: '/marketing/' },
          ],
        },
      ],
    }),
  ],
});
