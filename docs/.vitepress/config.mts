import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "🍕 Contoso Pizza Workshop",
  description: "Contoso Pizza",
  ignoreDeadLinks: true,
  head: [['link', { rel: 'icon', href: '/favicon.ico' }]],
  lang: 'en-US',
  lastUpdated: true,  
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config

    sidebar: [
      { 
        text: 'Welcome',
        items: [
          { text: 'Get started', link: '/index' },
          { text: 'About the workshop', link: '/about' },
        ]
      },
      {
        text: 'Setup',
        items: [
          { text: 'Get an Azure Subscription', link: '/get-azure' },
          { text: 'Developer Environment Setup', link: '/dev-environment' }
        ]
      },
      {
        text: 'Workshop',
        items: [
          { text: '1. Setup Microsoft Foundry', link: '/1_microsoft-foundry' },
          { text: '2. Create your first agent', link: '/2_create-agent' },
          { text: '3. Add instructions', link: '/3_add-instructions' },
          { text: '4. Add knowledge', link: '/4_add-knowledge' },
          { text: '5. Add estimation tool', link: '/5_add-tool' },
          { text: '6. Integrating MCP', link: '/6_add-mcp' },
        ]
      },
      {
        text: 'Resources',
        items: [
          { text: 'Pizza MCP server', link: '/pizza-mcp' }
        ]
      },
      { text: 'License', link: '/license' },
      { text: '✉️ Contact & Feedback', link: '/contact-feedback' }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/GlobalAICommunity/agentcon-pizza-workshop' }
    ],
    search: {
      provider: 'local'
    }
  },
  
})
