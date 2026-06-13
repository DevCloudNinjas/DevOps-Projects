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
