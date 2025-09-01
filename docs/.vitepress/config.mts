import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Pizza Workshop",
  description: "Contoso Pizza",
  ignoreDeadLinks: true,
  head: [['link', { rel: 'icon', href: '/favicon.ico' }]],
  lang: 'en-US',
  lastUpdated: true,  
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Workshop', link: '/' }
    ],

    sidebar: [
      { text: 'Welcome', link: '/' },
      {
        text: 'Setup & Resources',
        items: [
          { text: 'Get Azure', link: '/get-azure' },
          { text: 'Dev environment', link: '/dev-environment' },
          { text: 'Pizza MCP', link: '/pizza-mcp' }
        ]
      },
      {
        text: 'Workshop',
        items: [
          { text: '1. Setup Azure AI Foundry', link: '/1_ai-foundry' },
          { text: '2. Create your first agent', link: '/2_create-agent' },
          { text: '3. Add instructions', link: '/3_add-instructions' },
          { text: '4. Add knowledge', link: '/4_add-knowledge' },
          { text: '5. Add estimation tool', link: '/5_add-tool' },
          { text: '6. Integrating MCP', link: '/6_add-mcp' },
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/GlobalAICommunity/agentcon-pizza-workshop' }
    ]
  }
})
